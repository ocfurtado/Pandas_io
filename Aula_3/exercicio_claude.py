import pandas as pd
import json

with open('cotacoes_fornecedores.json', 'r') as file:
    dados = json.loads(file.read())

df_normalizado = pd.json_normalize(dados,
                  record_path='itens',
                  meta=[
                      'data_cotacao', 
                      ['fornecedor', 'codigo'], 
                      ['fornecedor', 'razao_social'], 
                      ['fornecedor', 'cidade'], 
                      ['fornecedor', 'uf']],
                      sep='_')

df_normalizado['data_cotacao'] = pd.to_datetime(df_normalizado['data_cotacao'])

df_normalizado['valor_total'] =( df_normalizado['quantidade'] * df_normalizado['preco_unitario']).round(2)

df_normalizado.to_json('cotacoes_consolidado.json', orient='records', force_ascii=False, date_format='iso')

df_normalizado.to_excel('cotacoes_consolidado.xlsx', sheet_name='cotacoes', index=False)

