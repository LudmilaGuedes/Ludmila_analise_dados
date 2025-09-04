import rpy2.robjects as ro
from rpy2.robjects.packages import importr

# Pacote para ler Excel no R
utils = importr("utils")
ro.r('install.packages("readxl", repos="https://cloud.r-project.org")')
readxl = importr("readxl")

# Caminho do arquivo
arquivo =  "C:/Ludmila/faculdade/ProgramacaoAnaliseDados/diferenca salarial agro e ind.xlsx"

# Ler planilha pelo R
ro.r(f'dados <- readxl::read_excel("{arquivo}")')

# Calcular média por setor no R
res = ro.r('aggregate(Rendimento ~ Setor, data = as.data.frame(dados), FUN = mean)')
print(res)


# Criar um DataFrame de exemplo
import pandas as pd
dados = pd.DataFrame({
    'Setor': ['Agro', 'Indústria', 'Agro', 'Indústria', 'Agro', 'Indústria'],
    'Rendimento': [2500, 3200, 2700, 3100, 2600, 3300]
})

# Calcular a média de rendimento por setor
media_por_setor = dados.groupby('Setor')['Rendimento'].mean().reset_index()

print(media_por_setor)
