import pandas as pd
import json
import sqlalchemy

from sqlalchemy import create_engine, inspect, text, MetaData
from sqlalchemy.orm import declarative_base

dados_fornecedores = pd.read_csv('fornecedores.csv', sep=';', dtype={'cod_fornecedor': str}, decimal=',', encoding='latin-1')
dados_fornecedores['receita_anual'] = dados_fornecedores['receita_anual'].str.replace('.', '', regex=False).str.replace(',', '.').astype('float64')

dados_contratos = pd.read_json('contratos.json', orient='records', dtype={'cod_fornecedor': str})
dados_contratos['vigencia_inicio'] = pd.to_datetime(dados_contratos['vigencia_inicio'], format='%d/%m/%Y')
dados_contratos['vigencia_fim'] = pd.to_datetime(dados_contratos['vigencia_fim'], format='%d/%m/%Y')

dados_notas_fiscais = pd.read_xml('notas_fiscais.xml', dtype={'cod_fornecedor': str}, encoding='utf-8')
dados_notas_fiscais['data_emissao'] = pd.to_datetime(dados_notas_fiscais['data_emissao'], format='%Y-%m-%d')

engine = create_engine('sqlite:///auditoria.db')
Base = declarative_base()
Base.metadata.create_all(engine)

dados_fornecedores.to_sql('fornecedores', con=engine, if_exists='replace', index=False)
dados_contratos.to_sql('contratos', con=engine, if_exists='replace', index=False)
dados_notas_fiscais.to_sql('notas_fiscais', con=engine, if_exists='replace', index=False)

query = "SELECT f.cod_fornecedor, f.razao_social, SUM(nf.valor_nf) as total_faturado \
        FROM fornecedores f \
        LEFT JOIN notas_fiscais nf ON f.cod_fornecedor = nf.cod_fornecedor \
        GROUP BY f.cod_fornecedor, f.razao_social \
        ORDER BY total_faturado DESC"
print(pd.read_sql(query, engine))

query = "SELECT c.num_contrato, f.razao_social, c.valor_contrato, \
            COALESCE(SUM(nf.valor_nf), 0) as total_executado, \
            ROUND(COALESCE(SUM(nf.valor_nf), 0) * 100.0 / c.valor_contrato, 1) as pct_executado \
        FROM contratos c \
        JOIN fornecedores f ON c.cod_fornecedor = f.cod_fornecedor \
        LEFT JOIN notas_fiscais nf ON c.num_contrato = nf.num_contrato \
        WHERE c.status_contrato = 'ativo' \
        GROUP BY c.num_contrato \
        ORDER BY pct_executado DESC"
print(pd.read_sql(query, engine))

query = "SELECT f.cod_fornecedor, f.razao_social, f.uf \
        FROM fornecedores f \
        LEFT JOIN notas_fiscais nf ON f.cod_fornecedor = nf.cod_fornecedor \
        WHERE nf.numero_nf IS NULL"
print(pd.read_sql(query, engine))


