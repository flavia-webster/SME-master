import heapq
import random

class Fila:
    def __init__(self, chegada_min, chegada_max, atendimento_min, atendimento_max, servidores, capacidade, seed=None):
        if seed is not None:
            random.seed(seed)
        self.chegada_min = chegada_min
        self.chegada_max = chegada_max
        self.atendimento_min = atendimento_min
        self.atendimento_max = atendimento_max
        self.servidores = servidores
        self.capacidade = capacidade
        self.clientes = 0
        self.eventos = []  # heap de eventos
        self.perdas = 0
        self.estatisticas = {'tempo': 0, 'clientes_atendidos': 0}
        self.tempo_estado = [0] * (capacidade + 1)
        self.ultimo_tempo = 0

    def atualizar_tempo_estado(self, novo_tempo):
        """Atualiza o tempo que a fila passou em cada estado."""
        tempo_passado = novo_tempo - self.ultimo_tempo
        if self.clientes < len(self.tempo_estado):
            self.tempo_estado[self.clientes] += tempo_passado
        self.ultimo_tempo = novo_tempo

    def agendar_evento(self, tipo, tempo):
        """Agenda um evento de chegada ou saída."""
        heapq.heappush(self.eventos, (tempo, tipo))

    def processar_evento(self, tipo, tempo):
        """Processa o evento de chegada ou saída."""
        self.atualizar_tempo_estado(tempo)
        
        if tipo == 'chegada':
            if self.clientes < self.capacidade:
                self.clientes += 1
                if self.clientes <= self.servidores:
                    # Se há servidores disponíveis, agendar saída
                    self.agendar_evento('saida', tempo + random.uniform(self.atendimento_min, self.atendimento_max))
                # Agendar próxima chegada
                self.agendar_evento('chegada', tempo + random.uniform(self.chegada_min, self.chegada_max))
            else:
                self.perdas += 1

        elif tipo == 'saida':
            self.clientes -= 1
            self.estatisticas['clientes_atendidos'] += 1
            if self.clientes >= self.servidores:
                # Se ainda há clientes esperando, agendar próxima saída
                self.agendar_evento('saida', tempo + random.uniform(self.atendimento_min, self.atendimento_max))

    def simular(self, tempo_inicial, num_eventos):
        """Realiza a simulação até completar o número de eventos."""
        self.agendar_evento('chegada', tempo_inicial)
        eventos_processados = 0

        while eventos_processados < num_eventos and self.eventos:
            tempo, tipo = heapq.heappop(self.eventos)
            self.processar_evento(tipo, tempo)
            eventos_processados += 1

        if self.eventos:
            # Atualizar o tempo final da simulação se ainda houver eventos
            self.atualizar_tempo_estado(tempo)

    def relatorio(self):
        """Gera o relatório de estatísticas da simulação."""
        tempo_total = sum(self.tempo_estado)
        print(f"Tempo total de simulação: {tempo_total:.2f}")
        print(f"Clientes atendidos: {self.estatisticas['clientes_atendidos']}")
        print(f"Clientes perdidos: {self.perdas}")
        print("\nDistribuição de estados:")
        for i, tempo in enumerate(self.tempo_estado):
            probabilidade = tempo / tempo_total * 100 if tempo_total > 0 else 0
            print(f"Estado {i}: {tempo:.2f} unidades de tempo ({probabilidade:.2f}%)")

if __name__ == "__main__":
    # Fila G/G/1/5
    print("Simulação para Fila G/G/1/5:")
    fila1 = Fila(2, 5, 3, 5, 1, 5, seed=42)
    fila1.simular(tempo_inicial=2.0, num_eventos=100000)
    fila1.relatorio()

    # Fila G/G/2/5
    print("\nSimulação para Fila G/G/2/5:")
    fila2 = Fila(2, 5, 3, 5, 2, 5, seed=42)
    fila2.simular(tempo_inicial=2.0, num_eventos=100000)
    fila2.relatorio()
