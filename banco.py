import mysql.connector

def conectar_banco():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="simulacao_transito"
    )
    return conexao

def criar_tabela_relatorios(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relatorios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        duracao_verde INT,
        duracao_amarelo INT,
        duracao_vermelho INT,
        quantidade_veiculos INT,
        quant_carros_pequenos INT,
        quant_carros_medios INT,
        quant_carros_grandes INT,
        quant_camioes_pequenos INT,
        quant_camioes_medios INT,
        quant_camioes_grandes INT,
        distancia_semaforo INT,
        ciclos_completos INT
    )
    """)
    conexao.commit()