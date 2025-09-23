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
lista_resultadoROE = []
lista_resultadoROIC = []
lista_resultadoPva = []

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

    #ROIC
    # Lucro Operacional
    filtro = (
            (df["conta"]=="3.05") &
            (df["descricao"].str.contains("resultado antes", case=False)) &
            (df["data_ini"]=="2025-01-01")
            )
    lucro_operacional = df.loc[filtro, ["valor"]].iloc[0]
    # PL
    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) &
            (df["descricao"].str.contains("^patrim", case=False))
            )
    pl = df.loc[filtro, ["valor"]].iloc[0]
    # Emprestimos 
    filtro = (
            (df["conta"].str.contains("2.01.04", case=False)) &
            (df["descricao"].str.contains("^empr.stimos*", case=False))
            )
    emprestimos = df.loc[filtro, ["valor"]].iloc[0]
    # Calculo 
    roic = lucro_operacional / (emprestimos+pl)
    roic = roic.iloc[0]
    resultados = {
                "ticker":ticker,
                "roic": roic
        }
    lista_resultadoROIC.append(resultados)
    print(ticker, roic)

    #ROE
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
    lista_resultadoROE.append(resultados)
    print(ticker, roe)

df_finalROE = pd.DataFrame(lista_resultadoROE)
df_finalROE.sort_values(["roe"])
df_finalROIC = pd.DataFrame(lista_resultadoROIC)
df_finalROIC.sort_values(["roic"])

df_final = pd.merge(df_finalROE, df_finalROIC, on="ticker", 
                    how="inner").drop_duplicates() 
df_final["media"] = (df_final["roe"] + df_final["roic"]) / 2 
df_final = df_final.sort_values(by="media", ascending=False)
#### Calculando outros indicadores 
# Calculando os descontos 
# Inicio do loop
for ticker in tickers:
    params = {
        'ticker': ticker,
        'ano_tri': '20252T',
        }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response["dados"][0]
    n_acoes = dados["total"] # Numero de acoes do ticker´s (total)
    balanco = dados["balanco"] # Balanco 
    df = pd.DataFrame(balanco)

    # Lucro liquido 
    filtro = (
        (df["conta"]=="3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) & 
        (df['data_ini']=="2025-01-01")
        )
    lucro_liquido = df.loc[filtro, "valor"].iloc[0]

    # PL
    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) &
            (df["descricao"].str.contains("^patrim", case=False))
            )
    pl = df.loc[filtro, "valor"].iloc[0]

    # Chamando api novamente 
    params = {'data_base': '2025-09-01'}
    response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
    response = response.json()
    dados = response["dados"]
    df_planilhao = pd.DataFrame(dados)
    filtro2 = df_planilhao["ticker"] == ticker
    preco = df_planilhao.loc[filtro2, "preco"].iloc[0]
    

    # Calculo dos descontos      
    p_vp = (preco * n_acoes)/ (pl * 1000)
    p_lucro = (preco * n_acoes) / (lucro_liquido * 1000)
    resultados_desconto = {
                "ticker":ticker,
                "p_vp": p_vp,
                "p_lucro": p_lucro
        }
    lista_resultadoPva.append(resultados_desconto)
    print(ticker, p_vp, p_lucro)
    df_final_desconto = pd.DataFrame(lista_resultadoPva)


df_finalROE = pd.DataFrame(lista_resultadoROE)
df_finalROE.sort_values(["roe"])
df_finalROIC = pd.DataFrame(lista_resultadoROIC)
df_finalROIC.sort_values(["roic"])
df_finalPVA = pd.DataFrame(lista_resultadoPva)
df_finalPVA.sort_values(["p_vp"])

df_final = pd.merge(df_finalROE, df_finalROIC, on="ticker", 
                    how="inner").drop_duplicates() 
df_final["media"] = (df_final["roe"] + df_final["roic"]) / 2 

df_final = df_final.sort_values(by="media", ascending=False)

df_final = pd.merge(df_final, df_finalPVA)
df_final["media_desconto"] = (abs(df_final["p_vp"]) + abs(df_final["p_lucro"]) / 2 )
df_final = df_final.sort_values(by="media_desconto", ascending=False)
