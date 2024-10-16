import heapq
import random
from Fila import Fila

class SimuladorTandem:
    def __init__(self, fila1_config, fila2_config, fila3_config, tempo_inicial, num_eventos, seed=None):
        self.fila1 = Fila(*fila1_config, seed=seed)
        self.fila2 = Fila(*fila2_config, seed=seed)
        self.fila3 = Fila(*fila3_config, seed=seed)
        self.tempo_atual = tempo_inicial
        self.num_eventos = num_eventos
        self.eventos_processados = 0
        self.fila1.agendar_evento('chegada', self.tempo_atual)

    def simular(self):
        while self.eventos_processados < self.num_eventos:
            if not self.fila1.eventos and not self.fila2.eventos and not self.fila3.eventos:
                break
            proximo_evento_fila1 = self.fila1.proximo_evento()
            proximo_evento_fila2 = self.fila2.proximo_evento()
            proximo_evento_fila3 = self.fila3.proximo_evento()
            if proximo_evento_fila1[0] <= proximo_evento_fila2[0]:
                self.processar_evento(self.fila1, proximo_evento_fila1)
            elif proximo_evento_fila2[0] <= proximo_evento_fila3[0]:
                self.processar_evento(self.fila2, proximo_evento_fila2)
            else:
                self.processar_evento(self.fila3, proximo_evento_fila3)
            self.eventos_processados += 1
            if self.fila1.clientes < self.fila1.capacidade:
                novo_tempo_chegada = self.tempo_atual + random.uniform(1.4, 3.4)
                self.fila1.agendar_evento('chegada', novo_tempo_chegada)

    def processar_evento(self, fila, evento):
        tempo, tipo = heapq.heappop(fila.eventos)
        fila.atualizar_tempo_estado(tempo)
        self.tempo_atual = tempo
        tempo_saida = fila.processar_evento(tipo, tempo)
        if tempo_saida is not None and fila is self.fila1:
            self.fila2.agendar_evento('chegada', tempo_saida)
        if tempo_saida is not None and fila is self.fila2:
            self.fila3.agendar_evento('chegada', tempo_saida)

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
        self.imprimir_secao_fila(self.fila1, "Q1 (G/G/1)", "Arrival: 2 ... 4", "Service: 1 ... 2")
        self.imprimir_secao_fila(self.fila2, "Q2 (G/G/2/5)", "", "Service: 4.0 ... 8.0")
        self.imprimir_secao_fila(self.fila3, "Q3 (G/G/2/10)", "", "Service: 5.0 ... 10.0")
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
        for fila in [self.fila1, self.fila2, self.fila3]:
            tempo_total_simulacao += sum(fila.tempo_estado)
        return tempo_total_simulacao / self.num_eventos if self.num_eventos > 0 else 0
    
    def imprimir_medias(self):
        print("\n=========================================================")
        print("Média de Tempo por Fila:")


        media_fila1 = sum(self.fila1.tempo_estado) / self.fila1.estatisticas['clientes_atendidos'] if self.fila1.estatisticas['clientes_atendidos'] > 0 else 0
        print(f"Média de Tempo para Fila 1: {media_fila1:.4f}")

        media_fila2 = sum(self.fila2.tempo_estado) / self.fila2.estatisticas['clientes_atendidos'] if self.fila2.estatisticas['clientes_atendidos'] > 0 else 0
        print(f"Média de Tempo para Fila 2: {media_fila2:.4f}")

        media_fila3 = sum(self.fila3.tempo_estado) / self.fila3.estatisticas['clientes_atendidos'] if self.fila3.estatisticas['clientes_atendidos'] > 0 else 0
        print(f"Média de Tempo para Fila 3: {media_fila3:.4f}")

        media_total = (media_fila1 + media_fila2 + media_fila3) / 3
        print("\n=========================================================")
        print(f"Média Total de Todas as Filas: {media_total:.4f}")
        print("=========================================================")

    def imprimir_perdas(self):
        print("\n=========================================================")
        print("Perdas de Clientes por Fila:")
        print(f"Perdas na Fila 1: {self.fila1.perdas}")
        print(f"Perdas na Fila 2: {self.fila2.perdas}")
        print(f"Perdas na Fila 3: {self.fila3.perdas}")
        print("=========================================================")

    def imprimir_tempo_global(self):
        print("\n=========================================================")
        tempo_global = sum(self.fila1.tempo_estado) + sum(self.fila2.tempo_estado) + sum(self.fila3.tempo_estado)
        print(f"Tempo Global da Simulação: {tempo_global:.4f}")
        print("=========================================================")

    def imprimir_distribuicao_probabilidades(self):
        print("\n=========================================================")
        print("Distribuição de Probabilidades dos Estados das Filas:")
        
        filas = [self.fila1, self.fila2, self.fila3]
        for i, fila in enumerate(filas):
            tempo_total = sum(fila.tempo_estado)
            print(f"\nFila {i + 1}:")
            for estado, tempo in enumerate(fila.tempo_estado):
                probabilidade = (tempo / tempo_total) * 100 if tempo_total > 0 else 0
                print(f"  Estado {estado}: {probabilidade:.2f}%")
        
        print("=========================================================")

    def imprimir_tempos_acumulados(self):
        print("\n=========================================================")
        print("Tempos Acumulados para os Estados das Filas:")
        
        filas = [self.fila1, self.fila2, self.fila3]
        for i, fila in enumerate(filas):
            print(f"\nFila {i + 1}:")
            for estado, tempo in enumerate(fila.tempo_estado):
                print(f"  Estado {estado}: {tempo:.4f}")
        
        print("=========================================================")
