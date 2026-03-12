import time

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
        time.sleep(0.2)

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

def menu():
    print("""
    1. Inserir Dados
    2. Listar Dados
    3. Atualizar Dados
    4. Excluir Dados
    5. Sair
    """)

def option_menu():
    option = input("Escolha uma opção: ")
    
    if option == "1":
        print("Insira o numero de lados do talhão\n Exemplo:0 para circulo, 3 para triângulo, 4 para quadrado, 5 para pentágono, 6 para hexágono, 7 para heptágono, 8 para octógono")
        lados = int(input("Numero de lados: "))
        forma_geometrica = identificar_forma(lados)
        print(f"Forma Geometrica: {forma_geometrica}")
        medidas = capturar_medidas(lados)
        print(f"Medidas: {medidas}")
        area = calcular_area(lados, medidas)
        print(f"Área: {area} m²")
        print("Area em hectares e alqueires")
        hectares, alqueires = converter_area(area)
        print(f"Área: {hectares} hectares")
        print(f"Área: {alqueires:.2f} alqueires")   
        
        cultura_escolhida = menu_culturas()
        print(f"Cultura Selecionada: {cultura_escolhida}")

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
            print("\n❌ Erro: Cultura inválida. Dados não foram salvos.")

    elif option == "2":
        print("\n" + "="*60)
        print(f"{'--- LISTAR DADOS ---':^60}")
        print("="*60)
        if not dados_talhoes:
            print(f"{'Nenhum dado cadastrado.':^60}")
        for i, t in enumerate(dados_talhoes):
            print(f"Talhão {i+1}: {t['cultura']} | Forma: {t['forma']}")
            print(f"  > Área: {t['area_m2']:,.2f} m²")
            print(f"  > Área: {t['hectares']:.4f} hectares")
            print(f"  > Área: {t['alqueires']:.2f} alqueires")
            print("-" * 60)

    elif option == "3":
        print("\n--- ATUALIZAR DADOS ---")
        if not dados_talhoes:
            print("Nenhum dado cadastrado para atualizar.")
        else:
            for i, t in enumerate(dados_talhoes):
                print(f"{i}. Cultura: {t['cultura']} | Área: {t['hectares']:.4f} ha")
            
            try:
                indice = int(input("\nDigite o número do talhão que deseja atualizar: "))
                
                if 0 <= indice < len(dados_talhoes):
                    print("O que deseja alterar?")
                    print("1. Cultura")
                    print("2. Medidas (Área)")
                    escolha = input("Opção: ")
                    
                    if escolha == "1":
                        nova_cultura = menu_culturas()
                        if nova_cultura != "Opção inválida":
                            dados_talhoes[indice]['cultura'] = nova_cultura
                            print("✅ Cultura atualizada com sucesso!")
                        else:
                            print("❌ Opção inválida. Nada foi alterado.")
                            
                    elif escolha == "2":
                        lados = int(input("Novo número de lados: "))
                        forma = identificar_forma(lados)
                        medidas = capturar_medidas(lados)
                        area = calcular_area(lados, medidas)
                        ha, alq = converter_area(area)
                        
                        dados_talhoes[indice]['forma'] = forma
                        dados_talhoes[indice]['area_m2'] = area
                        dados_talhoes[indice]['hectares'] = ha
                        dados_talhoes[indice]['alqueires'] = alq
                        print(f"✅ Área atualizada: {ha:.4f} ha | {alq:.2f} alq!")
                    else:
                        print("Opção inválida.")
                else:
                    print("❌ Índice não encontrado.")
            except ValueError:
                print("❌ Erro: Digite um número válido.")

    elif option == "4":
        print("\n--- EXCLUIR DADOS ---")
        if not dados_talhoes:
            print("Nenhum dado cadastrado para excluir.")
        else:
            for i, t in enumerate(dados_talhoes):
                print(f"{i}. Cultura: {t['cultura']} | Área: {t['hectares']:.4f} ha")
            try:
                indice = int(input("\nDigite o número do talhão que deseja excluir: "))
                if 0 <= indice < len(dados_talhoes):
                    removido = dados_talhoes.pop(indice)
                    print(f"✅ Talhão de {removido['cultura']} excluído com sucesso!")
                else:
                    print("❌ Índice não encontrado.")
            except ValueError:
                print("❌ Erro: Digite um número válido.")

    elif option == "5":
        print("Sair")
        exit()
    else:
        print("Opção inválida")

def identificar_forma(lados):
    if lados == 0: return "Círculo"
    elif lados == 3: return "Triângulo"
    elif lados == 4: return "Quadrilátero"
    elif lados == 5: return "Pentágono"
    elif lados == 6: return "Hexágono"
    elif lados == 7: return "Heptágono"
    elif lados == 8: return "Octógono"
    else: return "Forma não identificada"

def capturar_medidas(lados):
    if lados == 0:
        raio = float(input("Digite a medida de raio da circunferência em metros: "))
        return [raio]
    medidas = [0] * lados
    for i in range(lados):
        medidas[i] = float(input(f"Digite a medida do lado {i+1} em metros: "))
    return medidas

def calcular_area(lados, medidas):
    if lados == 0:
        raio = medidas[0]
        area = 3.1416 * (raio ** 2)
    elif lados == 3:
        a, b, c = medidas[0], medidas[1], medidas[2]
        s = (a + b + c) / 2
        area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
    elif lados == 4:
        area = medidas[0] * medidas[1]
    else:
        perimetro = sum(medidas)
        area = perimetro * medidas[0] / 4
    return area

def converter_area(area_m2):
    hectares = area_m2 / 10000
    alqueires = area_m2 / 24200
    return hectares, alqueires

def menu_culturas():
    print("""
    1. Soja
    2. Milho
    3. Café
    4. Trigo
    5. Cana-de-açúcar
    """)
    opcao = input("Escolha uma opção: ")
    if opcao == "1": return "Soja"
    elif opcao == "2": return "Milho"
    elif opcao == "3": return "Café"
    elif opcao == "4": return "Trigo"
    elif opcao == "5": return "Cana-de-açúcar"
    else: return "Opção inválida"

def main():
    apresentation_animate()
    while True:
        menu()
        option_menu()

main()