import rpy2.robjects as ro
from rpy2.robjects.packages import importr

# Pacote para ler Excel no R
utils = importr("utils")
ro.r('install.packages("readxl", repos="https://cloud.r-project.org")')
readxl = importr("readxl")

# Caminho do arquivo
arquivo = "C:/Ludmila/faculdade/inferencia_estatistica/diferenca salarial agro e ind.xlsx"

# Ler planilha pelo R
ro.r(f'dados <- readxl::read_excel("{arquivo}")')

# Calcular média por setor no R
res = ro.r('aggregate(Rendimento ~ Setor, data = as.data.frame(dados), FUN = mean)')
print(res)
