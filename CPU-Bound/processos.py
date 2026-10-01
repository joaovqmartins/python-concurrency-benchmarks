# 3c - Soma dos dígitos de todos os números de 1 até N - versão com MULTIPROCESSING
# Executar: python3 processos.py

import sys, time, os
from multiprocessing import Process, Queue

N = 40_000_000

def soma_digitos(numero):
    soma = 0
    while numero > 0:
        soma += numero % 10      # pega o último dígito
        numero = numero // 10    # remove o último dígito
    return soma

def somar_intervalo(inicio, fim, resultados):
    total = 0
    for numero in range(inicio, fim):
        total += soma_digitos(numero)
    resultados.put(total)        # cada processo envia a sua soma parcial pela fila

def criar_intervalos(num_processos):
    tamanho = N // num_processos
    intervalos = []
    for i in range(num_processos):
        inicio = i * tamanho + 1
        if i == num_processos - 1:
            fim = N + 1          # o último processo vai até o final
        else:
            fim = inicio + tamanho
        intervalos.append((inicio, fim))
    return intervalos

if __name__ == "__main__":
    print("Python:", sys.version)
    print("CPUs disponíveis:", os.cpu_count())
    num_processos = int(input("Digite o número de processos: "))

    intervalos = criar_intervalos(num_processos)
    print(intervalos)

    resultados = Queue()
    processos = []
    inicio = time.perf_counter()
    # Cria e inicia os processos
    for i in range(num_processos):
        processo = Process(target=somar_intervalo,
                           args=(intervalos[i][0], intervalos[i][1], resultados))
        processos.append(processo)
        processo.start()
    # Espera todos os processos terminarem
    for processo in processos:
        processo.join()
    fim = time.perf_counter()

    # Soma os resultados parciais
    total = 0
    for _ in range(num_processos):
        total += resultados.get()
    print(f"Tempo: {fim - inicio:.2f} segundos")
    print(f"Soma dos dígitos de 1 até {N:,}: {total:,}".replace(",", "."))
