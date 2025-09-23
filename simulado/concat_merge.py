import pandas as pd

df = pd.read_csv("C:\\Ludmila\\faculdade\\ProgramacaoAnaliseDados\\simulado\\myntra_dataset_ByScraping.csv")

# 1. Crie um novo DataFrame fictício chamado df_novos_produtos com as seguintes informações e use pd.concat([df, df_novos_produtos]) para juntar ao dataset original e verifique o novo tamanho do DataFrame.

dados_novos_produtos = {
    "brand_name": ["Myntra Basics", "Denim Pro", "Urban Style"],
    "pants_description": [
        "Men Slim Fit Blue Jeans",
        "Men Regular Fit Jeans",
        "Men Tapered Fit Jeans"
    ],
    "price": [1299, 1599, 1899],
    "MRP": [1999, 2499, 2899],
    "discount_percent": [0.35, 0.40, 0.34],
    "ratings": [4.1, 3.8, 4.3],
    "number_of_ratings": [23, 12, 47]
}
df_novos_produtos = pd.DataFrame(dados_novos_produtos)

#juntando dataframes 
df_novo = pd.concat([df,df_novos_produtos])

#verificando tamanho 
tamanho = df_novo.shape


import pandas as pd

df = pd.read_csv("C:\\Ludmila\\faculdade\\ProgramacaoAnaliseDados\\simulado\\myntra_dataset_ByScraping.csv")

# 1. Crie um novo DataFrame fictício chamado df_novos_produtos com as seguintes informações e use pd.concat([df, df_novos_produtos]) para juntar ao dataset original e verifique o novo tamanho do DataFrame.

dados_novos_produtos = {
    "brand_name": ["Myntra Basics", "Denim Pro", "Urban Style"],
    "pants_description": [
        "Men Slim Fit Blue Jeans",
        "Men Regular Fit Jeans",
        "Men Tapered Fit Jeans"
    ],
    "price": [1299, 1599, 1899],
    "MRP": [1999, 2499, 2899],
    "discount_percent": [0.35, 0.40, 0.34],
    "ratings": [4.1, 3.8, 4.3],
    "number_of_ratings": [23, 12, 47]
}
df_novos_produtos = pd.DataFrame(dados_novos_produtos)

#juntando dataframes 
pd.concat([df,df_novos_produtos])

#verificando tamanho 
tamanho = df.shape

# 2. Crie outro DataFrame df_promocoes apenas com colunas brand_name, pants_description e discount_percent para 3 novos produtos fictícios. Depois, use pd.concat([...], axis=0) e pd.concat([...], axis=1) e explique a diferença entre concatenação por linhas e concatenação por colunas.

dados_promocoes = {
    "brand_name": ["Test Brand A", "Test Brand B", "Test Brand C"],
    "pants_description": [
        "Men Slim Fit Black Jeans",
        "Men Regular Fit Grey Jeans",
        "Men Loose Fit White Jeans"
    ],
    "discount_percent": [0.50, 0.60, 0.45]
}
df_promocoes = pd.DataFrame(dados_promocoes)
pd.concat([df,df_novos_produtos], axis=1)

# # axis=0, concatenação por linhas (empilha os DataFrames verticalmente)
# df_linhas = pd.concat([df_promocoes, df_promocoes], axis=0)

# # axis=1, concatenação por colunas (junta os DataFrames lado a lado)
# df_colunas = pd.concat([df_promocoes, df_promocoes], axis=1)


# 3. Crie um DataFrame auxiliar chamado df_marcas_info com informações extras sobre algumas marcas e faça um merge entre o dataset original (df) e esse DataFrame usando a coluna brand_name.
dados_marcas_info = {
    "brand_name": ["Roadster", "WROGN", "Flying Machine", "Urban Style"],
    "country": ["India", "India", "USA", "Brazil"],
    "year_founded": [2012, 2014, 1980, 2018]
}

df_marcas_info = pd.DataFrame(dados_marcas_info)

# Fazer o merge com o DataFrame principal
df = pd.merge(df, df_marcas_info, on='brand_name', how='inner')


# 4. Crie um DataFrame df_categorias e faça um merge (inner join) entre df e df_categorias para adicionar a coluna category.
# Exemplo de dicionário:
dados_categorias = {
    "pants_description": [
        "Men Slim Fit Jeans",
        "Men Regular Fit Jeans",
        "Men Loose Fit Cotton Jeans",
        "Men Tapered Fit Jeans"
    ],
    "category": ["Slim", "Regular", "Loose", "Tapered"]
}

df_categorias = pd.DataFrame(dados_categorias)

# Fazer o merge (inner join) com df
df = pd.merge(df, df_categorias, on='pants_description', how='inner')


# 5. Imagine que você tem um DataFrame df_ratings_extra com avaliações atualizadas. Faça um merge com o dataset original, mantendo todos os registros (how='left'). Depois compare ratings (antiga) com avg_new_rating (nova).
# Exemplo de dicionário:
dados_ratings_extra = {
    "brand_name": ["Roadster", "WROGN", "Urban Style"],
    "avg_new_rating": [4.0, 4.3, 4.1]
}

df_ratings_extra = pd.DataFrame(dados_ratings_extra)

# Fazer o merge mantendo todos os registros do df original
df_novo = pd.merge(df, df_ratings_extra, on='brand_name', how='left')

#comparacao
df_novo[('rattings', "avg_new_ratings")]