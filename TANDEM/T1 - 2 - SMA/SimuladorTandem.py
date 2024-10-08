import heapq
import random
from Fila import Fila

class SimuladorTandem:
    def __init__(self, fila1_config, fila2_config, tempo_inicial, num_eventos, seed=None):
        self.fila1 = Fila(*fila1_config, seed=seed)
        self.fila2 = Fila(*fila2_config, seed=seed)
        self.tempo_atual = tempo_inicial
        self.num_eventos = num_eventos
        self.eventos_processados = 0
        self.fila1.agendar_evento('chegada', self.tempo_atual)

    def simular(self):
        while self.eventos_processados < self.num_eventos:
            if not self.fila1.eventos and not self.fila2.eventos:
                break
            proximo_evento_fila1 = self.fila1.proximo_evento()
            proximo_evento_fila2 = self.fila2.proximo_evento()
            if proximo_evento_fila1[0] <= proximo_evento_fila2[0]:
                self.processar_evento(self.fila1, proximo_evento_fila1)
            else:
                self.processar_evento(self.fila2, proximo_evento_fila2)
            self.eventos_processados += 1
            if self.fila1.clientes < self.fila1.capacidade:
                novo_tempo_chegada = self.tempo_atual + random.uniform(1, 3)
                self.fila1.agendar_evento('chegada', novo_tempo_chegada)

    def processar_evento(self, fila, evento):
        tempo, tipo = heapq.heappop(fila.eventos)
        fila.atualizar_tempo_estado(tempo)
        self.tempo_atual = tempo
        tempo_saida = fila.processar_evento(tipo, tempo)
        if tempo_saida is not None and fila is self.fila1:
            self.fila2.agendar_evento('chegada', tempo_saida)

    def calcular_estatisticas(self):
        return self.fila1.estatisticas['clientes_atendidos'] + self.fila2.estatisticas['clientes_atendidos']

    def imprimir_relatorio_formatado(self):
        print("========================================================")
        print("============   QUEUEING NETWORK SIMULATOR   ============")
        print("===================    ====================")
        print("================    Flávia Webster  =================")
        print("=========================================================")
        print("Simulation: #1")
        print("...simulating with random numbers (seed '1')...")
        print("=========================================================")
        print("=================    END OF SIMULATION   ================")
        print("=========================================================")

        print("\n=========================================================")
        print("======================    REPORT   ======================")
        print("=========================================================")
        self.imprimir_secao_fila(self.fila1, "Q1 (G/G/1)", "Arrival: 1.0 ... 4.0", "Service: 1.0 ... 1.5")
        self.imprimir_secao_fila(self.fila2, "Q2 (G/G/3/5)", "", "Service: 5.0 ... 10.0")
        print("=========================================================")
        print(f"Simulation average time: {self.calcular_tempo_medio():.4f}")
        print("=========================================================")

    def imprimir_secao_fila(self, fila, nome_fila, descricao_chegada, descricao_servico):
        print("*********************************************************")
        print(f"Queue:   {nome_fila}")
        print(descricao_chegada)
        print(descricao_servico)
        print("*********************************************************")
        print("   State               Time               Probability")

        tempo_total = sum(fila.tempo_estado)
        for estado, tempo in enumerate(fila.tempo_estado):
            probabilidade = (tempo / tempo_total) * 100 if tempo_total > 0 else 0
            print(f"      {estado}           {tempo:.4f}                {probabilidade:.2f}%")

        print(f"\nNumber of losses: {fila.perdas}")
        print("*********************************************************")

    def calcular_tempo_medio(self):
        tempo_total_simulacao = 0
        for fila in [self.fila1, self.fila2]:
            tempo_total_simulacao += sum(fila.tempo_estado)
        return tempo_total_simulacao / self.num_eventos if self.num_eventos > 0 else 0
    
    def imprimir_medias(self):
        print("\n=========================================================")
        print("Média de Tempo por Fila:")


        media_fila1 = sum(self.fila1.tempo_estado) / self.fila1.estatisticas['clientes_atendidos'] if self.fila1.estatisticas['clientes_atendidos'] > 0 else 0
        print(f"Média de Tempo para Fila 1: {media_fila1:.4f}")

        media_fila2 = sum(self.fila2.tempo_estado) / self.fila2.estatisticas['clientes_atendidos'] if self.fila2.estatisticas['clientes_atendidos'] > 0 else 0
        print(f"Média de Tempo para Fila 2: {media_fila2:.4f}")

        media_total = (media_fila1 + media_fila2) / 2
        print("\n=========================================================")
        print(f"Média Total de Todas as Filas: {media_total:.4f}")
        print("=========================================================")

