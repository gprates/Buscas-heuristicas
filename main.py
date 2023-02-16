import random
import numpy as np
import datetime

'''
Metodos Locais Monotonos -----------------------------------------------------------------------------------------------------------
'''

def atribuir_tarefa_aleatoria(numero_maquinas, numero_tarefas):
    """Gerar uma solução inicial aleatória para o problema."""
    atribuicao_tarefa = [0] * numero_tarefas

    for i in range(numero_tarefas):
        atribuicao_tarefa[i] = random.randint(0, numero_maquinas - 1)
    return atribuicao_tarefa

def calcular_custo_monotona(atribuicao_tarefa, capacidade_maquina):
    """Calcular o custo da solução atual."""
    custo = 0

    machine_load = [0] * len(capacidade_maquina)
    for i, task in enumerate(atribuicao_tarefa):
        machine_load[task] += 1
    for load in machine_load:
        custo += (load - capacidade_maquina[task]) ** 2
    return custo

def gerar_vizinho(atribuicao_tarefa):
    """Gerar uma solução vizinha."""
    vizinho = atribuicao_tarefa.copy()

    i = random.randint(0, len(atribuicao_tarefa) - 1)
    j = random.randint(0, len(atribuicao_tarefa) - 1)

    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]

    return vizinho

def busca_local(atribuicao_tarefa, capacidade_maquina):
    """Executar a Busca Local Monótona."""
    custo_atual = calcular_custo_monotona(atribuicao_tarefa, capacidade_maquina)

    iteracoes = 0
    while iteracoes<=1000:
        iteracoes+=1
        vizinho = gerar_vizinho(atribuicao_tarefa)
        custo_vizinho = calcular_custo_monotona(vizinho, capacidade_maquina)
        if custo_vizinho < custo_atual:
            atribuicao_tarefa = vizinho
            custo_atual = custo_vizinho
        else:
            break
            
    print('iteracoesm',iteracoes)
    return atribuicao_tarefa, custo_atual
        


'''
Metodos Locais Iterados -----------------------------------------------------------------------------------------------------------
'''

def gerar_solucao_inicial(numero_tarefas, numero_maquinas):
    # Inicialmente distribuímos as tarefas aleatoriamente entre as máquinas
    return [random.randint(0, numero_maquinas - 1) for i in range(numero_tarefas)]

def contar_carga(solucao, numero_maquinas):
    # Conta o número de tarefas em cada máquina
    carga = [0] * numero_maquinas

    for maquina in solucao:
        carga[maquina] += 1
    return carga

def calcular_custo_iterada(carga, numero_tarefas, numero_maquinas):
    # Calcula a diferença entre o número de tarefas na máquina mais carregada e a média
    media = numero_tarefas / numero_maquinas
    custo = max(carga) - media

    return custo

def perturbar(solucao, per):
    # Faz uma perturbação na solução atual, mudando o destino de uma tarefa aleatória
    i = random.randint(0, len(solucao) - 1)
    j = random.randint(0, len(solucao) - 1)

    if random.uniform(0, 1) < per:
        solucao[i], solucao[j] = solucao[j], solucao[i]
    return solucao

def busca_local_iterada(numero_tarefas, numero_maquinas, per):
    melhor_solucao = gerar_solucao_inicial(numero_tarefas, numero_maquinas)
    melhor_carga = contar_carga(melhor_solucao, numero_maquinas)
    melhor_custo = calcular_custo_iterada(melhor_carga, numero_tarefas, numero_maquinas)
    iteracoes = 0
    for i in range(1000):
        current_solution = perturbar(melhor_solucao[:], per)
        current_load = contar_carga(current_solution, numero_maquinas)
        current_cost = calcular_custo_iterada(current_load, numero_tarefas, numero_maquinas)

        if current_cost < melhor_custo:
            melhor_solucao = current_solution
            melhor_carga = current_load
            melhor_custo = current_cost

        iteracoes += 1
    print('iteracoes',iteracoes)
    return melhor_solucao

def busca_local_monotona_roda(numero_tarefas, numero_maquinas):
    start = datetime.datetime.now()

    # definir a capacidade de cada máquina
    capacidade_maquina = [numero_maquinas for _ in range(numero_maquinas)]

    # gerar uma solução inicial
    atribuicao_tarefa = atribuir_tarefa_aleatoria(numero_maquinas, numero_tarefas)

    # executar a Busca Local Monótona
    melhor_solucao, melhor_custo = busca_local(atribuicao_tarefa, capacidade_maquina)

    # imprimir a solução final e o custo
    print("Best solution:", melhor_solucao)
    print("Best custo:", melhor_custo)

    end = datetime.datetime.now()

    diff = end - start

    execution_time = diff.total_seconds() * 1000

    print(f'Tempo de execução monótona: {execution_time}ms')

    return melhor_solucao,melhor_custo,execution_time
    
 
def busca_local_iterada_roda(numero_tarefas,numero_maquinas,per):
    start = datetime.datetime.now()

    melhor_solucao = busca_local_iterada(numero_tarefas, numero_maquinas, per)
    carga = contar_carga(melhor_solucao, numero_maquinas)
    custo = calcular_custo_iterada(carga, numero_tarefas, numero_maquinas)
    print("Best solucao: ", melhor_solucao)
    print("carga: ",carga)
    print("custo: ", custo)

    end = datetime.datetime.now()

    diff = end - start

    execution_time = diff.total_seconds() * 1000

    print(f'Tempo de execução iterada: {execution_time}ms')

    return melhor_solucao,custo, execution_time


if __name__ == "__main__":
    numero_tarefas = 100
    numero_maquinas = 10
    per = 0.5

    melhor_solucao_ite, melhor_custo_ite, tempo_iterado = busca_local_iterada_roda(numero_tarefas,numero_maquinas,per)

    melhor_solucao_mono, melhor_custo_mono ,tempo_monotono = busca_local_monotona_roda(numero_tarefas,numero_maquinas)

    with open('resultado.txt', 'w') as f:       
        f.write(f'busca: iterada \nmelhor_solucao: {melhor_solucao_ite} \nmelhor_custo: {melhor_custo_ite} \ntempo_execucao: {tempo_iterado} ms \nparametro: {per} \nnumero_maquinas: {numero_maquinas} \nnumero_tarefas: {numero_tarefas}\n')
        f.write(f'busca: monotona \nmelhor_solucao: {melhor_solucao_mono} \nmelhor_custo: {melhor_custo_mono} \ntempo_execucao: {tempo_monotono} ms \nparametro: None \nnumero_maquinas: {numero_maquinas} \nnumero_tarefas: {numero_tarefas}\n')