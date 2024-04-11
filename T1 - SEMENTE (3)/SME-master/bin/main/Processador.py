from TipoAcao import TipoAcao
from Escalonador import Escalonador

class Processador:
    tempo_atual_sistema = 0
    tempo_anterior = 0
    condicao_parada = False
    contador_eventos = 0
    limite_eventos = 100000
    escalonador = None
    fila_inicial = None

    @classmethod
    def start(cls):
        while not cls.condicao_parada and cls.contador_eventos < cls.limite_eventos:
            evento_tuple = cls.escalonador.get_next()

            if evento_tuple:
                tempo_evento, _, evento = evento_tuple

                if evento['tipo_acao'] == TipoAcao.CHEGADA:
                    evento['fila'].processa_chegada(tempo_evento)
                elif evento['tipo_acao'] == TipoAcao.SAIDA:
                    evento['fila'].processa_saida(tempo_evento)

                cls.contador_eventos += 1
                cls.tempo_atual_sistema = tempo_evento
            else:
                cls.condicao_parada = True

    @classmethod
    def registra_novo_evento(cls, tipo_acao, tempo_evento, fila):
        cls.escalonador.registra_novo_evento(tipo_acao, tempo_evento, fila)

    @classmethod
    def reset(cls):
        cls.tempo_atual_sistema = 0
        cls.tempo_anterior = 0
        cls.condicao_parada = False
        cls.contador_eventos = 0

    @classmethod
    def config_processador(cls, escalonador, fila, tempo_inicial):
        cls.escalonador = escalonador
        cls.fila_inicial = fila
        cls.tempo_atual_sistema = tempo_inicial

    @classmethod
    def close(cls):
        if cls.contador_eventos == 0:
            print("Nenhum evento foi processado.")
            return

        print("## RESULTADOS ##\n")
        estatisticas, perdas = cls.fila_inicial.get_estatisticas()
        for estado, probabilidade in estatisticas.items():
            print(f"Estado {estado}: {probabilidade:.2f}%")
        
        print(f"\nNúmero de perdas: {perdas}")
        print(f"\nTempo médio do sistema: {cls.tempo_atual_sistema / cls.contador_eventos:.2f}")
        print("Simulação finalizada.")
