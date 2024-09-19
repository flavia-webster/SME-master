import heapq
import random

class Fila:
    def __init__(self, atendimento_min, atendimento_max, servidores, capacidade, seed=None):
        if seed is not None:
            random.seed(seed)
        self.atendimento_min = atendimento_min
        self.atendimento_max = atendimento_max
        self.servidores = servidores
        self.capacidade = capacidade
        self.clientes = 0
        self.eventos = []
        self.perdas = 0
        self.estatisticas = {'tempo': 0, 'clientes_atendidos': 0}
        self.tempo_estado = [0] * (capacidade + 1)
        self.ultimo_tempo = 0

    def atualizar_tempo_estado(self, novo_tempo):
        tempo_passado = novo_tempo - self.ultimo_tempo
        if self.clientes < len(self.tempo_estado):
            self.tempo_estado[self.clientes] += tempo_passado
        self.ultimo_tempo = novo_tempo  

    def agendar_evento(self, tipo, tempo):
        heapq.heappush(self.eventos, (tempo, tipo))

    def processar_evento(self, tipo, tempo):
        if tipo == 'chegada':
            if self.clientes < self.capacidade:
                self.clientes += 1
                if self.clientes <= self.servidores:
                    self.agendar_evento('saida', tempo + random.uniform(self.atendimento_min, self.atendimento_max))
            else:
                self.perdas += 1
        elif tipo == 'saida':
            self.clientes -= 1
            self.estatisticas['clientes_atendidos'] += 1
            if self.clientes >= self.servidores:
                self.agendar_evento('saida', tempo + random.uniform(self.atendimento_min, self.atendimento_max))
            return tempo

    def proximo_evento(self):
        return self.eventos[0] if self.eventos else (float('inf'), '')