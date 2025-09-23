import requests
import pandas as pd


#1 - quantos feriados nacionais existem no ano atual?

ano = 2025
response = requests.get(f'https://brasilapi.com.br/api/feriados/v1/{ano}')
dados = response.json()
df = pd.DataFrame(dados)
quantidade = df.shape[0]


#2 - quantos modelos de veículos BYD estão cadastrados na FIPE? import requests

import pandas as pd

tipoVeiculo = "carros"

marcas = f"https://brasilapi.com.br/api/fipe/marcas/v1/{tipoVeiculo}"
response_marcas = requests.get(marcas)
dados_marcas = response_marcas.json()
df_marcas = pd.DataFrame(dados_marcas)

codigoBYD = df_marcas[df_marcas['nome'] == 'BYD']['valor'].values[0]

modelos = f"https://brasilapi.com.br/api/fipe/veiculos/v1/{tipoVeiculo}/{codigoBYD}"
response_modelos = requests.get(modelos)
dados_modelos = response_modelos.json()
df_modelos = pd.DataFrame(dados_modelos)
quantidadeBYD = df_modelos.shape[0]


#3 - qual ano o Brasil apresentou o menor PIB per capita e mostre o respectivo valor

import requests
import pandas as pd

pais="BRA"
indicador="NY.GDP.PCAP.CD"
url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json"

responsePIB = requests.get(url)
dadosPIB = responsePIB.json()
dadosPIB = dadosPIB[1]


dfPIB = pd.DataFrame(dadosPIB)
dfPIB = dfPIB[['date', 'value']]

menorPIB = dfPIB['value'].min()
menor = dfPIB[dfPIB['value'] == menorPIB]['date'].values[0]


#4 

import requests
import pandas as pd
import matplotlib.pyplot as plt

responseIPEA = requests.get('http://www.ipeadata.gov.br/api/odata4/Metadados')
dadosIPEA = responseIPEA.json()
dfIPEA = pd.DataFrame(dadosIPEA['value'])# Corrigido para acessar a chave 'value'

df_anfavea = dfIPEA[dfIPEA["FNTSIGLA"].str.contains("anfavea.*", regex=True, case=False)]
df_licenciamento = df_anfavea[df_anfavea["SERNOME"].str.contains("licenciamento", regex=True, case=False)]

serie = df_licenciamento[df_licenciamento["SERCOMENTARIO"].str.contains("automóveis.*comerciais.*pesados", regex=True, case=False)]

codigo_serie = serie["SERCODIGO"].values[0]

urlValores = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{codigo_serie}')"
responseValores = requests.get(urlValores)
dados_valores = responseValores.json()
df_valores = pd.DataFrame(dados_valores['value'])  


df_valores["VALDATA"] = pd.to_datetime(df_valores["VALDATA"], utc=True, errors="coerce")
df_valores["VALDATA"] = df_valores["VALDATA"].dt.tz_convert("America/Sao_Paulo")
df_valores["DATA"] = df_valores["VALDATA"].dt.date

plt.figure(figsize=(12,6))
plt.plot(df_valores["DATA"], df_valores["VALVALOR"])
plt.title("Licenciamento de Autoveículos no Brasil")
plt.xlabel("Ano")
plt.ylabel("Quantidade")
plt.grid(True)
plt.tight_layout()
plt.show()


#5

import requests
import pandas as pd

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
    "@dataInicial='01-01-2023'&@dataFinalCotacao='12-31-2023'&$format=json"
)
responsePTAX = requests.get(url)
dadosPTAX = responsePTAX.json()
dfPTAX = pd.DataFrame(dadosPTAX['value'])

dfPTAX["dataHoraCotacao"] = pd.to_datetime(dfPTAX["dataHoraCotacao"], utc=True, errors="coerce")


plt.figure(figsize=(12,6))
plt.plot(dfPTAX["dataHoraCotacao"], dfPTAX["cotacaoVenda"])
plt.title("cotacao dolar")
plt.xlabel("mes")
plt.ylabel("cotacao")
plt.grid(True)
plt.tight_layout()
plt.show()
