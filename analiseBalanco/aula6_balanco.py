import requests
import pandas as pd

# Token e cabeçalho
token = token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxNDc4LCJpYXQiOjE3NTYzNzk0NzgsImp0aSI6ImExOTA3MTk5ZTU2NDQ3OGVhNmI0NGJhNDViYzBlYzViIiwidXNlcl9pZCI6IjQ5In0.pZtn2sQhc-GKGZtjWeL6kcZy9RwrJQfKIMZkBak3MTc"
headers = {'Authorization': f'JWT {token}'}

# Parâmetros para buscar o planilhão
params_planilhao = {'data_base': '2025-09-01'}
url_planilhao = 'https://laboratoriodefinancas.com/api/v1/planilhao'

# Requisição do planilhão
response = requests.get(url_planilhao, params=params_planilhao, headers=headers)
if response.status_code != 200:
    raise Exception(f"Erro ao buscar planilhão: {response.status_code}")

dados_planilhao = response.json().get("dados", [])
df_planilhao = pd.DataFrame(dados_planilhao)

# Filtrar tickers do setor construção
tickers_construcao = df_planilhao[df_planilhao["setor"] == "construção"]["ticker"].unique()

# Lista para armazenar resultados
lista_resultado = []

# Filtrar tickers e ano_tri do setor construção
df_construcao = df_planilhao[df_planilhao["setor"] == "construção"]
tickers_ano = df_construcao[["ticker", "ano_tri"]].drop_duplicates()

lista_resultado = []

for _, row in tickers_ano.iterrows():
    ticker = row["ticker"]
    ano_tri = row["ano_tri"]  # usa o formato exato do planilhão

    params_balanco = {
        'ticker': ticker,
        'ano_tri': ano_tri
    }

    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params_balanco, headers=headers)

    if response.status_code == 404:
        print(f"Erro 404: balanço não encontrado para {ticker} no período {ano_tri}")
        continue

    try:
        dados_balanco = response.json()["dados"][0]["balanco"]
        df_balanco = pd.DataFrame(dados_balanco)

        # Lucro líquido
        filtro_lucro = (
            (df_balanco["conta"] == "3.11") &
            (df_balanco["descricao"].str.contains("^lucro", case=False)) &
            (df_balanco["data_ini"] == "2025-01-01")
        )
        lucro_liquido = df_balanco.loc[filtro_lucro, "valor"].iloc[0]

        # Patrimônio líquido
        filtro_pl = (
            (df_balanco["conta"] == "2.03") &
            (df_balanco["descricao"].str.contains("^patrim", case=False))
        )
        patrimonio_liquido = df_balanco.loc[filtro_pl, "valor"].iloc[0]

        roe = lucro_liquido / patrimonio_liquido

        lista_resultado.append({
            "ticker": ticker,
            "roe": roe
        })

        print(f"{ticker}: ROE = {roe:.4f}")

    except Exception as e:
        print(f"Erro ao processar dados de {ticker}: {e}")

# Transformar lista_resultado em DataFrame
df_roe_calculado = pd.DataFrame(lista_resultado)

# Unir com o planilhão original
df_planilhao_atualizado = df_planilhao.merge(df_roe_calculado, on="ticker", how="left", suffixes=("", "_calculado"))

# Exibir os tickers do setor construção com ROE original e calculado
df_construcao_comparado = df_planilhao_atualizado[df_planilhao_atualizado["setor"] == "construção"][["ticker", "roe", "roe_calculado"]]
print(df_construcao_comparado)

