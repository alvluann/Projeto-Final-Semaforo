class Veiculo:
    def __init__(self, modelo):
        self.modelo = modelo

    def caracteristica(self):
        if self.modelo == "pequeno":
            return {"velocidade": 20, "tamanho": 3}
        elif self.modelo == "medio":
            return {"velocidade": 15, "tamanho": 5}
        elif self.modelo == "grande":
            return {"velocidade": 10, "tamanho": 10}
        elif self.modelo == "caminhao_pequeno":
            return {"velocidade": 10, "tamanho": 15}
        elif self.modelo == "caminhao_medio":
            return {"velocidade": 7, "tamanho": 20}
        elif self.modelo == "caminhao_grande":
            return {"velocidade": 5, "tamanho": 25}

    def __str__(self):
        return f"{self.modelo.capitalize()} {self.__class__.__name__}"

class Carro(Veiculo):
    pass

class Caminhao(Veiculo):
    pass