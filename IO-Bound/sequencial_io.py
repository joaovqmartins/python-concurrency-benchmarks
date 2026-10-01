# Consulta de preço de um produto em 5 lojas online - versão SEQUENCIAL

import time, random

# Cada loja: (nome, tempo de resposta em segundos)
LOJAS = [
    ("Loja A", 1),
    ("Loja B", 2),
    ("Loja C", 3),
    ("Loja D", 1.5),
    ("Loja E", 2.5),
]

def consultar_loja(nome, segundos):
    print(f"Consultando {nome}...")
    time.sleep(segundos)                    # simula a espera pela resposta da rede
    preco = random.randint(3000, 4000)      # preço que a loja "devolveu"
    print(f"{nome} respondeu em {segundos} s: R$ {preco}")
    return nome, preco

inicio = time.perf_counter()
resultados = []
for nome, segundos in LOJAS:
    resultados.append(consultar_loja(nome, segundos))
fim = time.perf_counter()

# Procura o menor preço
melhor_loja, melhor_preco = resultados[0]
for nome, preco in resultados:
    if preco < melhor_preco:
        melhor_loja = nome
        melhor_preco = preco

print(f"\nMelhor preço: {melhor_loja} com R$ {melhor_preco}")
print(f"Tempo total: {fim - inicio:.2f} segundos")
