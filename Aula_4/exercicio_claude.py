import pandas as pd

dados_contratos_ativos = pd.read_html('contratos_ativos.html', encoding='utf-8')[1]
dados_notas_fiscais = pd.read_xml('notas_fiscais.xml')

dados_contratos_ativos['vigencia_inicio'] = pd.to_datetime(dados_contratos_ativos['vigencia_inicio'], format='%d/%m/%Y')
dados_contratos_ativos['vigencia_fim'] = pd.to_datetime(dados_contratos_ativos['vigencia_fim'], format='%d/%m/%Y')
dados_notas_fiscais['data_emissao'] = pd.to_datetime(dados_notas_fiscais['data_emissao'], format='%Y-%m-%d')

dados_notas_fiscais_agrupadas = dados_notas_fiscais.groupby(by='cod_fornecedor', as_index=False).agg(
    total_faturado = pd.NamedAgg(column='valor_nf', aggfunc='sum'),
    qtd_notas = pd.NamedAgg(column='numero_nf', aggfunc='count')
)

dados_consolidados = dados_contratos_ativos.merge(dados_notas_fiscais_agrupadas, how='outer', on='cod_fornecedor')

dados_consolidados[['total_faturado', 'qtd_notas']] = dados_consolidados[['total_faturado', 'qtd_notas']].fillna(0)
dados_consolidados[['razao_social']] = dados_consolidados[['razao_social']].fillna('SEM CONTRATO')

dados_consolidados['percentual_executado'] = ((dados_consolidados['total_faturado'] / dados_consolidados['valor_contrato']) * 100).round(1)
dados_consolidados['percentual_executado'] = dados_consolidados['percentual_executado'].fillna('N/A')

dados_consolidados.to_html('auditoria_contratos.html', index=False)
dados_consolidados.to_excel('auditoria_contratos.xlsx', sheet_name='auditoria', index=False)



