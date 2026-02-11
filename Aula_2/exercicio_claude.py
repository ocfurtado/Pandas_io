import pandas as pd

dados_brutos = pd.read_excel('beneficios_funcionarios.xlsx',
                             sheet_name='dados_brutos',
                             skiprows=3,
                             dtype={'matricula': str},
                             usecols='A:E')

tabela_desconto = pd.read_excel('beneficios_funcionarios.xlsx',
                                sheet_name='tabela_desconto')

dados_consolidados = pd.merge(dados_brutos, tabela_desconto, how='left', on='tipo_beneficio')

dados_consolidados['valor_desconto'] = (
    dados_consolidados['valor_mensal'] * dados_consolidados['percentual_desconto']
).round(2)

dados_consolidados['valor_liquido'] = (
    dados_consolidados['valor_mensal'] - dados_consolidados['valor_desconto']
).round(2)

dados_consolidados.to_excel('beneficios_consolidado.xlsx',
                            sheet_name='consolidado',
                            index=False)

