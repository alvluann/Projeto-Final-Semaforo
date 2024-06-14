class Semaforo:
    def __init__(self, duracao_verde, duracao_amarelo, duracao_vermelho):
        self.duracao_verde = duracao_verde
        self.duracao_amarelo = duracao_amarelo
        self.duracao_vermelho = duracao_vermelho
        self.estado_atual = 'verde'
        self.tempo_restante = duracao_vermelho

    def ciclo_semaforo(self):
        if self.tempo_restante > 0:
            self.tempo_restante -= 1
        else:
            if self.estado_atual == 'vermelho':
                self.estado_atual = 'verde'
                self.tempo_restante = self.duracao_verde
            elif self.estado_atual == 'verde':
                self.estado_atual = 'amarelo'
                self.tempo_restante = self.duracao_amarelo
            elif self.estado_atual == 'amarelo':
                self.estado_atual = 'vermelho'
                self.tempo_restante = self.duracao_vermelho

    def is_verde(self):
        return self.estado_atual == 'verde'
