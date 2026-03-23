import time
import sys
import os
import glob
import shutil
import subprocess
import pandas as pd
from vetor_produtos import produtos

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
_CONFIG_DIR = os.path.join(_PROJECT_ROOT, "config")
ARQUIVO_DADOS = os.path.join(_CONFIG_DIR, "dados_fazenda.csv")
ARQUIVO_INSUMOS = os.path.join(_CONFIG_DIR, "insumos_por_talhao.csv")


def _ensure_utf8_stdio():
    """Evita UnicodeEncodeError no Windows (cp1252) ao imprimir emojis e acentos."""
    for stream in (sys.stdout, sys.stderr):
        try:
            if stream and hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_utf8_stdio()

clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')
def apresentation_animate():
    logo = """
    

🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱
███████╗░█████╗░██████╗░███╗░░░███╗████████╗███████╗░█████╗░██╗░░██╗
██╔════╝██╔══██╗██╔══██╗████╗░████║╚══██╔══╝██╔════╝██╔══██╗██║░░██║
█████╗░░███████║██████╔╝██╔████╔██║░░░██║░░░█████╗░░██║░░╚═╝███████║
██╔══╝░░██╔══██║██╔══██╗██║╚██╔╝██║░░░██║░░░██╔══╝░░██║░░██╗██╔══██║
██║░░░░░██║░░██║██║░░██║██║░╚═╝░██║░░░██║░░░███████╗╚█████╔╝██║░░██║
╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚═╝
🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱🌱

 
Bem-vindo ao sistema de gestão agrícola! 🌱
 
Aqui você pode gerenciar suas plantações, calcular custos e muito mais. 
 
Para começar, selecione uma das opções abaixo:
"""
    for linha in logo.split("\n"):
        print(linha)
        time.sleep(0.010)



dados_talhoes = []
def validar_lados():
    """Esta é a função que usa a expressão lógica para validar a entrada"""
    while True:
        try:
            lados = int(input("Numero de lados (0 para círculo, ou 3 a 8): "))
            # A EXPRESSÃO LÓGICA VAI AQUI:
            if lados == 0 or 3 <= lados <= 8:
                return lados
            else:
                print("❌ Erro: Forma geométrica não suportada. Escolha 0 ou entre 3 e 8.")
                continue
        except ValueError:
            print("❌ Erro: Digite apenas números inteiros.")
            continue


def dimensao_para_linhas(lados, medidas):
    """
    Obtém a dimensão do talhão (em m) para cálculo do número de linhas,
    usando os dados já informados: número de lados e medidas.
    - Círculo: diâmetro (2 × raio)
    - Triângulo/Quadrilátero/Polígono: menor lado (faixa onde as linhas se distribuem)
    """
    if lados == 0:
        return 2 * medidas[0]  # diâmetro
    return min(medidas)  # menor lado

def comprimento_linha(lados, medidas):
    """
    Comprimento da linha/rua (m) para cálculo de pulverização por metro.
    - Círculo: diâmetro (2 × raio)
    - Polígono: maior lado (comprimento da ruas)
    """
    if lados == 0:
        return 2 * medidas[0]
    return max(medidas)

def solicitar_linhas_plantio(lados, medidas):
    """
    Solicita apenas o espaçamento entre linhas. A dimensão do talhão é obtida
    dos dados já informados (lados e medidas). Fórmula: num_linhas = dimensão / espaçamento.
    """
    dimensao = dimensao_para_linhas(lados, medidas)
    while True:
        try:
            espacamento = float(input("Espaçamento entre linhas de plantio (m): ").replace(",", "."))
            if espacamento <= 0:
                print("❌ Espaçamento deve ser maior que zero.")
                continue
            num_linhas = int(round(dimensao / espacamento))
            if num_linhas < 1:
                num_linhas = 1
            return espacamento, dimensao, num_linhas
        except ValueError:
            print("❌ Digite um valor numérico válido (ex.: 0.5).")

def calcular_insumos_talhao(cultura, hectares):
    """
    Calcula quantidade de insumo e custo por marca. Para cada tipo (Inseticida, Fungicida, etc.),
    as marcas são concorrentes: exibe custo/ha e custo total e indica qual marca tem
    melhor custo-benefício (menor custo total para a área).
    Custo por ha = dose × preço (unidade); Custo total = hectares × custo por ha.
    """
    produtos_cultura = [p for p in produtos if p[0] == cultura]
    if not produtos_cultura:
        print(f"  Nenhum insumo cadastrado para {cultura}.")
        return
    print(f"\n--- Manejo de insumos para {cultura} ({fmt_hectares(hectares)}) ---")
    # Agrupar por tipo (Inseticida, Fungicida, Fertilizante Foliar)
    tipos = {}
    for p in produtos_cultura:
        tipo = p[1]
        if tipo not in tipos:
            tipos[tipo] = []
        tipos[tipo].append(p)
    for tipo, lista_p in tipos.items():
        print(f"\n  [{tipo}]")
        # Calcular para cada produto: quantidade, custo/ha, custo total
        opcoes = []
        for p in lista_p:
            nome_produto, fabricante, dose, unidade_ha, preco = p[2], p[3], p[4], p[5], p[6]
            quantidade_total = hectares * dose
            unidade_total = "L" if unidade_ha == "L/ha" else "kg"
            custo_ha = dose * preco
            custo_total = hectares * custo_ha
            opcoes.append((nome_produto, fabricante, dose, unidade_ha, quantidade_total, unidade_total, custo_ha, custo_total))
        # Melhor custo-benefício = menor custo total
        melhor_idx = min(range(len(opcoes)), key=lambda i: opcoes[i][7])
        for i, (nome, fab, dose, un_ha, qtd, un_tot, c_ha, c_total) in enumerate(opcoes):
            destaque = " ← MELHOR CUSTO-BENEFÍCIO" if i == melhor_idx else ""
            print(f"    {nome} ({fab}): {dose} {un_ha} → {qtd:.2f} {un_tot} | R$ {c_ha:.2f}/ha | Total: R$ {c_total:.2f}{destaque}")
    print()

def dose_ha_para_por_metro(dose_por_ha, unidade_ha, espacamento_m):
    """
    Converte dose por hectare (L/ha ou kg/ha) para por metro de linha.
    Relação: 1 ha = 10.000 m²; com espaçamento E, há 10.000/E metros lineares de linha.
    Logo: mL/m = (L/ha × 1000) / (10.000/E) = L/ha × E / 10  →  kg/m = kg/ha × E / 10.000
    """
    metros_linha_por_ha = 10000 / espacamento_m
    if unidade_ha == "L/ha":
        return (dose_por_ha * 1000) / metros_linha_por_ha  # mL por metro
    return dose_por_ha / metros_linha_por_ha  # kg por metro

def calcular_pulverizacao_por_metro(talhao):
    """
    Calcula aplicação por metro de linha a partir do vetor de produtos (dose L/ha ou kg/ha)
    e do espaçamento do talhão. Fórmula: mL/m = (L/ha × espacamento) / 10.
    Total necessário = ruas × comprimento da linha × (mL/m ÷ 1000) ou × kg/m.
    """
    num_linhas = talhao.get("num_linhas")
    comp_linha = talhao.get("comprimento_linha")
    espacamento = talhao.get("espacamento_linhas")
    cultura = talhao.get("cultura")
    if num_linhas is None or comp_linha is None or espacamento is None:
        return
    produtos_cultura = [p for p in produtos if p[0] == cultura]
    if not produtos_cultura:
        return
    print("--- Pulverização por metro de linha (a partir do vetor de produtos: L/ha × espaçamento) ---")
    print(f"  Ruas: {num_linhas}  |  Comprimento da linha: {comp_linha:.1f} m  |  Espaçamento: {espacamento} m")
    print(f"  Fórmula: mL/m = (L/ha × espaçamento) / 10  →  Total L = ruas × compr. × (mL/m ÷ 1000)\n")
    for p in produtos_cultura:
        nome, fabricante, dose, unidade_ha = p[2], p[3], p[4], p[5]
        por_metro = dose_ha_para_por_metro(dose, unidade_ha, espacamento)
        if unidade_ha == "L/ha":
            total = num_linhas * comp_linha * (por_metro / 1000)
            print(f"  {nome} ({fabricante}): {dose} {unidade_ha} → {por_metro:.2f} mL/m  →  Total: {total:,.2f} L")
        else:
            total = num_linhas * comp_linha * por_metro
            print(f"  {nome} ({fabricante}): {dose} {unidade_ha} → {por_metro:.4f} kg/m  →  Total: {total:,.2f} kg")
    exportar_insumos_por_talhao()

def exportar_insumos_por_talhao(silencioso=False):
    """
    Gera insumos_por_talhao.csv com um registro por (talhão, produto): quantidade, custo e
    aplicação por metro (mL/m ou kg/m e total L ou kg). Chamado logo após o cálculo de insumos.
    """
    if not dados_talhoes:
        return
    linhas = []
    for idx, t in enumerate(dados_talhoes):
        cultura = t["cultura"]
        hectares = t["hectares"]
        num_linhas = t.get("num_linhas")
        comp_linha = t.get("comprimento_linha")
        espacamento = t.get("espacamento_linhas")
        for p in produtos:
            if p[0] != cultura:
                continue
            cultura_p, tipo, nome, fabricante, dose, unidade_ha, preco = p[0], p[1], p[2], p[3], p[4], p[5], p[6]
            qtd = hectares * dose
            custo_ha = dose * preco
            custo_total = hectares * custo_ha
            unidade_tot = "L" if unidade_ha == "L/ha" else "kg"
            row = {
                "talhao": idx + 1,
                "cultura": cultura,
                "hectares": round(hectares, 4),
                "produto": nome,
                "fabricante": fabricante,
                "tipo": tipo,
                "dose": dose,
                "unidade_ha": unidade_ha,
                "quantidade_total": round(qtd, 4),
                "unidade_qtd": unidade_tot,
                "custo_ha": round(custo_ha, 2),
                "custo_total": round(custo_total, 2),
            }
            if num_linhas is not None and comp_linha is not None and espacamento is not None:
                por_metro = dose_ha_para_por_metro(dose, unidade_ha, espacamento)
                if unidade_ha == "L/ha":
                    total_apl = num_linhas * comp_linha * (por_metro / 1000)
                    row["por_metro"] = round(por_metro, 4)
                else:
                    total_apl = num_linhas * comp_linha * por_metro
                    row["por_metro"] = round(por_metro, 6)
                row["total_aplicacao"] = round(total_apl, 4)
                row["unidade_aplicacao"] = "L" if unidade_ha == "L/ha" else "kg"
            else:
                row["por_metro"] = None
                row["total_aplicacao"] = None
                row["unidade_aplicacao"] = None
            linhas.append(row)
    if not linhas:
        return
    df = pd.DataFrame(linhas)
    os.makedirs(_CONFIG_DIR, exist_ok=True)
    df.to_csv(ARQUIVO_INSUMOS, index=False, encoding="utf-8")
    if not silencioso:
        print("  📄 Atualizado: config/insumos_por_talhao.csv")

def forma_para_lados(forma):
    """Mapeia nome da forma para número de lados (0 = círculo)."""
    mapa = {"Círculo": 0, "Triângulo": 3, "Quadrilátero": 4, "Pentágono": 5,
            "Hexágono": 6, "Heptágono": 7, "Octógono": 8}
    return mapa.get(forma, 4)  # default quadrilátero

def carregar_dados_csv():
    """
    Carrega dados de dados_fazenda.csv para dados_talhoes.
    Permite retomar trabalho com dados exportados anteriormente.
    """
    global dados_talhoes
    arquivo = ARQUIVO_DADOS
    if not os.path.exists(arquivo):
        print(f"\n❌ Arquivo não encontrado: config/dados_fazenda.csv")
        print("   Exporte os dados primeiro (opção 5) ou insira dados manualmente (opção 1).")
        return
    try:
        df = pd.read_csv(arquivo, encoding="utf-8")
        if df.empty:
            print("\n❌ O arquivo está vazio.")
            return
        colunas_esperadas = ["cultura", "forma", "area_m2", "hectares", "alqueires"]
        for col in colunas_esperadas:
            if col not in df.columns:
                print(f"\n❌ Coluna obrigatória '{col}' não encontrada no CSV.")
                return
        dados_talhoes.clear()
        for _, row in df.iterrows():
            forma = str(row["forma"]).strip()
            area_m2 = float(row["area_m2"])
            lados = forma_para_lados(forma)
            # Inferir medidas: círculo usa raio; quadrilátero usa dimensao/comprimento se disponíveis
            if lados == 0:
                raio = (area_m2 / 3.1416) ** 0.5
                medidas = [raio]
            elif lados == 4 and pd.notna(row.get("dimensao_linhas")) and pd.notna(row.get("comprimento_linha")):
                dim = float(row["dimensao_linhas"])
                comp = float(row["comprimento_linha"])
                medidas = [dim, comp]
            else:
                lado_aprox = (area_m2) ** 0.5
                medidas = [lado_aprox] * max(lados, 1)
            talhao = {
                "cultura": str(row["cultura"]).strip(),
                "forma": forma,
                "area_m2": area_m2,
                "hectares": float(row["hectares"]),
                "alqueires": float(row["alqueires"]),
                "lados": lados,
                "medidas": medidas,
                "espacamento_linhas": float(row["espacamento_linhas"]) if pd.notna(row.get("espacamento_linhas")) else None,
                "dimensao_linhas": float(row["dimensao_linhas"]) if pd.notna(row.get("dimensao_linhas")) else None,
                "num_linhas": int(row["num_linhas"]) if pd.notna(row.get("num_linhas")) else None,
                "comprimento_linha": float(row["comprimento_linha"]) if pd.notna(row.get("comprimento_linha")) else None,
            }
            dados_talhoes.append(talhao)
        print(f"\n✅ {len(dados_talhoes)} talhão(ões) carregado(s) de config/dados_fazenda.csv!")
        exportar_insumos_por_talhao(silencioso=True)
    except Exception as e:
        print(f"\n❌ Erro ao carregar CSV: {e}")

def calcular_uso_produtos():
    """
    Calcula e exibe o uso total de produtos (insumos) para todos os talhões cadastrados.
    Agrupa por produto e soma quantidades e custos.
    """
    if not dados_talhoes:
        print("\n❌ Nenhum talhão cadastrado. Insira dados primeiro (opção 1).")
        return
    # Agregar por (cultura, tipo, nome, fabricante): quantidade total, custo total
    uso = {}  # chave: (cultura, tipo, nome, fab) -> (qtd, unidade, custo_total)
    for t in dados_talhoes:
        cultura, hectares = t["cultura"], t["hectares"]
        for p in produtos:
            if p[0] != cultura:
                continue
            cultura_p, tipo, nome, fabricante, dose, unidade_ha, preco = p[0], p[1], p[2], p[3], p[4], p[5], p[6]
            qtd = hectares * dose
            custo_total = hectares * dose * preco
            unidade = "L" if unidade_ha == "L/ha" else "kg"
            chave = (cultura, tipo, nome, fabricante)
            if chave not in uso:
                uso[chave] = [0.0, unidade, 0.0]
            uso[chave][0] += qtd
            uso[chave][2] += custo_total
    print("\n" + "="*60)
    print(f"{'--- USO DE PRODUTOS (TODOS OS TALHÕES) ---':^60}")
    print("="*60)
    # Agrupar por cultura e tipo
    culturas_ordem = []
    for t in dados_talhoes:
        if t["cultura"] not in culturas_ordem:
            culturas_ordem.append(t["cultura"])
    for cultura in culturas_ordem:
        itens = [(k, v) for k, v in uso.items() if k[0] == cultura]
        if not itens:
            continue
        ha_total = sum(t["hectares"] for t in dados_talhoes if t["cultura"] == cultura)
        print(f"\n  [{cultura}] — {fmt_hectares(ha_total)} total")
        tipos_vistos = set()
        for (c, tipo, nome, fab), (qtd, un, custo) in sorted(itens, key=lambda x: (x[0][1], x[0][2])):
            if tipo not in tipos_vistos:
                tipos_vistos.add(tipo)
                print(f"    [{tipo}]")
            print(f"      {nome} ({fab}): {qtd:,.2f} {un} | Custo total: R$ {custo:,.2f}")
    print("\n" + "="*60)
    exportar_insumos_por_talhao()

def exportar_dataframe():
    """
    Única função que gera dados_fazenda.csv. Chamada somente pela opção 5 (Exportar Dados).
    Exporta os talhões para CSV com colunas adequadas ao DataFrame e ao R.
    Inclui: cultura, forma, área (m², ha, alq), linhas de plantio (espaçamento, dimensão, número).
    Não inclui listas (ex.: medidas) para manter o CSV limpo.
    """
    if not dados_talhoes:
        print("\n❌ Não há dados para exportar.")
        return
    colunas = [
        "cultura", "forma", "area_m2", "hectares", "alqueires",
        "espacamento_linhas", "dimensao_linhas", "num_linhas", "comprimento_linha"
    ]
    linhas = []
    for t in dados_talhoes:
        linhas.append({
            "cultura": t["cultura"],
            "forma": t["forma"],
            "area_m2": t["area_m2"],
            "hectares": t["hectares"],
            "alqueires": t["alqueires"],
            "espacamento_linhas": t.get("espacamento_linhas"),
            "dimensao_linhas": t.get("dimensao_linhas"),
            "num_linhas": t.get("num_linhas"),
            "comprimento_linha": t.get("comprimento_linha"),
        })
    df = pd.DataFrame(linhas, columns=colunas)
    os.makedirs(_CONFIG_DIR, exist_ok=True)
    df.to_csv(ARQUIVO_DADOS, index=False, encoding="utf-8")
    print("\n✅ Data Frame exportado com sucesso para config/dados_fazenda.csv!")
    print("   Colunas:", ", ".join(colunas))
    print("   No R: df <- read.csv('config/dados_fazenda.csv')")            

def encontrar_rscript():
    """Localiza o executável Rscript: tenta PATH primeiro, depois caminhos padrão do Windows."""
    caminho = shutil.which("Rscript") or shutil.which("Rscript.exe")
    if caminho:
        return caminho
    for padrao in [
        r"C:\Program Files\R\R-*\bin\Rscript.exe",
        r"C:\Program Files (x86)\R\R-*\bin\Rscript.exe",
    ]:
        encontrados = sorted(glob.glob(padrao))
        if encontrados:
            return encontrados[-1]  # versão mais recente
    return None


def menu():
    print("""
    0. Carregar dados de dados_fazenda.csv
    1. Inserir Dados
    2. Listar Dados
    3. Atualizar Dados
    4. Excluir Dados
    5. Exportar Dados - Dataframe
    6. Calcular uso de produtos
    7. Calcular Insumos para Talhão - Aplicação por L metro de linha
    8. Sistema de Análise R (Estatística + Clima)
    9. Sair
    """)

def option_menu():
    option = input("Escolha uma opção: ")
    
    if option == "0":
        carregar_dados_csv()
    elif option == "1":
        print("\nInsira o numero de lados do talhão\nExemplo: 0 (Círculo), 3 (Triângulo), 4 (Quadrado), etc.")
        try:
            lados = validar_lados()
            forma_geometrica = identificar_forma(lados)
            print(f"Forma Geometrica: {forma_geometrica}")
            medidas = capturar_medidas(lados)
            area = calcular_area(lados, medidas)
            hectares, alqueires = converter_area(area)
            
            print(f"Área Calculada: {area:,.2f} m²")
            print(f"Área: {fmt_hectares(hectares)} | {alqueires:.2f} alq")
            
            cultura_escolhida = menu_culturas()

            if cultura_escolhida != "Opção inválida":
                print(f"\nLinhas de plantio (dimensão do talhão: {dimensao_para_linhas(lados, medidas):.1f} m, a partir dos lados já informados)")
                espacamento, dimensao, num_linhas = solicitar_linhas_plantio(lados, medidas)
                comp_linha = comprimento_linha(lados, medidas)
                print(f"  → {num_linhas} linhas (ruas) no talhão | Comprimento da linha: {comp_linha:.1f} m")
                talhao = {
                    "cultura": cultura_escolhida,
                    "forma": forma_geometrica,
                    "area_m2": area,
                    "hectares": hectares,
                    "alqueires": alqueires,
                    "lados": lados,
                    "medidas": medidas,
                    "espacamento_linhas": espacamento,
                    "dimensao_linhas": dimensao,
                    "num_linhas": num_linhas,
                    "comprimento_linha": comp_linha
                }
                dados_talhoes.append(talhao)
                print("\n✅ Dados gravados com sucesso!")
            else:
                print("\n❌ Erro: Cultura inválida.")
        except ValueError as e:
            print(f"❌ Erro: {e}")

    elif option == "2":
        print("\n" + "="*60)
        print(f"{'--- LISTAR DADOS ---':^60}")
        print("="*60)
        if not dados_talhoes:
            print(f"{'Nenhum dado cadastrado.':^60}")
        for i, t in enumerate(dados_talhoes):
            print(f"\nTalhão {i+1}: {t['cultura']} | Forma: {t['forma']}")
            print(f"  > Área: {t['area_m2']:,.2f} m²")
            print(f"  > Área: {fmt_hectares(t['hectares'])} | {t['alqueires']:.2f} alqueires")
            if "num_linhas" in t:
                print(f"  > Linhas de plantio: {t['num_linhas']} ruas (espaçamento {t['espacamento_linhas']} m)")
                if "comprimento_linha" in t:
                    print(f"  > Comprimento da linha (rua): {t['comprimento_linha']:.1f} m")
            print("-" * 60)

    elif option == "3":
        print("\n--- ATUALIZAR DADOS ---")
        if not dados_talhoes:
            print("Nenhum dado cadastrado.")
        else:
            print("\nTalhões cadastrados — escolha o número do talhão que deseja atualizar:\n")
            for i, t in enumerate(dados_talhoes):
                print(f"  {i}. {t['cultura']} | Forma: {t['forma']} | Área: {fmt_hectares(t['hectares'])}")
            print()
            try:
                indice = int(input("Digite o número do talhão: "))
                if 0 <= indice < len(dados_talhoes):
                    print("1. Cultura | 2. Área")
                    escolha = input("Opção: ")
                    if escolha == "1":
                        nova = menu_culturas()
                        if nova != "Opção inválida":
                            dados_talhoes[indice]['cultura'] = nova
                            print("✅ Cultura atualizada.")
                    elif escolha == "2":
                        lados = validar_lados()
                        medidas = capturar_medidas(lados)
                        area = calcular_area(lados, medidas)
                        ha, alq = converter_area(area)
                        dados_talhoes[indice].update({"area_m2": area, "hectares": ha, "alqueires": alq, "forma": identificar_forma(lados), "lados": lados, "medidas": medidas})
                        espacamento, dimensao, num_linhas = solicitar_linhas_plantio(lados, medidas)
                        comp_linha = comprimento_linha(lados, medidas)
                        dados_talhoes[indice]["espacamento_linhas"] = espacamento
                        dados_talhoes[indice]["dimensao_linhas"] = dimensao
                        dados_talhoes[indice]["num_linhas"] = num_linhas
                        dados_talhoes[indice]["comprimento_linha"] = comp_linha
                        print("✅ Área atualizada.")
                else:
                    print("❌ Índice inválido.")
            except ValueError:
                print("❌ Erro de entrada.")

    elif option == "4":
        print("\n--- EXCLUIR DADOS ---")
        if not dados_talhoes:
            print("Nenhum dado cadastrado.")
        else:
            for i, t in enumerate(dados_talhoes):
                print(f"{i}. {t['cultura']} ({fmt_hectares(t['hectares'])})")
            try:
                indice = int(input("\nÍndice para excluir: "))
                if 0 <= indice < len(dados_talhoes):
                    confirmar = input(f"Confirmar exclusão de {dados_talhoes[indice]['cultura']}? (S/N): ").upper()
                    if confirmar == 'S':
                        removido = dados_talhoes.pop(indice)
                        print(f"✅ {removido['cultura']} removido!")
                else: print("❌ Não encontrado.")
            except ValueError: print("❌ Erro de entrada.")

    elif option == "5":
        # Único momento em que dados_fazenda.csv é gerado
        exportar_dataframe()
    elif option == "6":
        calcular_uso_produtos()
    elif option == "7":
        print("\n--- CALCULAR INSUMOS PARA TALHÃO ---")
        if not dados_talhoes:
            print("Nenhum talhão cadastrado. Insira dados primeiro (opção 1).")
        else:
            for i, t in enumerate(dados_talhoes):
                print(f"{i}. {t['cultura']} ({fmt_hectares(t['hectares'])})")
            try:
                idx = int(input("\nNúmero do talhão: "))
                if 0 <= idx < len(dados_talhoes):
                    t = dados_talhoes[idx]
                    calcular_insumos_talhao(t['cultura'], t['hectares'])
                    calcular_pulverizacao_por_metro(t)
                else:
                    print("❌ Índice inválido.")
            except ValueError:
                print("❌ Erro de entrada.")

    elif option == "8":
        rscript = encontrar_rscript()
        if not rscript:
            print("\n❌ R não encontrado no sistema.")
            print("   Instale em: https://cran.r-project.org/")
            print("   Ou adicione o caminho do Rscript ao PATH do Windows.")
        else:
            script_dir = _SCRIPT_DIR
            app_r = os.path.join(script_dir, "app.R")
            if not os.path.exists(app_r):
                print(f"\n❌ app.R não encontrado em: {app_r}")
            else:
                print("\n" + "="*60)
                print(f"{'Iniciando Sistema de Análise R...':^60}")
                print("="*60)
                subprocess.run([rscript, app_r], cwd=script_dir)
                print("\n" + "="*60)
                print(f"{'Retornando ao menu Python':^60}")
                print("="*60)

    elif option == "9":
        print("Saindo do sistema...")
        sys.exit()

    else:
        print("Opção inválida")

def identificar_forma(lados):
    formas = {0: "Círculo", 3: "Triângulo", 4: "Quadrilátero", 5: "Pentágono", 6: "Hexágono", 7: "Heptágono", 8: "Octógono"}
    return formas.get(lados, "Forma não identificada")

def validar_triangulo(medidas):
    """Verifica se os três lados formam um triângulo (desigualdade triangular)."""
    a, b, c = medidas[0], medidas[1], medidas[2]
    return a + b > c and a + c > b and b + c > a

def capturar_medidas(lados):
    if lados == 0:
        return [float(input("Raio (m): "))]
    return [float(input(f"Lado {i+1} (m): ")) for i in range(lados)]

def calcular_area(lados, medidas):
    if lados == 0: return 3.1416 * (medidas[0] ** 2)
    if lados == 3:
        if not validar_triangulo(medidas):
            raise ValueError("Triângulo inválido: a soma de dois lados deve ser maior que o terceiro.")
        s = sum(medidas) / 2
        radicando = s * (s - medidas[0]) * (s - medidas[1]) * (s - medidas[2])
        if radicando < 0:
            raise ValueError("Triângulo inválido: as medidas não formam um triângulo.")
        return radicando ** 0.5
    if lados == 4: return medidas[0] * medidas[1]
    # Aproximação para polígono regular: (perímetro × apótema)/2 ≈ (soma dos lados × lado)/4
    # Para polígonos irregulares o valor é apenas estimativo.
    return (sum(medidas) * medidas[0]) / 4

def converter_area(area_m2):
    return area_m2 / 10000, area_m2 / 24200

def fmt_hectares(hectares):
    """Formata hectares: número redondo quando inteiro, com 'ha' no fim."""
    h = hectares.real if isinstance(hectares, complex) else hectares
    if h == int(h):
        return f"{int(h)} ha"
    return f"{h:.2f} ha"

def menu_culturas():
    culturas = {"1": "Soja", "2": "Milho", "3": "Café", "4": "Trigo", "5": "Cana-de-açúcar"}
    print("\n".join([f"{k}. {v}" for k, v in culturas.items()]))
    return culturas.get(input("Escolha a cultura: "), "Opção inválida")

def main():
    apresentation_animate()
    while True:
        menu()
        option_menu()

if __name__ == "__main__":
    main()