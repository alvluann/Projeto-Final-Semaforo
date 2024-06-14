import random
from collections import deque
from veiculos import Carro, Caminhao
from semaforo import Semaforo
import mysql.connector

def criar_trafego(quantidade):
    fila = deque()
    modelos = ["pequeno", "medio", "grande"]
    for _ in range(quantidade):
        if random.random() < 0.5:
            veiculo = Carro(random.choice(modelos))
        else:
            veiculo = Caminhao(random.choice(modelos))
        fila.append(veiculo)
    return fila

def criar_trafego_personalizado(quant_carros_pequenos, quant_carros_medios, quant_carros_grandes, quant_camioes_pequenos, quant_camioes_medios, quant_camioes_grandes):
    fila = deque()
    for _ in range(quant_carros_pequenos):
        fila.append(Carro("pequeno"))
    for _ in range(quant_carros_medios):
        fila.append(Carro("medio"))
    for _ in range(quant_carros_grandes):
        fila.append(Carro("grande"))
    for _ in range(quant_camioes_pequenos):
        fila.append(Caminhao("pequeno"))
    for _ in range(quant_camioes_medios):
        fila.append(Caminhao("medio"))
    for _ in range(quant_camioes_grandes):
        fila.append(Caminhao("grande"))

    lista_fila = list(fila)
    random.shuffle(lista_fila)
    return deque(lista_fila)

def simular_transito(fila_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo):
    semaforo = Semaforo(duracao_verde, duracao_amarelo, duracao_vermelho)
    ciclos_completos = 0

    primeiro_veiculo = None
    segundo_veiculo = None

    while len(fila_veiculos) != 0:
        semaforo.ciclo_semaforo()

        if semaforo.is_verde() and semaforo.duracao_verde >= 0:
            while fila_veiculos and semaforo.duracao_verde > 0:
                veiculo = fila_veiculos.popleft()

                if not primeiro_veiculo:
                    primeiro_veiculo = veiculo
                    distancia_percorrida = veiculo.tamanho() * semaforo.duracao_verde / veiculo.caracteristica()["velocidade"]
                    if distancia_percorrida >= distancia_semaforo:
                        # First vehicle crosses the intersection
                        primeiro_veiculo = None
                elif primeiro_veiculo and segundo_veiculo is None:
                    segundo_veiculo = veiculo
                    distancia_percorrida = veiculo.tamanho() * semaforo.duracao_verde / veiculo.caracteristica()["velocidade"]
                elif segundo_veiculo:
                    if veiculo.caracteristica()["velocidade"] > primeiro_veiculo.caracteristica()["velocidade"]:
                        veiculo.caracteristica()["velocidade"] = primeiro_veiculo.caracteristica()["velocidade"]
                    distancia_percorrida = veiculo.tamanho() * semaforo.duracao_verde / veiculo.caracteristica()["velocidade"]

                    if distancia_percorrida >= distancia_semaforo:
                        segundo_veiculo = None

                semaforo.duracao_verde -= veiculo.tamanho() / veiculo.caracteristica()["velocidade"]

        ciclos_completos += 1

    return ciclos_completos

def salvar_relatorio(conexao, quantidade_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo,
                     ciclos_completos, quant_carros_pequenos, quant_carros_medios, quant_carros_grandes,
                     quant_camioes_pequenos, quant_camioes_medios, quant_camioes_grandes):
    cursor = conexao.cursor()
    sql = """
    INSERT INTO relatorios (duracao_verde, duracao_amarelo, duracao_vermelho, quantidade_veiculos,
                            quant_carros_pequenos, quant_carros_medios, quant_carros_grandes,
                            quant_camioes_pequenos, quant_camioes_medios, quant_camioes_grandes,
                            distancia_semaforo, ciclos_completos)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (duracao_verde, duracao_amarelo, duracao_vermelho, quantidade_veiculos, quant_carros_pequenos,
               quant_carros_medios, quant_carros_grandes, quant_camioes_pequenos, quant_camioes_medios,
               quant_camioes_grandes, distancia_semaforo, ciclos_completos)
    cursor.execute(sql, valores)
    conexao.commit()

def mostrar_relatorios(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM relatorios")
    relatorios = cursor.fetchall()

    for relatorio in relatorios:
        relatorio_id, duracao_verde, duracao_amarelo, duracao_vermelho, quantidade_veiculos, quant_carros_pequenos, \
        quant_carros_medios, quant_carros_grandes, quant_camioes_pequenos, quant_camioes_medios, \
        quant_camioes_grandes, distancia_semaforo, ciclos_completos = relatorio
        print(f"Número do Relatório: {relatorio_id}")
        print(f"Duração do Sinal Verde: {duracao_verde} segundos")
        print(f"Duração do Sinal Amarelo: {duracao_amarelo} segundos")
        print(f"Duração do Sinal Vermelho: {duracao_vermelho} segundos")
        print(f"Quantidade de Veículos: {quantidade_veiculos}")
        print(f"Quantidade de Carros Pequenos: {quant_carros_pequenos}")
        print(f"Quantidade de Carros Médios: {quant_carros_medios}")
        print(f"Quantidade de Carros Grandes: {quant_carros_grandes}")
        print(f"Quantidade de Caminhões Pequenos: {quant_camioes_pequenos}")
        print(f"Quantidade de Caminhões Médios: {quant_camioes_medios}")
        print(f"Quantidade de Caminhões Grandes: {quant_camioes_grandes}")
        print(f"Distância do Semáforo: {distancia_semaforo} metros")
        print(f"Ciclos Completos: {ciclos_completos}")
        print("-" * 40)