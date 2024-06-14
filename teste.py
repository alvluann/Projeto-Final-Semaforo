import mysql.connector
from collections import deque
import random


class Semaforo:
    def __init__(self, duracao_verde, duracao_amarelo, duracao_vermelho):
        self.duracao_verde = duracao_verde
        self.duracao_amarelo = duracao_amarelo
        self.duracao_vermelho = duracao_vermelho
        self.tempo_restante = duracao_verde

    def ciclo_semaforo(self):
        self.tempo_restante -= 1
        if self.tempo_restante < 0:
            self.tempo_restante = self.duracao_verde + self.duracao_amarelo + self.duracao_vermelho

    def is_verde(self):
        return self.tempo_restante > self.duracao_amarelo + self.duracao_vermelho


class Carro:
    def __init__(self, modelo):
        self.__modelo__ = modelo

    def caracteristica(self):
        modelos_caracteristicas = {
            "pequeno": {"tamanho": 5, "velocidade": 30},
            "medio": {"tamanho": 10, "velocidade": 20},
            "grande": {"tamanho": 15, "velocidade": 10}
        }
        return modelos_caracteristicas.get(self.__modelo__.lower(), {"tamanho": 0, "velocidade": 0})

    def tamanho(self):
        return self.caracteristica()["tamanho"]


class Caminhao:
    def __init__(self, modelo):
        self.__modelo__ = modelo

    def caracteristica(self):
        modelos_caracteristicas = {
            "pequeno": {"tamanho": 15, "velocidade": 15},
            "medio": {"tamanho": 20, "velocidade": 10},
            "grande": {"tamanho": 25, "velocidade": 5}
        }
        return modelos_caracteristicas.get(self.__modelo__.lower(), {"tamanho": 0, "velocidade": 0})

    def tamanho(self):
        return self.caracteristica()["tamanho"]


def criar_trafego(quantidade, aleatorio=True, especifico=None):
    fila = deque()
    modelos_carro = ["pequeno", "medio", "grande"]
    modelos_caminhao = ["pequeno", "medio", "grande"]

    if aleatorio:
        for _ in range(quantidade):
            if random.random() < 0.5:
                veiculo = Carro(random.choice(modelos_carro))
            else:
                veiculo = Caminhao(random.choice(modelos_caminhao))
            fila.append(veiculo)
    else:
        for tipo, modelo in especifico:
            if tipo.lower() == "carro":
                fila.append(Carro(modelo))
            elif tipo.lower() == "caminhao":
                fila.append(Caminhao(modelo))
    return fila


def simular_transito(fila_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo):
    semaforo = Semaforo(duracao_verde, duracao_amarelo, duracao_vermelho)
    ciclos_completos = 0

    while fila_veiculos:
        tempo_verde_restante = duracao_verde

        while semaforo.is_verde() and tempo_verde_restante > 0 and fila_veiculos:
            veiculo = fila_veiculos[0]
            distancia_necessaria = distancia_semaforo + veiculo.tamanho()
            tempo_necessario = distancia_necessaria / veiculo.caracteristica()["velocidade"]

            if tempo_necessario <= tempo_verde_restante:
                fila_veiculos.popleft()
                tempo_verde_restante -= tempo_necessario
            else:
                break

        ciclos_completos += 1
        semaforo.ciclo_semaforo()

    return ciclos_completos


def salvar_relatorio(conexao, quantidade_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo,
                     ciclos_completos):
    cursor = conexao.cursor()
    sql = """
    INSERT INTO relatorios (quantidade_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo, ciclos_completos)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
    quantidade_veiculos, duracao_verde, duracao_amarelo, duracao_vermelho, distancia_semaforo, ciclos_completos)
    cursor.execute(sql, valores)
    conexao.commit()


def mostrar_relatorios(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM relatorios")
    relatorios = cursor.fetchall()
    for relatorio in relatorios:
        print(relatorio)


# Configurar a conexão com o banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="simulacao_transito"
)

# Exemplo de uso
fila = criar_trafego(2, aleatorio=False, especifico=[("carro", "pequeno"), ("caminhao", "medio")])
print("Fila de tráfego gerada:")
for veiculo in fila:
    print(f"{type(veiculo).__name__} {veiculo.caracteristica()}")

ciclos = simular_transito(fila, 10, 2, 10, 5)
print(f"Número de ciclos completos: {ciclos}")

# Salvar o relatório no banco de dados
salvar_relatorio(conexao, 2, 10, 2, 10, 5, ciclos)

# Mostrar todos os relatórios
print("Relatórios salvos no banco de dados:")
mostrar_relatorios(conexao)

# Fechar a conexão com o banco de dados
conexao.close()