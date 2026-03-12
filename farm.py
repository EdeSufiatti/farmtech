import time
import sys
import pandas as pd

def apresentation_animate():
    logo = """
███████╗░█████╗░██████╗░███╗░░░███╗████████╗███████╗░█████╗░██╗░░██╗
██╔════╝██╔══██╗██╔══██╗████╗░████║╚══██╔══╝██╔════╝██╔══██╗██║░░██║
█████╗░░███████║██████╔╝██╔████╔██║░░░██║░░░█████╗░░██║░░╚═╝███████║
██╔══╝░░██╔══██║██╔══██╗██║╚██╔╝██║░░░██║░░░██╔══╝░░██║░░██╗██╔══██║
██║░░░░░██║░░██║██║░░██║██║░╚═╝░██║░░░██║░░░███████╗╚█████╔╝██║░░██║
╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚═╝
 
Bem-vindo ao sistema de gestão agrícola!
 
Aqui você pode gerenciar suas plantações, calcular custos e muito mais. 
 
Para começar, selecione uma das opções abaixo:
"""
    for linha in logo.split("\n"):
        print(linha)
        time.sleep(0.1)

# vetor produtos (mantido conforme original)
produtos = [
    ["Soja","Inseticida","Curbix","Bayer",0.75,"L/ha",320],
    ["Soja","Fungicida","Fox Xpro","Bayer",0.40,"L/ha",280],
    ["Soja","Fertilizante Foliar","Bayfolan","Bayer",2.0,"L/ha",50],
    ["Soja","Inseticida","Pirate","BASF",0.60,"L/ha",290],
    ["Soja","Fungicida","Orkestra","BASF",0.35,"L/ha",300],
    ["Soja","Fertilizante Foliar","Basfoliar Kelp","BASF",2.0,"L/ha",45],
    ["Soja","Inseticida","Engeo Pleno","Syngenta",0.25,"L/ha",340],
    ["Soja","Fungicida","Elatus","Syngenta",0.20,"L/ha",450],
    ["Soja","Fertilizante Foliar","Quantis","Syngenta",2.0,"L/ha",60],
    ["Milho","Inseticida","Belt","Bayer",0.10,"L/ha",950],
    ["Milho","Fungicida","Stratego Pro","Bayer",0.40,"L/ha",240],
    ["Milho","Fertilizante Foliar","Bayfolan","Bayer",2.0,"L/ha",50],
    ["Milho","Inseticida","Fastac","BASF",0.20,"L/ha",190],
    ["Milho","Fungicida","Orkestra","BASF",0.45,"L/ha",300],
    ["Milho","Fertilizante Foliar","Basfoliar 20-20-20","BASF",3.0,"kg/ha",32],
    ["Milho","Inseticida","Ampligo","Syngenta",0.20,"L/ha",380],
    ["Milho","Fungicida","Miravis Neo","Syngenta",0.30,"L/ha",420],
    ["Milho","Fertilizante Foliar","Quantis","Syngenta",2.0,"L/ha",60],
    ["Café","Inseticida","Sivanto Prime","Bayer",0.75,"L/ha",420],
    ["Café","Fungicida","Sphere Max","Bayer",0.60,"L/ha",270],
    ["Café","Fertilizante Foliar","Bayfolan","Bayer",2.0,"L/ha",50],
    ["Café","Inseticida","Fastac","BASF",0.30,"L/ha",190],
    ["Café","Fungicida","Opera","BASF",0.75,"L/ha",250],
    ["Café","Fertilizante Foliar","Basfoliar Zn","BASF",1.5,"L/ha",38],
    ["Café","Inseticida","Actara","Syngenta",0.20,"L/ha",410],
    ["Café","Fungicida","Amistar Top","Syngenta",0.50,"L/ha",300],
    ["Café","Fertilizante Foliar","Quantis","Syngenta",2.0,"L/ha",60],
    ["Trigo","Inseticida","Decis","Bayer",0.20,"L/ha",180],
    ["Trigo","Fungicida","Fox","Bayer",0.50,"L/ha",230],
    ["Trigo","Fertilizante Foliar","Bayfolan","Bayer",2.0,"L/ha",50],
    ["Trigo","Inseticida","Fastac","BASF",0.20,"L/ha",190],
    ["Trigo","Fungicida","Opera","BASF",0.60,"L/ha",250],
    ["Trigo","Fertilizante Foliar","Basfoliar Boro","BASF",1.0,"L/ha",35],
    ["Trigo","Inseticida","Karate Zeon","Syngenta",0.15,"L/ha",210],
    ["Trigo","Fungicida","Trivapro","Syngenta",0.40,"L/ha",320],
    ["Trigo","Fertilizante Foliar","Quantis","Syngenta",2.0,"L/ha",60],
    ["Cana-de-açúcar","Inseticida","Connect","Bayer",1.0,"L/ha",150],
    ["Cana-de-açúcar","Fungicida","Sphere Max","Bayer",0.70,"L/ha",270],
    ["Cana-de-açúcar","Fertilizante Foliar","Bayfolan","Bayer",2.0,"L/ha",50],
    ["Cana-de-açúcar","Inseticida","Fastac","BASF",0.30,"L/ha",190],
    ["Cana-de-açúcar","Fungicida","Opera","BASF",0.75,"L/ha",250],
    ["Cana-de-açúcar","Fertilizante Foliar","Basfoliar Ativ","BASF",2.0,"L/ha",40],
    ["Cana-de-açúcar","Inseticida","Engeo Pleno","Syngenta",0.30,"L/ha",340],
    ["Cana-de-açúcar","Fungicida","Amistar","Syngenta",0.60,"L/ha",290],
    ["Cana-de-açúcar","Fertilizante Foliar","Quantis","Syngenta",2.0,"L/ha",60]
]

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
        except ValueError:
            print("❌ Erro: Digite apenas números inteiros.")


def exportar_dataframe():
    if not dados_talhoes:
        print("\n❌ Não há dados para exportar.")
        return
    df = pd.DataFrame(dados_talhoes)
    df.to_csv("dados_fazenda.csv", index=False, encoding="utf-8")
    print("\n✅ Data Frame exportado com sucesso para 'dados_fazenda.csv'!")
    print("   No R, leia com: df <- read.csv('dados_fazenda.csv')")            

def menu():
    print("""
    1. Inserir Dados
    2. Listar Dados
    3. Atualizar Dados
    4. Excluir Dados
    5. Exportar Dados - Dataframe
    6. Sair
    """)

def option_menu():
    option = input("Escolha uma opção: ")
    
    if option == "1":
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
                talhao = {
                    "cultura": cultura_escolhida,
                    "forma": forma_geometrica,
                    "area_m2": area,
                    "hectares": hectares,
                    "alqueires": alqueires
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
            print(f"Talhão {i+1}: {t['cultura']} | Forma: {t['forma']}")
            print(f"  > Área: {t['area_m2']:,.2f} m²")
            print(f"  > Área: {fmt_hectares(t['hectares'])} | {t['alqueires']:.2f} alqueires")
            print("-" * 60)

    elif option == "3":
        print("\n--- ATUALIZAR DADOS ---")
        if not dados_talhoes:
            print("Nenhum dado cadastrado.")
        else:
            for i, t in enumerate(dados_talhoes):
                print(f"{i}. Cultura: {t['cultura']} | Área: {fmt_hectares(t['hectares'])}")
            try:
                indice = int(input("\nDigite o número do talhão: "))
                if 0 <= indice < len(dados_talhoes):
                    print("1. Cultura | 2. Área")
                    escolha = input("Opção: ")
                    if escolha == "1":
                        nova = menu_culturas()
                        if nova != "Opção inválida":
                            dados_talhoes[indice]['cultura'] = nova
                            print("✅ Cultura atualizada!")
                    elif escolha == "2":
                        print("Exemplo: 0 (Círculo), 3 (Triângulo), 4 (Quadrado), etc.")
                        lados = validar_lados()
                        medidas = capturar_medidas(lados)
                        area = calcular_area(lados, medidas)
                        ha, alq = converter_area(area)
                        dados_talhoes[indice].update({"area_m2": area, "hectares": ha, "alqueires": alq, "forma": identificar_forma(lados)})
                        print("✅ Área atualizada!")
                else: print("❌ Índice inválido.")
            except ValueError: print("❌ Erro de entrada.")

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
        exportar_dataframe()
    elif option == "6":
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
    return (sum(medidas) * medidas[0]) / 4 # Aproximação para polígonos regulares

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