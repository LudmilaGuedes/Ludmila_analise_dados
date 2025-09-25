import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco')
params = {
'ticker': 'PETR4',
'ano_tri': '20231T',
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
pd.json_normalize(response)
response.status_code
response = response.json()
dados= response["dados"][0]
balanco = dados['balanco']
df = pd.DataFrame(balanco)

filtro = (df["conta"]=='3.11') & (df["descricao"].str.contains("^lucro", case=False)) 
df.loc[filtro]

lucro_liquido = df.iloc[filtro, ["valor"]].iloc[0]

filtro = (
    (df["conta"] == "2.03") &
    (df["descricao"].str.contains("^patrim", case=False))
)

pl = df.loc[filtro, ["valor"]].iloc[0]
roe = lucro_liquido/pl 

# • Git init 
# 	◦ inicializar um novo repositório 
# • git remote add origin 
# 	◦ adicionar repositório remoto ao seu repositório Git local 
# 	◦ git remote add origin + link do repositório (pega no git hub)
# • git pull origin main 
# 	◦ atualizar e puxar arquivos do repositório remoto 
# • git status 
# 	◦ verificar qual brunch seu repositório local está configurado 
# • git checkout -b main 
# 	◦ mudar a brunch para main 
# • git add .
# 	◦ atualiza as alterações 
# • git commit -m “atualizacao"
# 	◦ salvar alterações no repositório 
# • git push origin main 
# 	◦ empurra alterações para o repositório remoto

# INNER JOIN (Junção Interna)
# Retorna apenas os registros que têm correspondência nas duas tabelas.
# Imagine duas listas: ele mostra só os itens que aparecem nas duas ao mesmo tempo.

# FULL JOIN (Junção Completa)
# Retorna todos os registros das duas tabelas, combinando os que têm correspondência e mantendo os que não têm.
# É como juntar duas listas inteiras, mesmo que alguns itens não combinem.

# LEFT JOIN (Junção à Esquerda)
# Retorna todos os registros da tabela da esquerda, e os correspondentes da tabela da direita (se houver).
# Se não houver correspondência, os dados da direita aparecem como nulos.

# RIGHT JOIN (Junção à Direita)
# Retorna todos os registros da tabela da direita, e os correspondentes da tabela da esquerda (se houver).
# Também preenche com nulos quando não há correspondência.