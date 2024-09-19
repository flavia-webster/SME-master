from SimuladorTandem import SimuladorTandem


if __name__ == "__main__":
    fila1_config = (1.4, 3.4, 2, 3) 
    fila2_config = (2, 3, 1, 5) 
    simulador = SimuladorTandem(fila1_config, fila2_config, tempo_inicial=1.5, num_eventos=100000, seed=42)
    simulador.simular()
    simulador.imprimir_relatorio_formatado()
    simulador.imprimir_medias()
    simulador.imprimir_perdas()
    simulador.imprimir_tempo_global()
