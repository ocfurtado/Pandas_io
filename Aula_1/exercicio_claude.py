import pandas as pd

caminho_arquivo = 'pagamentos_fornecedores.csv'

pagamentos_fornecedores = pd.read_csv(caminho_arquivo, sep=';', encoding='latin-1')

pagamentos_fornecedores['status'] = pagamentos_fornecedores['status'].fillna('não informado')
pagamentos_fornecedores['cod_fornecedor'] = pagamentos_fornecedores['cod_fornecedor'].astype(str)
pagamentos_fornecedores['valor_pago'] = pagamentos_fornecedores['valor_pago'].str.replace('.', '', regex=False).str.replace(',', '.').astype(float)
pagamentos_fornecedores['data_pagamento'] = pd.to_datetime(pagamentos_fornecedores['data_pagamento'], format='%d/%m/%Y')

pagamentos_fornecedores.to_csv('pagamentos_limpo.csv', sep=',', index=False, encoding='UTF-8')