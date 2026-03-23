# FIAP — Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP — Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
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

Organização alinhada ao **template FIAP** (`assets`, `config`, `document`, `scripts`, `src`, `.github`). O código-fonte está em **`src/`**; dados exportados em **`config/`**; na raiz existe apenas o atalho **`farm.py`** para execução.

```
farmtech-main/
├── .github/
├── assets/                   # Logo FIAP e demais imagens
├── config/                   # dados_fazenda.csv, insumos_por_talhao.csv (gerados pelo app)
├── document/                 # Documentação complementar e enunciado
├── scripts/
├── src/                      # farm.py, vetor_produtos.py, app.R, módulos R
├── farm.py                   # Atalho → executa src/farm.py
└── README.md
```

---

## Pré-requisitos

| Ferramenta | Versão mínima | Verificar |
|------------|---------------|-----------|
| Python | 3.8+ | `python --version` |
| pandas | qualquer | `pip install pandas` |
| R | 4.0+ | `Rscript --version` |

> Os pacotes R (`dplyr`, `httr`, `jsonlite`) podem ser instalados na primeira execução dos scripts.

---

## Como abrir o projeto

No VS Code ou Cursor: **File → Open Folder** → pasta do repositório. Use o terminal integrado na **raiz** do projeto.

---

## 1. Aplicação Python

### Executar (na raiz do repositório)

```powershell
python farm.py
```

(Equivale a executar `src/farm.py` com o `PYTHONPATH` correto.)

### Menu de opções

| Opção | Descrição |
|-------|-----------|
| 0 | Carregar dados de `config/dados_fazenda.csv` |
| 1 | Inserir dados (talhão, área, cultura, linhas) |
| 2 | Listar dados |
| 3 | Atualizar dados |
| 4 | Excluir dados |
| 5 | Exportar dataframe → `config/dados_fazenda.csv` |
| 6 | Calcular uso de produtos |
| 7 | Calcular insumos por talhão (por metro de linha) |
| 8 | Sistema de Análise R (`src/app.R`) |
| 9 | Sair |

> Use a opção **5** antes de rodar o R para atualizar o CSV.

---

## 2. Sistema R — `src/app.R`

Pode ser aberto pela opção **8** do menu Python ou pelo terminal:

```powershell
Rscript src/app.R
```

### Menu do `app.R`

| Opção | Módulo | Descrição |
|-------|--------|-----------|
| 1 | `analise_estatistica.R` | Estatísticas no CSV em `config/` |
| 2 | `clima_meteorologico.R` | Boletim meteorológico (Open-Meteo) |
| 3 | Sair | Volta ao menu Python |

---

## 3. Módulos R (em `src/`)

```powershell
Rscript src/analise_estatistica.R
Rscript src/clima_meteorologico.R
```

---

## R não está no PATH (Windows)

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\R\R-4.5.2\bin", "Machine")
```

(Ajuste a versão da pasta `R-x.x.x`.)

---

## Fluxo resumido

```
python farm.py
  ├─ Opção 5  → exporta config/dados_fazenda.csv
  ├─ Opção 8  → R (src/app.R)
  └─ Opção 9  → sair
```

---

## Referências

- [Open-Meteo API](https://open-meteo.com/)
- [CRAN](https://cran.r-project.org/)
- Enunciado: `document/instruoces-avaliacao-fase1`
- Desenvolvido por Edemir Sufiatti. 2026-03-18
