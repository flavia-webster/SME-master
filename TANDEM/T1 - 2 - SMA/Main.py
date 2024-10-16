from SimuladorTandem import SimuladorTandem


if __name__ == "__main__":
    fila1_config = (1, 2, 1, 4) 
    fila2_config = (4, 8, 2, 10) 
    fila3_config = (5, 15, 2, 15) 
    simulador = SimuladorTandem(fila1_config, fila2_config, fila3_config, tempo_inicial=2.0, num_eventos=100000, seed=42)
    simulador.simular()
    simulador.imprimir_relatorio_formatado()
    simulador.imprimir_medias()
    simulador.imprimir_perdas()
    simulador.imprimir_tempo_global()
    simulador.imprimir_distribuicao_probabilidades()
    simulador.imprimir_tempos_acumulados()
