# 3a - Soma dos dígitos de todos os números de 1 até N - versão SEQUENCIAL

import sys, time, os

N = 40_000_000

def soma_digitos(numero):
    soma = 0
    while numero > 0:
        soma += numero % 10      # pega o último dígito
        numero = numero // 10    # remove o último dígito
    return soma

def somar_intervalo(inicio, fim):
    total = 0
    for numero in range(inicio, fim):
        total += soma_digitos(numero)
    return total

print("Python:", sys.version)
print("CPUs disponíveis:", os.cpu_count())
print("Número de processos/threads: 1")

inicio = time.perf_counter()
total = somar_intervalo(1, N + 1)
fim = time.perf_counter()
print(f"Tempo: {fim - inicio:.2f} segundos")
print(f"Soma dos dígitos de 1 até {N:,}: {total:,}".replace(",", "."))
