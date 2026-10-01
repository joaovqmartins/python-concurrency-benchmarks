# 3b - Soma dos dígitos de todos os números de 1 até N - versão com THREADS
# Com GIL:  python3 threads.py
# Sem GIL:  python3.14t threads.py

import sys, time, os, threading

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
    resultados.append(total)     # cada thread guarda a sua soma parcial

def criar_intervalos(num_threads):
    tamanho = N // num_threads
    intervalos = []
    for i in range(num_threads):
        inicio = i * tamanho + 1
        if i == num_threads - 1:
            fim = N + 1          # a última thread vai até o final
        else:
            fim = inicio + tamanho
        intervalos.append((inicio, fim))
    return intervalos

print("Python:", sys.version)
print("GIL está habilitado:", sys._is_gil_enabled())
print("CPUs disponíveis:", os.cpu_count())
num_threads = int(input("Digite o número de threads: "))

intervalos = criar_intervalos(num_threads)
print(intervalos)

resultados = []
threads = []
inicio = time.perf_counter()
for i in range(num_threads):
    thread = threading.Thread(target=somar_intervalo,
                              args=(intervalos[i][0], intervalos[i][1], resultados))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
fim = time.perf_counter()

total = sum(resultados)
print(f"Tempo: {fim - inicio:.2f} segundos")
print(f"Soma dos dígitos de 1 até {N:,}: {total:,}".replace(",", "."))
