import rpy2.robjects as ro
from rpy2.robjects.packages import importr

# Importar pacotes do R
utils = importr("utils")
readxl = importr("readxl")

# Instalar o pacote 'readxl' se necessário
ro.r('if (!require("readxl")) install.packages("readxl", repos="https://cloud.r-project.org")')

# Caminho do arquivo Excel
arquivo = "C:/Ludmila/faculdade/inferencia_estatistica/diferenca salarial agro e ind.xlsx"

# Ler a planilha no R
ro.r(f'dados <- readxl::read_excel("{arquivo}")')

# Calcular média por setor
res = ro.r('aggregate(Rendimento ~ Setor, data = as.data.frame(dados), FUN = mean)')

# Exibir resultado
print(res)
