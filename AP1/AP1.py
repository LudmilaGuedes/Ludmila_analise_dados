# O dataset NCR Ride Bookings contém registros de corridas urbanas realizadas em regiões da National Capital Region (NCR), que abrange Delhi, Gurgaon, Noida, Ghaziabad, Faridabad e áreas próximas.
# Utilize os arquivos : ncr_ride_bookings.csv e ncr_ride_regions.xlsx para resolver as questoes.
# Principais informaçoes no dataset:
# Date → Data da corrida
# Time → Horário da corrida
# Booking ID → Identificador da corrida
# Booking Status → Status da corrida
# Customer ID → Identificador do cliente
# Vehicle Type → Tipo de veículo
# Pickup Location → Local de embarque
# Drop Location → Local de desembarque
# Booking Value → Valor da corrida
# Ride Distance → Distância percorrida
# Driver Ratings → Avaliação do motorista
# Customer Rating → Avaliação do cliente
# Payment Method → Método de pagamento

import pandas as pd
dfBookings = pd.read_csv("C:\\Ludmila\\faculdade\\ProgramacaoAnaliseDados\\AP1\\ncr_ride_bookings.csv")
dfRegioes = pd.read_excel("C:\\Ludmila\\faculdade\\ProgramacaoAnaliseDados\\AP1\\ncr_ride_regioes.xlsx")

# 1 - Quantas corridas estão com Status da Corrida como Completada ("Completed") no dataset? 

CorridasCompleta = dfBookings[dfBookings['Booking Status'] == 'Completed']
qtd_Completa = CorridasCompleta.shape[0]
print(qtd_Completa)

# 2 - Qual a proporção em relação ao total de corridas?

TotalCorridas = dfBookings.shape[0]
proporcao = qtd_Completa/TotalCorridas

# 3 - Calcule a média e mediana da Distância percorrida por cada Tipo de veículo.
dfBookings.info

GoSedan = dfBookings[dfBookings['Vehicle Type'] == 'Go Sedan']
mediaGoSedan = GoSedan['Ride Distance'].mean()
medianaGoSedan = GoSedan['Ride Distance'].median()

Auto = dfBookings[dfBookings['Vehicle Type'] == 'Auto']
mediaAuto = Auto['Ride Distance'].mean()
medianaAuto = Auto['Ride Distance'].median()

PremierSedan = dfBookings[dfBookings['Vehicle Type'] == 'Premier Sedan']
mediaPremierSedan = PremierSedan['Ride Distance'].mean()
medianaPremierSedan = PremierSedan['Ride Distance'].median()

Bike = dfBookings[dfBookings['Vehicle Type'] == 'Bike']
mediaBike = Bike['Ride Distance'].mean()
medianaBike = Bike['Ride Distance'].median()

GoMini = dfBookings[dfBookings['Vehicle Type'] == 'Go Mini']
mediaGoMini = GoMini['Ride Distance'].mean()
medianaGoMini= GoMini['Ride Distance'].median()

eBike = dfBookings[dfBookings['Vehicle Type'] == 'eBike']
mediaEBike = eBike['Ride Distance'].mean()
medianaEBike = eBike['Ride Distance'].median()


# 4 - Qual o Metodo de Pagamento mais utilizado pelas bicicletas ("Bike") ?

MetodosBike= Bike['Payment Method'].mode()


# 5 - Faca um merge com ncr_ride_regions.xlsx pela coluna ("Pickup Location") para pegar as regioes das corrifas.
# e verifique qual a Regiao com o maior Valor da corrida?

dfMerge = dfBookings.merge(dfRegioes, on="Pickup Location", how="left")
colunas = ['Booking Value', 'Regiao']
maior = dfMerge[colunas].nlargest(1, 'Booking Value')


# 6 - O IPEA disponibiliza uma API pública com diversas séries econômicas. 
# Para encontrar a série de interesse, é necessário primeiro acessar o endpoint de metadados.
# Acesse o endpoint de metadados: "http://www.ipeadata.gov.br/api/odata4/Metadados"
# e filtre para encontrar as séries da Fipe relacionadas a venda de imoveis (“venda”).
# Dica Técnica, filtre atraves das coluna FNTSIGLA: df["FNTSIGLA"].str.contains() 
# e depois SERNOME: df["SERNOME"].str.contains() 


# Descubra qual é o código da série correspondente.
# Usando o código encontrado, acesse a API de valores: f"http://ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{CODIGO_ENCONTRADO}')"
# e construa um DataFrame pandas com as datas (DATA) e os valores (VALVALOR).
# Converta a coluna de datas para o formato adequado (pd.to_datetime())

import requests
response = requests.get('http://www.ipeadata.gov.br/api/odata4/Metadados')
pd.json_normalize(response)
response.status_code
response = response.json()
dados= response["value"]
dados = dados["SERCODIGO"]

dfIPEA = pd.DataFrame(dados)

df_anfavea = dfIPEA[dfIPEA["FNTSIGLA"].str.contains("anfavea.*", regex=True, case=False)]
df_licenciamento = df_anfavea[df_anfavea["SERNOME"].str.contains("licenciamento", regex=True, case=False)]

serie = df_licenciamento[df_licenciamento["SERCOMENTARIO"].str.contains("automóveis.*comerciais.*pesados", regex=True, case=False)]

codigo_serie = serie["SERCODIGO"].values[0]


# 7 -  Monte um gráfico de linha mostrando a evolução das vendas ao longo do tempo.
# Dica: você pode usar a biblioteca matplotlib para gerar o gráfico.

df_valores = pd.DataFrame(dados)

df_valores["data"] = pd.to_datetime(df_valores["data"], utc=True, errors="coerce")
df_valores["data"] = df_valores["data"].dt.tz_convert("America/Sao_Paulo")
df_valores["DATA"] = df_valores["data"].dt.date

plt.figure(figsize=(12,6))
plt.plot(df_valores["DATA"], df_valores["vendas"])
plt.title("evolução das vendas ao longo do tempo.")
plt.xlabel("Ano")
plt.ylabel("Valor fechamento")
plt.grid(True)
plt.tight_layout()
plt.show()


# 8 - Crie o grafico do bitcoin (ticker: "btc") atraves da api preco-diversos
# Pegue o periodo compreendido entre 2001 a 2025
# Monte um gráfico de linha mostrando a evolução do preco de fechamento

import matplotlib.pyplot as plt
import requests
token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
headers = {'Authorization': 'Bearer {}'.format(token)}
params = {
'ticker': 'ibov',
'data_ini': '2001-01-01',
'data_fim': '2025-01-01'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
response = response.json()
dados= response["dados"]
df_valores = pd.DataFrame(dados)

df_valores["data"] = pd.to_datetime(df_valores["data"], utc=True, errors="coerce")
df_valores["data"] = df_valores["data"].dt.tz_convert("America/Sao_Paulo")
df_valores["DATA"] = df_valores["data"].dt.date

plt.figure(figsize=(12,6))
plt.plot(df_valores["DATA"], df_valores["fechamento"])
plt.title("evolução do preco de fechamento")
plt.xlabel("Ano")
plt.ylabel("Valor fechamento")
plt.grid(True)
plt.tight_layout()
plt.show()


# 9 - Você tem acesso à API do Laboratório de Finanças, que fornece dados do Planilhão em formato JSON. 
# A autenticação é feita via JWT Token no cabeçalho da requisição.
# Acesse a API no endpoint: https://laboratoriodefinancas.com/api/v1/planilhao
# passando como parâmetro a data (por exemplo, "2025-09-23").
# Construa um DataFrame pandas a partir dos dados recebidos.
# Selecione a empresa do setor de "tecnologia" que apresenta o maior ROC (Return on Capital) nessa data.
# Exiba o ticker da empresa, setor e o valor do ROC correspondente.

import requests
token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
'data_base': '2025-09-23'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados= response["dados"]
df = pd.DataFrame(dados)

dfTecnologia = df[(df['setor'] == 'tecnologia')]

colunas = ['ticker','setor', 'preco', 'roc']
maiorROC = dfTecnologia[colunas].nlargest(1, 'roc')

# 10 - A API do Laboratório de Finanças fornece informações de balanços patrimoniais de empresas listadas na B3.
# Acesse o endpoint: https://laboratoriodefinancas.com/api/v1/balanco
# usando a empresa Gerdau ("GGBR4") e o período 2025/2º trimestre (ano_tri = "20252T").
# O retorno da API contém uma chave "balanco", que é uma lista com diversas contas do balanço.
# Localize dentro dessa lista a conta cuja descrição é “Ativo Total” e "Lucro Liquido".
# Calcule o Return on Assets que é dados pela formula: ROA = Lucro Liquido / Ativo Totais.

import requests
token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'GGBR4', 
          'ano_tri': '20252T'
          }
response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
response = response.json()
dados= response["dados"][0]
balanco = dados['balanco']
df = pd.DataFrame(balanco)

filtro = (df["descricao"]=='Ativos Totais') & (df["descricao"].str.contains("^lucro", case=False)) 
df.loc[filtro]

lucro_liquido = df.iloc[filtro, ["valor"]].iloc[0]

filtro2 = (
    (df["conta"] == "2.03") &
    (df["descricao"].str.contains("^patrim", case=False))
)

ativos = df.loc[filtro2, ["valor"]].iloc[0]
roe = lucro_liquido/ativos