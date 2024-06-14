from logica import criar_trafego, criar_trafego_personalizado, simular_transito, salvar_relatorio, mostrar_relatorios
from banco import conectar_banco, criar_tabela_relatorios
from veiculos import Carro, Caminhao
import mysql.connector

def main():
    print("Escolha como deseja trabalhar o trânsito:")
    print("1. Aleatório")
    print("2. Personalizado")
    print("3. Mostrar Relatório")

    conexao = conectar_banco()
    criar_tabela_relatorios(conexao)

    escolha = int(input("Digite 1, 2 ou 3: "))

    if escolha == 1:
        quantidade_veiculos = int(input("Digite a quantidade total de veículos: "))
        fila_veiculos = criar_trafego(quantidade_veiculos)
        quant_carros_pequenos = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Carro) and veiculo.modelo == "pequeno")
        quant_carros_medios = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Carro) and veiculo.modelo == "medio")
        quant_carros_grandes = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Carro) and veiculo.modelo == "grande")
        quant_camioes_pequenos = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Caminhao) and veiculo.modelo == "pequeno")
        quant_camioes_medios = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Caminhao) and veiculo.modelo == "medio")
        quant_camioes_grandes = sum(1 for veiculo in fila_veiculos if isinstance(veiculo, Caminhao) and veiculo.modelo == "grande")
    elif escolha == 2:
        quant_carros_pequenos = int(input("Digite a quantidade de carros pequenos: "))
        quant_carros_medios = int(input("Digite a quantidade de carros médios: "))
        quant_carros_grandes = int(input("Digite a quantidade de carros grandes: "))
        quant_camioes_pequenos = int(input("Digite a quantidade de caminhões pequenos: "))
        quant_camioes_medios = int(input("Digite a quantidade de caminhões médios: "))
        quant_camioes_grandes = int(input("Digite a quantidade de caminhões grandes: "))
        fila_veiculos = criar_trafego_personalizado(
            quant_carros_pequenos, quant_carros_medios, quant_carros_grandes,
            quant_camioes_pequenos, quant_camioes_medios, quant_camioes_grandes)
        quantidade_veiculos = len(fila_veiculos)
    elif escolha == 3:
        mostrar_relatorios(conexao)
        conexao.close()
        return
    else:
        print("Opção inválida!")
        conexao.close()
        return

    print("Fila de tráfego gerada:")
    for veiculo in fila_veiculos:
        print(veiculo)

    duracao_verde = int(input("Digite a duração do sinal verde: "))
    duracao_amarelo = int(input("Digite a duração do sinal amarelo: "))
    duracao_vermelho = int(input("Digite a duração do sinal vermelho: "))
    distancia_semaforo = int(input("Digite a distância do semáforo: "))

    ciclos = simular_transito(fila_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo)
    print(f"Número de ciclos completos: {ciclos}")

    salvar_relatorio(conexao, quantidade_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo,
                     ciclos, quant_carros_pequenos, quant_carros_medios, quant_carros_grandes,
                     quant_camioes_pequenos, quant_camioes_medios, quant_camioes_grandes)

    conexao.close()

if __name__ == "__main__":
    main()