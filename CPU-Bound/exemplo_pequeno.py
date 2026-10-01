# Exemplo PEQUENO só para entender o problema (não vai para as medições)
# Mostra, número por número, a soma dos dígitos de 1 até 12.

N = 12

def soma_digitos(numero):
    soma = 0
    while numero > 0:
        soma += numero % 10      # pega o último dígito
        numero = numero // 10    # remove o último dígito
    return soma

total = 0
for numero in range(1, N + 1):
    s = soma_digitos(numero)
    total += s
    print(f"Número {numero:2} -> soma dos dígitos = {s:2} | total acumulado = {total}")

print(f"\nResultado final para N = {N}: {total}")
