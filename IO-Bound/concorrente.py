# Consulta de preço de um produto em 5 lojas online - versão CONCORRENTE (asyncio)

import time, random, asyncio

# Cada loja: (nome, tempo de resposta em segundos)
LOJAS = [
    ("Loja A", 1),
    ("Loja B", 2),
    ("Loja C", 3),
    ("Loja D", 1.5),
    ("Loja E", 2.5),
]

async def consultar_loja(nome, segundos):
    print(f"Consultando {nome}...")
    await asyncio.sleep(segundos)           # espera SEM travar: as outras lojas seguem
    preco = random.randint(3000, 4000)
    print(f"{nome} respondeu em {segundos} s: R$ {preco}")
    return nome, preco

async def main():
    tarefas = []
    for nome, segundos in LOJAS:
        tarefas.append(consultar_loja(nome, segundos))
    # Executa todas as consultas de forma concorrente e espera todas terminarem
    return await asyncio.gather(*tarefas)

inicio = time.perf_counter()
resultados = asyncio.run(main())
fim = time.perf_counter()

# Procura o menor preço
melhor_loja, melhor_preco = resultados[0]
for nome, preco in resultados:
    if preco < melhor_preco:
        melhor_loja = nome
        melhor_preco = preco

print(f"\nMelhor preço: {melhor_loja} com R$ {melhor_preco}")
print(f"Tempo total: {fim - inicio:.2f} segundos")
