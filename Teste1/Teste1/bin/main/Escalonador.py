import heapq
from TipoAcao import TipoAcao
from typing import Optional

class Escalonador:
    def __init__(self):
        self.eventos_nao_processados = []
        self.eventos_processados = []
        self.contador_eventos = 0 

    def registra_novo_evento(self, tipo_acao, tempo_evento, fila):
        evento = {'tipo_acao': tipo_acao, 'tempo_agendado': tempo_evento, 'fila': fila}
        heapq.heappush(self.eventos_nao_processados, (tempo_evento, self.contador_eventos, evento))
        self.contador_eventos += 1
        
    def get_next(self):
        if self.eventos_nao_processados:
            next_event = heapq.heappop(self.eventos_nao_processados)
            return next_event
        return None
