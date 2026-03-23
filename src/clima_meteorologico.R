# ============================================================
#  FarmTech Solutions — Coleta de Dados Meteorológicos via API
#  API utilizada: Open-Meteo (https://open-meteo.com/)
#  Sem necessidade de chave de API — totalmente gratuita
# ============================================================

# --- Instalação e carregamento dos pacotes necessários -------
pacotes <- c("httr", "jsonlite")
for (p in pacotes) {
  if (!require(p, character.only = TRUE, quietly = TRUE)) {
    install.packages(p, repos = "https://cloud.r-project.org", quiet = TRUE)
    library(p, character.only = TRUE)
  }
}

# --- Entrada da localização pelo usuário ---------------------
separador_simples <- function(char = "-", n = 54) cat(strrep(char, n), "\n")

cat("\n")
separador_simples("=")
cat("   FARMTECH SOLUTIONS — BOLETIM METEOROLÓGICO\n")
separador_simples("=")
cat("\n")
cat("  Informe a localização para consulta:\n\n")

con_in <- file("stdin", open = "r")

cat("  Cidade : ")
cidade_input <- trimws(readLines(con_in, n = 1))
cat("  Estado : ")
estado_input <- trimws(readLines(con_in, n = 1))

close(con_in)

if (nchar(cidade_input) == 0) {
  cat("ERRO: o nome da cidade não pode ser vazio.\n")
  quit(status = 1)
}

CIDADE_LABEL <- if (nchar(estado_input) > 0) {
  paste0(cidade_input, " - ", toupper(estado_input))
} else {
  cidade_input
}

# Busca de nome para geocodificação: "Cidade, Estado, Brazil"
busca_geo <- if (nchar(estado_input) > 0) {
  paste(cidade_input, estado_input, "Brazil", sep = ", ")
} else {
  paste(cidade_input, "Brazil", sep = ", ")
}

# --- Geocodificação via Open-Meteo Geocoding API -------------
cat("\n  Buscando coordenadas para:", CIDADE_LABEL, "...\n")

url_geo <- paste0(
  "https://geocoding-api.open-meteo.com/v1/search",
  "?name=", URLencode(cidade_input),
  "&count=5&language=pt&format=json"
)

resp_geo <- tryCatch(
  GET(url_geo, timeout(15)),
  error = function(e) {
    cat("ERRO: Não foi possível acessar a API de geocodificação.\n")
    cat("Verifique sua conexão com a internet.\n")
    quit(status = 1)
  }
)

if (http_error(resp_geo)) {
  cat("ERRO HTTP na geocodificação:", status_code(resp_geo), "\n")
  quit(status = 1)
}

geo <- fromJSON(content(resp_geo, as = "text", encoding = "UTF-8"))

if (is.null(geo$results) || length(geo$results) == 0) {
  cat("ERRO: Cidade '", cidade_input, "' não encontrada.\n", sep = "")
  cat("Verifique o nome e tente novamente.\n")
  quit(status = 1)
}

resultados <- geo$results

# Filtra resultados com "Brazil" no país, se disponível
brasil_idx <- which(tolower(resultados$country) == "brazil")
if (length(brasil_idx) > 0) {
  resultados <- resultados[brasil_idx, ]
}

# Usa o primeiro resultado
LATITUDE  <- resultados$latitude[1]
LONGITUDE <- resultados$longitude[1]
TIMEZONE  <- if (!is.null(resultados$timezone[1]) && !is.na(resultados$timezone[1])) {
  resultados$timezone[1]
} else {
  "America/Sao_Paulo"
}

# Confirma localização encontrada
nome_encontrado <- resultados$name[1]
estado_encontrado <- if (!is.null(resultados$admin1[1])) resultados$admin1[1] else ""
pais_encontrado   <- if (!is.null(resultados$country[1])) resultados$country[1] else ""

cat("  Localização encontrada:", nome_encontrado)
if (nchar(estado_encontrado) > 0) cat(" —", estado_encontrado)
if (nchar(pais_encontrado)   > 0) cat(" —", pais_encontrado)
cat("\n\n")

# --- Montagem da URL da API Open-Meteo -----------------------
url_api <- paste0(
  "https://api.open-meteo.com/v1/forecast",
  "?latitude=", LATITUDE,
  "&longitude=", LONGITUDE,
  "&current_weather=true",
  "&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,",
  "wind_speed_10m,soil_temperature_0cm,et0_fao_evapotranspiration",
  "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,",
  "wind_speed_10m_max,et0_fao_evapotranspiration",
  "&timezone=", TIMEZONE,
  "&forecast_days=5"
)

# --- Requisição à API ----------------------------------------
cat("Conectando à API meteorológica Open-Meteo...\n")
resposta <- tryCatch(
  GET(url_api, timeout(15)),
  error = function(e) {
    cat("ERRO: Não foi possível conectar à API.\n")
    cat("Verifique sua conexão com a internet.\n")
    cat("Detalhe:", conditionMessage(e), "\n")
    quit(status = 1)
  }
)

if (http_error(resposta)) {
  cat("ERRO HTTP:", status_code(resposta), "\n")
  quit(status = 1)
}

dados <- fromJSON(content(resposta, as = "text", encoding = "UTF-8"))

# --- Função auxiliar: linha separadora -----------------------
separador <- function(char = "-", n = 54) cat(strrep(char, n), "\n")

# ============================================================
#  EXIBIÇÃO DOS DADOS NO TERMINAL
# ============================================================

separador("=")
cat("  Local        :", CIDADE_LABEL, "\n")
cat("  Latitude     :", LATITUDE, "  Longitude:", LONGITUDE, "\n")
cat("  Fuso horário :", TIMEZONE, "\n")
separador()

# --- Tempo atual --------------------------------------------
atual <- dados$current_weather
hora_atual <- format(Sys.time(), "%d/%m/%Y %H:%M")

cat("\n  CONDIÇÕES ATUAIS  (", hora_atual, ")\n")
separador()
cat("  Temperatura         :", atual$temperature, "°C\n")
cat("  Velocidade do vento :", atual$windspeed, "km/h\n")
cat("  Direção do vento    :", atual$winddirection, "°\n")

# Código WMO → descrição em português
interpretar_wmo <- function(codigo) {
  wmo <- list(
    "0"  = "Céu limpo",
    "1"  = "Principalmente limpo",
    "2"  = "Parcialmente nublado",
    "3"  = "Nublado",
    "45" = "Névoa",
    "48" = "Névoa com gelo",
    "51" = "Garoa leve",
    "53" = "Garoa moderada",
    "55" = "Garoa intensa",
    "61" = "Chuva leve",
    "63" = "Chuva moderada",
    "65" = "Chuva forte",
    "71" = "Neve leve",
    "73" = "Neve moderada",
    "75" = "Neve intensa",
    "80" = "Pancadas de chuva leves",
    "81" = "Pancadas de chuva moderadas",
    "82" = "Pancadas de chuva violentas",
    "95" = "Tempestade",
    "96" = "Tempestade com granizo leve",
    "99" = "Tempestade com granizo intenso"
  )
  desc <- wmo[[as.character(codigo)]]
  if (is.null(desc)) "Condição não identificada" else desc
}

cat("  Condição climática  :", interpretar_wmo(atual$weathercode), "\n")
cat("  Período             :", ifelse(atual$is_day == 1, "Dia", "Noite"), "\n")

# --- Previsão dos próximos 5 dias ---------------------------
diario   <- dados$daily
n_dias   <- length(diario$time)

cat("\n")
separador()
cat("  PREVISÃO PARA OS PRÓXIMOS", n_dias, "DIAS\n")
separador()

for (i in seq_len(n_dias)) {
  data_fmt <- format(as.Date(diario$time[i]), "%d/%m/%Y")
  tmax     <- diario$temperature_2m_max[i]
  tmin     <- diario$temperature_2m_min[i]
  chuva    <- diario$precipitation_sum[i]
  vento    <- diario$wind_speed_10m_max[i]
  et0      <- diario$et0_fao_evapotranspiration[i]

  cat("\n  Data               :", data_fmt, "\n")
  cat("  Temp. Máx / Mín    :", tmax, "°C /", tmin, "°C\n")
  cat("  Precipitação total :", chuva, "mm\n")
  cat("  Vento máx.         :", vento, "km/h\n")
  cat("  Evapotransp. (ET0) :", et0, "mm  [referência FAO]\n")

  # Alerta agrícola simples
  if (!is.na(chuva) && chuva > 20) {
    cat("  ** ALERTA: chuva intensa prevista — verificar drenagem **\n")
  }
  if (!is.na(tmax) && tmax > 35) {
    cat("  ** ALERTA: calor extremo — considerar irrigação adicional **\n")
  }
  if (!is.na(et0) && et0 > 6) {
    cat("  ** ALERTA: alta evapotranspiração — monitorar umidade do solo **\n")
  }
  separador(".", 54)
}

# --- Estatísticas do período --------------------------------
tmax_vec <- diario$temperature_2m_max
tmin_vec <- diario$temperature_2m_min
chuva_vec <- diario$precipitation_sum
et0_vec   <- diario$et0_fao_evapotranspiration

cat("\n")
separador("=")
cat("  RESUMO ESTATÍSTICO DO PERÍODO\n")
separador("=")
cat("  Temperatura máxima\n")
cat("    Média   :", round(mean(tmax_vec,  na.rm = TRUE), 1), "°C\n")
cat("    Desvio  :", round(sd(tmax_vec,    na.rm = TRUE), 2), "°C\n")
cat("    Máx/Mín :", max(tmax_vec, na.rm = TRUE), "°C /",
                     min(tmax_vec, na.rm = TRUE), "°C\n")

cat("\n  Temperatura mínima\n")
cat("    Média   :", round(mean(tmin_vec,  na.rm = TRUE), 1), "°C\n")
cat("    Desvio  :", round(sd(tmin_vec,    na.rm = TRUE), 2), "°C\n")

cat("\n  Precipitação acumulada\n")
cat("    Total no período :", round(sum(chuva_vec, na.rm = TRUE), 1), "mm\n")
cat("    Média diária     :", round(mean(chuva_vec, na.rm = TRUE), 1), "mm\n")
cat("    Desvio padrão    :", round(sd(chuva_vec,   na.rm = TRUE), 2), "mm\n")

cat("\n  Evapotranspiração (ET0)\n")
cat("    Total no período :", round(sum(et0_vec, na.rm = TRUE), 1), "mm\n")
cat("    Média diária     :", round(mean(et0_vec, na.rm = TRUE), 1), "mm\n")

cat("\n")
separador("=")
cat("  Fonte: Open-Meteo API (open-meteo.com)\n")
cat("  Modelo: ECMWF IFS — dados atualizados a cada hora\n")
separador("=")
cat("\n")
