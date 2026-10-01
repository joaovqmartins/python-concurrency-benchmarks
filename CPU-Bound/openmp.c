// 3d - Soma dos dígitos de todos os números de 1 até N - versão com OpenMP em C
// Compilar: gcc -fopenmp openmp.c -o openmp
// Executar: ./openmp

#include <stdio.h>
#include <omp.h>

int soma_digitos(int numero) {
    int soma = 0;
    while (numero > 0) {
        soma += numero % 10;     // pega o último dígito
        numero = numero / 10;    // remove o último dígito (divisão inteira)
    }
    return soma;
}

int main() {
    int limite = 40000000;
    long long total = 0;         // 64 bits: um int vai só até ~2,1 bilhões e o total (1,32 bilhão) já está perto do limite
    int threads;

    printf("Digite o numero de threads: ");
    scanf("%d", &threads);

    double inicio = omp_get_wtime();
    omp_set_num_threads(threads);
    #pragma omp parallel for schedule(static) reduction(+:total)
    for (int numero = 1; numero <= limite; numero++) {
        total += soma_digitos(numero);
    }
    double fim = omp_get_wtime();

    printf("Tempo: %.4f seg\n", fim - inicio);
    printf("Soma dos digitos de 1 ate %d: %lld\n", limite, total);
    return 0;
}
