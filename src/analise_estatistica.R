# Instalar e carregar o pacote dplyr para manipulação de dados
# esta etapa não está concluida, projeto em vscode 
# esrtuturar readme.md com instruções de execução para instalação do pacote dplyr
# estrutura também no readme.md com instruções de execução do código em python

# mover o que está em readme.md para arquivo instruções-atividade-fase1.md

if (!require("dplyr")) install.packages("dplyr")
library(dplyr)

# 1. Pasta config/ na raiz do projeto (template FIAP)
args <- commandArgs(trailingOnly = FALSE)
fa <- grep("^--file=", args, value = TRUE)
script_dir <- if (length(fa)) {
  dirname(normalizePath(sub("^--file=", "", fa[1])))
} else {
  normalizePath(getwd())
}
proj_root <- normalizePath(file.path(script_dir, ".."))
config_dir <- file.path(proj_root, "config")
candidato <- file.path(config_dir, "dados_fazenda.csv")
if (file.exists(candidato)) {
  nome <- candidato
} else {
  arquivos <- list.files(config_dir, pattern = "\\.csv$", full.names = TRUE)
  if (length(arquivos) == 0) stop("Nenhum .csv em config/. Exporte pelo Python (opção 5).")
  nome <- arquivos[1]
}

# 2. Ler o CSV
dados <- read.csv(nome)

# 3. Selecionar só colunas numéricas e calcular Média e Desvio padrão (summarize, como no curso)
medias <- dados %>%
  select(where(is.numeric)) %>%
  summarise(across(everything(), ~ round(mean(., na.rm = TRUE), 2)))

desvios <- dados %>%
  select(where(is.numeric)) %>%
  summarise(across(everything(), ~ round(sd(., na.rm = TRUE), 2)))

# 4. Mostrar nome do arquivo e resultados
cat("Arquivo:", nome, "\n\n")
cat("Média:\n")
print(medias)
cat("\nDesvio padrão:\n")
print(desvios)
