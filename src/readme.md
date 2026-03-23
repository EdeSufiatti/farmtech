# FIAP — Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP" border="0" width="40%" height="40%"></a>
</p>

<br>

# FarmTech Solutions – Agricultura Digital

Projeto de gestão agrícola (Python + R) – atividade avaliativa FIAP.

Link video no yoytube - não listado
https://youtu.be/zYY6PB0g4Ug

**Repositório:** https://github.com/EdeSufiatti/farmtech

> O repositório está **privado** por orientação da instituição. Será tornado público após a validação pelo professor.

---

## Estrutura do projeto

Organização alinhada ao **template FIAP** (pastas `assets`, `config`, `document`, `scripts`, `src`, `.github`). Os arquivos **Python, R e CSV** permanecem na **raiz** para que os caminhos relativos do código continuem válidos sem alteração.

```
farmtech-main/
├── .github/                  # Modelo de reporte de problemas (template FIAP)
├── assets/                   # Logo e demais imagens
├── config/                   # Parâmetros e ajustes (ver readme interno)
├── document/                 # Documentação e enunciado
│   ├── ai_project_document_fiap.md
│   ├── instruoces-avaliacao-fase1
│   └── other/
├── scripts/                  # Scripts auxiliares (ver readme interno)
├── src/                      # Reservado — readme do template FIAP
├── farm.py                   # Aplicação Python principal (menu interativo)
├── vetor_produtos.py         # Vetor de insumos/produtos agrícolas
├── app.R                     # Menu R principal (ponto de entrada do sistema R)
├── analise_estatistica.R     # Análise estatística dos dados da fazenda
├── clima_meteorologico.R     # Boletim meteorológico via API (Desafio Extra)
├── dados_fazenda.csv         # Gerado pelo Python – entrada para o R
├── insumos_por_talhao.csv    # Gerado automaticamente ao calcular insumos
└── README.md
```

---

## Pré-requisitos

| Ferramenta | Versão mínima | Verificar |
|------------|---------------|-----------|
| Python | 3.8+ | `python --version` |
| pandas | qualquer | instalado com `pip install pandas` |
| R | 4.0+ | `Rscript --version` |

> Os pacotes R (`dplyr`, `httr`, `jsonlite`) são instalados automaticamente na primeira execução de cada script.

---

## Como abrir o projeto

No VS Code ou Cursor: **File → Open Folder** → selecione a pasta do repositório.

Use o **terminal integrado**: `Ctrl+`` ` ou menu **Terminal → New Terminal**.

---

## 1. Aplicação Python — `farm.py`

### Executar

```powershell
python farm.py
```

### Menu de opções

| Opção | Descrição |
|-------|-----------|
| 0 | Carregar dados de `dados_fazenda.csv` (continuar trabalhando) |
| 1 | Inserir dados (talhão: forma geométrica, área, cultura, espaçamento entre linhas) |
| 2 | Listar dados (talhões cadastrados com cálculo de insumos) |
| 3 | Atualizar dados (cultura ou área de um talhão existente) |
| 4 | Excluir dados (remover um talhão) |
| 5 | Exportar dados — dataframe para `dados_fazenda.csv` (entrada para análise no R) |
| 6 | Calcular insumos para talhão — manejo e aplicação por metro de linha |
| 7 | **Sistema de Análise R** (Estatística + Clima — chama `app.R` diretamente) |
| 8 | Sair |

> Use a opção **5** antes de rodar o R para garantir que o CSV está atualizado.

---

## 2. Sistema R — `app.R`

O `app.R` é o ponto de entrada do sistema R, com menu interativo que permite escolher entre os dois módulos disponíveis. Pode ser chamado **diretamente pelo menu Python (opção 7)** ou pelo terminal.

### Executar pelo terminal

```powershell
Rscript app.R
```

Ou, se o R não estiver no PATH:

```powershell
& "C:\Program Files\R\R-4.5.2\bin\Rscript.exe" .\app.R
```

### Menu do `app.R`

| Opção | Módulo chamado | Descrição |
|-------|----------------|-----------|
| 1 | `analise_estatistica.R` | Lê o CSV e calcula média e desvio padrão |
| 2 | `clima_meteorologico.R` | Solicita cidade/estado e exibe boletim meteorológico |
| 3 | — | Sair e voltar ao menu Python |

---

## 3. Módulos R

### `analise_estatistica.R` — Análise Estatística

Lê automaticamente o primeiro `.csv` encontrado na pasta (normalmente `dados_fazenda.csv`) e calcula, para cada coluna numérica:

- **Média**
- **Desvio padrão**

Usa o pacote `dplyr` (instalado automaticamente na primeira execução).

```powershell
Rscript analise_estatistica.R
```

---

### `clima_meteorologico.R` — Boletim Meteorológico *(Desafio Extra)*

Conecta-se à API pública [Open-Meteo](https://open-meteo.com/) (gratuita, sem chave de API) e exibe no terminal:

- Condições climáticas atuais (temperatura, vento, condição do tempo)
- Previsão dos próximos 5 dias (temperatura máx/mín, precipitação, vento, evapotranspiração ET0)
- Alertas agrícolas automáticos (chuva intensa, calor extremo, alta evapotranspiração)
- Resumo estatístico do período (média, desvio padrão, totais)

O script **solicita cidade e estado** antes de consultar a API e geocodifica a localização automaticamente.

Pacotes instalados automaticamente: `httr`, `jsonlite`. Requer conexão com a internet.

```powershell
Rscript clima_meteorologico.R
```

---

## R não está no PATH (Windows)

Se `Rscript` não for reconhecido no terminal, adicione ao PATH:

```powershell
# Executar no PowerShell como Administrador (reinicie o terminal após)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\R\R-4.5.2\bin", "Machine")
```

> Ajuste `R-4.5.2` conforme a versão instalada em `C:\Program Files\R\`.

---

## Fluxo completo de uso

```
python farm.py
  ├─ Opção 1  → cadastrar talhões
  ├─ Opção 5  → exportar dados_fazenda.csv
  ├─ Opção 7  → abre app.R
  │              ├─ Opção 1 → análise estatística do CSV
  │              ├─ Opção 2 → boletim meteorológico (digita cidade/estado)
  │              └─ Opção 3 → volta ao menu Python
  └─ Opção 8  → sair
```

---

## Referências

- [Open-Meteo API](https://open-meteo.com/) – dados meteorológicos gratuitos
- [CRAN – The Comprehensive R Archive Network](https://cran.r-project.org/)
- Enunciado completo: `document/instruoces-avaliacao-fase1`
- Desenvolvido por Edemir Sufiatti. 2026-03-18
