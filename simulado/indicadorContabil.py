# 1 - 
# passando como parƒmetro a data do dia de hoje (por exemplo, "2025-09-17").
# Construa um DataFrame pandas a partir dos dados recebidos.
# Selecione a empresa que apresenta o maior ROE (Return on Equity) nessa data.
# Exiba o nome da empresa e o valor do ROE correspondente.

import requests
import pandas as pd

token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
'data_base': '2025-09-17'
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
pd.json_normalize(response)
response.status_code
response = response.json()
dados= response["dados"]
df = pd.DataFrame(dados)

colunas = ['ticker', 'roe', 'data_base']
maiorROE = df[colunas].nlargest(1, 'roe')


# 2 - Acesse a API do Planilh?o e traga os dados de uma data de sua escolha.
# Construa um DataFrame pandas com os dados recebidos.
# Filtre as empresas que pertencem ao setor ?petr¢leo?.
# Elimine todos os registros cujo indicador P/VP (p_vp) seja negativo.
# Selecione a empresa com o maior P/VP dentro do setor de petr¢leo e exiba seu ticker, setor e valor de P/VP.

dfPetroleo = df[(df['setor'] == 'petróleo') & (df['p_vp'] > 0)]

colunas2 = ['ticker','setor', 'preco', 'p_vp']
maiorPVP= dfPetroleo[colunas2].nlargest(1, 'p_vp')


# 3 -
# usando o ticker PETR4 e o per¡odo 2025/2§ trimestre (ano_tri = "20252T").
# O retorno da API cont‚m uma chave "balanco", que ‚ uma lista com diversas contas do balan‡o.
# Localize dentro dessa lista a conta cuja descri‡?o ‚ ?1 - Ativo Total?.
# Exiba o valor correspondente a essa conta.

import requests
token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'PETR4', 
'ano_tri': '20252T'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
pd.json_normalize(response)
response.status_code
response = response.json()
dados= response["dados"][0]
balanco = dados['balanco']
df2 = pd.DataFrame(balanco)

ativoTotal = df2[(df2['descricao'] == 'Ativo Total')]
valorAtivo = ativoTotal['valor'][0] 
