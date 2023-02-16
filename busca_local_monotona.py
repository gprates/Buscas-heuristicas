import random

iteracoes_monotona = None

def atribuir_tarefa_aleatoria(numero_maquinas, numero_tarefas):
    """Gerar uma solução inicial aleatória para o problema."""
    atribuicao_tarefa = [0] * numero_tarefas

    for i in range(numero_tarefas):
        atribuicao_tarefa[i] = random.randint(0, numero_maquinas - 1)
    return atribuicao_tarefa

def calcular_custo(atribuicao_tarefa, capacidade_maquina):
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
    iteracoes_monotona = 0
    """Executar a Busca Local Monótona."""
    custo_atual = calcular_custo(atribuicao_tarefa, capacidade_maquina)

    while True:
        vizinho = gerar_vizinho(atribuicao_tarefa)
        custo_vizinho = calcular_custo(vizinho, capacidade_maquina)
        iteracoes_monotona += 1
        if custo_vizinho < custo_atual:
            atribuicao_tarefa = vizinho
            custo_atual = custo_vizinho
        else:
            return atribuicao_tarefa, custo_atual, iteracoes_monotona
        

# definir a capacidade de cada máquina
capacidade_maquina = [10 for _ in range(10)]

# gerar uma solução inicial
atribuicao_tarefa = atribuir_tarefa_aleatoria(10, 100)

# executar a Busca Local Monótona
melhor_solucao, melhor_custo, iteracoes_monotona = busca_local(atribuicao_tarefa, capacidade_maquina)

print("Iterações monótona>: ", iteracoes_monotona)

# imprimir a solução final e o custo
print("Best solution:", melhor_solucao)
print("Best custo:", melhor_custo)