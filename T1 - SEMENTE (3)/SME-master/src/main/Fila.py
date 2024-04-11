import random
from Processador import Processador
from TipoAcao import TipoAcao

class Fila:
    def __init__(self, id_fila, tempo_chegada, tempo_servico, capacidade, servidores):
        self.id_fila = id_fila
        self.tempo_chegada = tempo_chegada 
        self.tempo_servico = tempo_servico  
        self.capacidade = capacidade
        self.servidores = servidores
        self.fila_espera = 0
        self.servindo = 0
        self.perdas = 0
        self.estatisticas = {}
        self.transicoes = []
        self.ultimo_tempo = 0 

    def inicia_chegadas(self, tempo_inicial):
        self.ultimo_tempo = tempo_inicial
        self.agendar_proxima_chegada(tempo_inicial)    

    def adiciona_transicao(self, fila_filho, probabilidade):
        assert 0 <= probabilidade <= 1, "Probabilidade deve ser entre 0 e 1"
        self.transicoes.append((fila_filho, probabilidade))

    def escolhe_proxima_fila(self):
        filas, probabilidades = zip(*self.transicoes)
        return random.choices(filas, weights=probabilidades, k=1)[0]

    def atualiza_estatisticas(self, tempo_atual):
        estado_atual = self.fila_espera + self.servindo
        if estado_atual in self.estatisticas:
            self.estatisticas[estado_atual] += (tempo_atual - self.ultimo_tempo)
        else:
            self.estatisticas[estado_atual] = (tempo_atual - self.ultimo_tempo)
        self.ultimo_tempo = tempo_atual

    def processa_chegada(self, tempo_atual):
        if self.fila_espera + self.servindo >= self.capacidade:
            self.perdas += 1
        else:
            self.fila_espera += 1
            if self.servindo < self.servidores:
                self.servindo += 1
                self.fila_espera -= 1
                self.agendar_saida(tempo_atual)

        self.atualiza_estatisticas(tempo_atual)
        self.agendar_proxima_chegada(tempo_atual)

    def agendar_saida(self, tempo_atual):
        tempo_servico = random.uniform(*self.tempo_servico)
        Processador.registra_novo_evento(
            TipoAcao.SAIDA,
            tempo_atual + tempo_servico,
            self
        )

    def agendar_proxima_chegada(self, tempo_atual):
        tempo_entre_chegadas = random.uniform(*self.tempo_chegada)
        Processador.registra_novo_evento(
            TipoAcao.CHEGADA,
            tempo_atual + tempo_entre_chegadas,
            self
        )

    def processa_saida(self, tempo_atual):
        self.servindo -= 1
        if self.fila_espera > 0:
            self.fila_espera -= 1
            self.servindo += 1
            self.agendar_saida(tempo_atual)

        proxima_fila = self.escolhe_proxima_fila()
        if proxima_fila is not None:
            proxima_fila.processa_chegada(tempo_atual)

        self.atualiza_estatisticas(tempo_atual)

    def get_estatisticas(self):
        tempo_total = sum(self.estatisticas.values())
        probabilidade = {estado: (tempo / tempo_total) * 100 for estado, tempo in self.estatisticas.items()}
        return probabilidade, self.perdas
