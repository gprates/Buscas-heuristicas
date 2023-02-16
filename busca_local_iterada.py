import random
import numpy as np
import datetime

def gerar_solucao_inicial(numero_tarefas, numero_maquinas):
    # Inicialmente distribuímos as tarefas aleatoriamente entre as máquinas
    return [random.randint(0, numero_maquinas - 1) for i in range(numero_tarefas)]

def contar_carga(solucao, numero_maquinas):
    # Conta o número de tarefas em cada máquina
    carga = [0] * numero_maquinas

    for maquina in solucao:
        carga[maquina] += 1
    return carga

def calcular_custo(carga, numero_tarefas, numero_maquinas):
    # Calcula a diferença entre o número de tarefas na máquina mais carregada e a média
    media = numero_tarefas / numero_maquinas
    custo = max(carga) - media

    return custo

def perturbar(solucao, perturbacao):
    # Faz uma perturbação na solução atual, mudando o destino de uma tarefa aleatória
    i = random.randint(0, len(solucao) - 1)
    j = random.randint(0, len(solucao) - 1)

    if random.uniform(0, 1) < perturbacao:
        solucao[i], solucao[j] = solucao[j], solucao[i]
    return solucao

def busca_local_iterada(numero_tarefas, numero_maquinas, perturbacao):
    melhor_solucao = gerar_solucao_inicial(numero_tarefas, numero_maquinas)
    melhor_carga = contar_carga(melhor_solucao, numero_maquinas)
    melhor_custo = calcular_custo(melhor_carga, numero_tarefas, numero_maquinas)

    for i in range(100):
        solucao_atual = perturbar(melhor_solucao[:], perturbacao)
        carga_atual = contar_carga(solucao_atual, numero_maquinas)
        custo_atual = calcular_custo(carga_atual, numero_tarefas, numero_maquinas)

        if custo_atual < melhor_custo:
            melhor_solucao = solucao_atual
            melhor_carga = carga_atual
            melhor_custo = custo_atual
    return melhor_solucao

if __name__ == "__main__":
    numero_tarefas = 100
    numero_maquinas = 10
    perturbacao = 0.5

    start = datetime.datetime.now()

    melhor_solucao = busca_local_iterada(numero_tarefas, numero_maquinas, perturbacao)

    print("Best solucao: ", melhor_solucao)
    print("carga: ", contar_carga(melhor_solucao, numero_maquinas))
    print("custo: ", calcular_custo(contar_carga(melhor_solucao, numero_maquinas), numero_tarefas, numero_maquinas))

    end = datetime.datetime.now()

    diff = end - start

    execution_time = diff.total_seconds() * 1000

    print(f'Tempo de execução: {execution_time}ms')