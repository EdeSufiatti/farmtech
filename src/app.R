# ============================================================
#  FarmTech Solutions — Aplicação R Principal
#  Ponto de entrada: chama os módulos via menu interativo
# ============================================================

# --- Localiza o Rscript executável atual --------------------
rscript <- file.path(
  R.home("bin"),
  ifelse(.Platform$OS.type == "windows", "Rscript.exe", "Rscript")
)

# --- Diretório onde está este script ------------------------
script_dir <- tryCatch(
  normalizePath(dirname(sys.frame(1)$ofile)),
  error = function(e) normalizePath(getwd())
)

# --- Funções auxiliares -------------------------------------
separador <- function(char = "-", n = 54) cat(strrep(char, n), "\n")

# Lê uma linha do terminal (abre e fecha conexão a cada leitura
# para não bloquear o stdin dos subprocessos)
ler_linha <- function() {
  con <- file("stdin", open = "r")
  on.exit(close(con), add = TRUE)
  linha <- readLines(con, n = 1)
  if (length(linha) == 0) return("")   # EOF → trata como vazio
  trimws(linha)
}

pausar <- function() {
  cat("\n  Pressione ENTER para voltar ao menu...")
  ler_linha()
  invisible(NULL)
}

# Executa um módulo .R como subprocesso independente
executar_modulo <- function(arquivo) {
  caminho <- file.path(script_dir, arquivo)
  if (!file.exists(caminho)) {
    cat("\n  ERRO: arquivo '", arquivo, "' não encontrado em:\n", sep = "")
    cat("  ", caminho, "\n")
    pausar()
    return(invisible(NULL))
  }
  separador("=")
  system2(rscript, args = shQuote(caminho), wait = TRUE)
  separador("=")
  pausar()
}

# --- Menu principal -----------------------------------------
exibir_menu <- function() {
  cat("\n")
  separador("=")
  cat("    FARMTECH SOLUTIONS — SISTEMA DE ANÁLISE R\n")
  separador("=")
  cat("\n")
  cat("   1. Análise Estatística dos dados da fazenda\n")
  cat("      (lê o CSV exportado pelo sistema Python)\n")
  cat("\n")
  cat("   2. Boletim Meteorológico via API\n")
  cat("      (consulta Open-Meteo por cidade e estado)\n")
  cat("\n")
  cat("   3. Sair\n")
  cat("\n")
  separador()
  cat("   Escolha uma opção [1-3]: ")
}

# --- Loop principal -----------------------------------------
repeat {
  exibir_menu()
  opcao <- ler_linha()

  if (opcao == "1") {
    cat("\n")
    executar_modulo("analise_estatistica.R")

  } else if (opcao == "2") {
    cat("\n")
    executar_modulo("clima_meteorologico.R")

  } else if (opcao %in% c("3", "0", "q", "Q", "sair")) {
    cat("\n")
    separador("=")
    cat("    FarmTech Solutions — Até logo!\n")
    separador("=")
    cat("\n")
    break

  } else if (nchar(opcao) == 0) {
    next  # ENTER em branco → reexibe o menu

  } else {
    cat("\n  Opção inválida. Digite 1, 2 ou 3.\n")
  }
}
