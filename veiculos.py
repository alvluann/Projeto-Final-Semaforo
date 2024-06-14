class Veiculo:
    def __init__(self, modelo):
        self.modelo = modelo

    def tamanho(self):
        if self.modelo == "pequeno":
            return 3
        elif self.modelo == "medio":
            return 5
        elif self.modelo == "grande":
            return 7

    def caracteristica(self):
        if self.modelo == "pequeno":
            return {"velocidade": 40}
        elif self.modelo == "medio":
            return {"velocidade": 30}
        elif self.modelo == "grande":
            return {"velocidade": 20}

    def __str__(self):
        return f"{self.modelo.capitalize()} {self.__class__.__name__}"

class Carro(Veiculo):
    pass

class Caminhao(Veiculo):
    pass