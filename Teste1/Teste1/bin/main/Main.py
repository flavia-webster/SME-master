import random
from Processador import Processador
from Escalonador import Escalonador
from Fila import Fila
from TipoAcao import TipoAcao

def simular_com_semente(semente, tempo_inicial=0):
    random.seed(semente)

   
    escalonador = Escalonador()


    fila1 = Fila(1, (1.4, 1.4), (1.4, 1.4), float('inf'), 1)  # G/G/1
    fila2 = Fila(2, (4.15, 4.15), (4.15, 4.15), 15, 3)       # G/G/3/15
    fila3 = Fila(3, (10.20, 10.20), (10.20, 10.20), 8, 2)    # G/G/2/8

    fila1.adiciona_transicao(fila2, 0.8)
    fila1.adiciona_transicao(None, 0.2)  
    fila2.adiciona_transicao(fila3, 0.5)
    fila2.adiciona_transicao(fila1, 0.2)
    fila2.adiciona_transicao(None, 0.3)  
    fila3.adiciona_transicao(None, 1.0)  


    Processador.config_processador(escalonador, fila1, tempo_inicial)
    Processador.reset() 

   
    fila1.inicia_chegadas(tempo_inicial)
    fila2.inicia_chegadas(tempo_inicial)
    fila3.inicia_chegadas(tempo_inicial)

   
    Processador.start()

   
    Processador.close()

    return Processador.tempo_atual_sistema, fila1, fila2, fila3

def print_header():
    header = (
        "========================================================\n"
        "============   QUEUEING NETWORK SIMULATOR   ============\n"
        "==================    (Novembro 2023)    ==================\n"
        "================    Flávia Webster e Arthur Zanella    ================\n"
        "========================================================\n"
        "=====                   Afonso Sales           =====\n"
        "======   Engenharia de Software (PUCRS)      ======\n"
        "========================================================\n"
    )
    print(header)

def print_queue_report(queue):
    print("*********************************************************")
    print(f"Queue:   Q{queue.id_fila} (G/G/{queue.servidores}/{queue.capacidade})")
    print(f"Arrival: {queue.tempo_chegada[0]} ... {queue.tempo_chegada[1]}")
    print(f"Service: {queue.tempo_servico[0]} ... {queue.tempo_servico[1]}")
    print("*********************************************************")
    print("   State               Time               Probability")
    for estado, tempo in queue.estatisticas.items():
        probabilidade = (tempo / sum(queue.estatisticas.values())) * 100
        print(f"     {estado:<17} {tempo:<20} {probabilidade:.2f}%")
    print(f"\nNumber of losses: {queue.perdas}")

def print_footer(media_tempo):
    footer = (
        "========================================================\n"
        "======================    REPORT   =====================\n"
        "========================================================\n"
        f"Simulation average time: {media_tempo}\n"
        "========================================================"
    )
    print(footer)

if __name__ == "__main__":
    resultados = []
    filas = []
    for semente in range(1, 6):  
        resultado, fila1, fila2, fila3 = simular_com_semente(semente)
        resultados.append(resultado)
        filas.append((fila1, fila2, fila3))

    
    media_resultados = sum(resultados) / len(resultados)

    print_header()
    
    for fila in filas[-1]:
        print_queue_report(fila)
    print_footer(media_resultados)
    print(f"Média do Tempo Atual do Sistema após 5 simulações: {media_resultados}")
