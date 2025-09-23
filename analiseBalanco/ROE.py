# import requests
# import pandas as pd
# import time

# # Token de autenticação
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
# headers = {'Authorization': f'JWT {token}'}

# # 1. Buscar todos os tickers
# response = requests.get('https://laboratoriodefinancas.com/api/v1/ticker', headers=headers)
# response = response.json()
# dados = response["dados"]
# lista_tickers = [item['ticker'] for item in dados]

# # 2. Função para buscar ROE de cada ticker
# def buscar_roe(ticker):
#     url = f"https://laboratoriodefinancas.com/api/v1/indicadores/{ticker}"
#     try:
#         r = requests.get(url, headers=headers)
#         if r.status_code == 200:
#             indicadores = r.json()
#             roe = indicadores.get('roe', None)
#             return roe
#         else:
#             return None
#     except Exception as e:
#         return None

# # 3. Loop para buscar ROE de todos os tickers
# resultados = []
# for ticker in lista_tickers:
#     roe = buscar_roe(ticker)
#     resultados.append({'Ticker': ticker, 'ROE': roe})
#     time.sleep(0.5)  # respeita o servidor

# # 4. Criar DataFrame com os resultados
# df_roe = pd.DataFrame(resultados)

# # 5. Exibir os primeiros resultados
# print(df_roe.head())

#Planilhao
import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5NTc1OTczLCJpYXQiOjE3NTY5ODM5NzMsImp0aSI6ImI5ZmEwMjNjNmFmMTQwMWI4OTEwMmU1NjUzMzVjNTFlIiwidXNlcl9pZCI6IjQ5In0.o5_dZ9ARgy78WHEIH1Q_rKDw-me3DxykRRg6sqnEBkE"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'data_base': '2025-09-01'}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
filtro = df["setor"]=="construção"
tickers = df.loc[filtro, "ticker"].values
lista_resultado = []
# Inicio do for loop
for ticker in tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
        }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)
    # Lucro Liquido
    filtro = (
            (df["conta"]=="3.11") &
            (df["descricao"].str.contains("^lucro", case=False)) &
            (df["data_ini"]=="2025-01-01")
            )
    lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]
    # PL
    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) &
            (df["descricao"].str.contains("^patrim", case=False))
            )
    pl = df.loc[filtro, ["valor"]].iloc[0]
    roe = lucro_liquido / pl
    roe = roe.iloc[0]
    resultados = {
                "ticker":ticker,
                "roe": roe
        }
    lista_resultado.append(resultados)
    print(ticker, roe)
df_final = pd.DataFrame(lista_resultado)
df_final.sort_values(["roe"])