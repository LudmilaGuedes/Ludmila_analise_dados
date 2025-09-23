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
# • git commit -m “nome da mudança”
# 	◦ salvar alterações no repositório 
# • git push origin main 
# 	◦ empurra alterações para o repositório remoto