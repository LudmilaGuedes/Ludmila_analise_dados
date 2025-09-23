import pandas as pd

df = pd.read_csv("C:\\Ludmila\\faculdade\\ProgramacaoAnaliseDados\\simulado\\myntra_dataset_ByScraping.csv")

#1. Mostrar as 5 primeiras e as 5 últimas linhas do DataFrame. 
head =df.head()
tail =df.tail()

# 2. Exibir o número de linhas e colunas.
n_linhas = df.shape
n_colunas = df.columns

# 3. Listar os nomes das colunas.
nomes_colunas = df.columns

# 4. Mostrar os tipos de dados de cada coluna.
tipos_colunas = df.dtypes

# 5. Usar info() para ver informações gerais.
info = df.info()

# 6. Verifique quais são as marcas (brand_name) que temos na amostra.
marcas = df['brand_name'].unique

# 7. Filtrar produtos com preço entre 1000 e 3000
filtro = df[(df['price'] > 1000) & (df['price'] < 3000)]


# 8. Selecionar as colunas brand_name, pants_description e price em um novo DataFrame chamado df2.
df2 = df[['brand_name', 'pants_description', 'price']]

# 9. Filtrar os produtos da marca Roadster e gravar em um novo df_roadster.
df_roadster = df2[df2['brand_name'] == 'Roadster']

# 10. Verificar valores nulos em cada coluna.
valores_nulos = df.isnull().sum()

# 11. Ordenar os 10 produtos mais caros (price em ordem decrescente).
top_10_caros = df.sort_values(by='price', ascending=False).head(10)

# 12. Qual é o preço médio (mean) dos produtos no dataset?
preco_media = df['price'].mean()

# 13. Qual é o preço mediano (median)?
preco_mediana = df['price'].median()

# 14. Qual é o desvio padrão do preço (std)?
preco_desvio_padrao = df['price'].std()

#15. Mostre o valor mínimo e o valor máximo do desconto (discount_percent).
desconto_min = df['discount_percent'].min()
desconto_max = df['discount_percent'].max()

#16. Quantos produtos estão abaixo do preço médio e quantos estão acima?
abaixo_media = df[df['price'] < preco_media]
n_abaixo = len(abaixo_media)
acima_media = df[df['price'] > preco_media]
n_acima = len(acima_media)

# 17. Adicionar uma nova coluna chamada preco_desconto que multiplica MRP por (1 - discount_percent).
df['preco_desconto'] = df['MRP'] * (1 - df['discount_percent'])

# 18. Remover todos os produtos com ratings menores que 2.0.
df = df[df['ratings'] >= 2.0]

# 19. Excluir a coluna pants_description.
df.drop('pants_description', axis=1)

#20. Agrupar por brand_name e calcular o preço médio (price).
preco_medio_por_marca = df.groupby('brand_name')['price'].mean()


