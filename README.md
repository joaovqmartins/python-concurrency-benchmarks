# ⚡ Python Concurrency Benchmarks

Comparação prática entre **asyncio**, **threading com e sem GIL** (Python 3.14 free-threading), **multiprocessing** e **OpenMP em C**, medindo **tempo, speedup e eficiência** em cargas **IO-bound** e **CPU-bound**.

> Projeto desenvolvido a partir de um trabalho da disciplina *Sistemas Operacionais com Linux e Python*, e organizado aqui como referência rápida ("colinha") de comandos e resultados.

### Destaques

- 🌐 **IO-bound:** asyncio deixou a aplicação **3,3× mais rápida** usando uma única thread.
- 🔒 **GIL:** com o GIL, mais threads **não** trazem ganho em código CPU-bound (speedup ≈ 1,1).
- 🔓 **Sem GIL:** com o Python 3.14 free-threading, 8 threads chegaram a **2,2×** de speedup.
- 🧩 **Multiprocessing:** a melhor opção em Python puro (**2,7×** com 8 processos).
- 🚀 **OpenMP em C:** **~55× mais rápido** que o Python sequencial com 8 threads.

**Stack:** Python 3.14 · asyncio · threading · multiprocessing · C · OpenMP · GCC · Ubuntu (WSL2)

---

## 📁 Estrutura

```
.
├── ambiente.py              # mostra versão do Python, GIL e nº de CPUs
├── IO-Bound/
│   ├── sequencial_io.py     # consulta 5 lojas, uma de cada vez
│   └── concorrente.py       # consulta 5 lojas ao mesmo tempo (asyncio)
└── CPU-Bound/
    ├── exemplo_pequeno.py   # mostra a conta passo a passo (N = 12)
    ├── sequencial.py        # 3a - Python sequencial
    ├── threads.py           # 3b - threading (com e sem GIL)
    ├── processos.py         # 3c - multiprocessing
    └── openmp.c             # 3d - OpenMP em C
```

---

## 🖥️ 1. Ambiente

| Item | Configuração |
|---|---|
| Processador | Intel Core i5-1135G7 @ 2,40 GHz |
| Núcleos | **4 físicos / 8 lógicos** (Hyper-Threading) |
| Memória | 5,7 GiB visíveis no Ubuntu |
| Sistema | Ubuntu 26.04 LTS no **WSL2** (Windows) |
| Python com GIL | 3.14.4 (do Ubuntu) → `python3` |
| Python sem GIL | 3.14.7 free-threading (compilado) → `python3.14t` |
| Compilador C | GCC 15.2.0 com OpenMP |

### Comandos para descobrir o ambiente

```bash
nproc                  # nº de CPUs lógicas (deu 8)
lscpu                  # modelo, núcleos, threads por núcleo, virtualização
free -h                # memória RAM
cat /etc/os-release    # versão do Linux
python3 --version      # versão do Python
python3 ambiente.py    # mesmo resultado via Python (os.cpu_count())
```

> 💡 As 8 CPUs são **4 núcleos físicos × 2 threads**. Por isso o ganho de 4 → 8 threads é pequeno.

---

## ⚙️ 2. Preparação (fazer uma vez só)

### Clonar e abrir no VS Code pelo Ubuntu (WSL)

```bash
git clone https://github.com/joaovqmartins/python-concurrency-benchmarks.git
cd python-concurrency-benchmarks
code .
```

No VS Code, abra o terminal em **Terminal › New Terminal › Ubuntu (WSL)**. O prompt tem que ser `usuario@maquina:~$`, e não `PS C:\>`, que é o PowerShell.

### Instalar o Python **sem GIL** (free-threading)

Baseado no `README.TXT` da Aula07:

```bash
# 1) Ferramentas de compilação (o build-essential também traz o gcc do OpenMP)
sudo apt update && sudo apt install -y build-essential pkg-config libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev libffi-dev liblzma-dev tk-dev uuid-dev wget

# 2) Baixar e descompactar o código-fonte
cd /tmp && wget https://www.python.org/ftp/python/3.14.7/Python-3.14.7.tgz
tar -xzf Python-3.14.7.tgz && cd Python-3.14.7

# 3) Configurar SEM GIL, instalando numa pasta separada
./configure --disable-gil --prefix=$HOME/python3.14t

# 4) Compilar usando todas as CPUs (demora uns minutos) e instalar
make -j$(nproc)
make install

# 5) Colocar no FINAL do PATH (assim python3 continua sendo o normal, com GIL)
echo 'export PATH="$PATH:$HOME/python3.14t/bin"' >> ~/.bashrc
source ~/.bashrc
```

> ⚠️ O README da aula coloca a pasta no **começo** do PATH (`$HOME/python3.14t/bin:$PATH`). Como essa pasta também tem um `python3`, ele substituiria o Python com GIL. Por isso aqui a pasta vai no **final**.

### Conferir os dois Pythons

```bash
python3     -c "import sys; print(sys.version); print('GIL:', sys._is_gil_enabled())"
python3.14t -c "import sys; print(sys.version); print('GIL:', sys._is_gil_enabled())"
```

| Comando | Versão | GIL |
|---|---|---|
| `python3` | 3.14.4 | `True` |
| `python3.14t` | 3.14.7 free-threading | `False` |

---

## 🌐 3. IO-bound: sequencial × asyncio

Simula a consulta do preço de um produto em 5 lojas que demoram 1; 2; 3; 1,5 e 2,5 s para responder.

```bash
cd IO-Bound
python3 sequencial_io.py   # ~10 s  (soma das esperas)
python3 concorrente.py     # ~3 s   (espera da loja mais lenta)
```

| Versão | Tempo (s) | Speedup |
|---|---|---|
| Sequencial | 10,00 | 1,00 |
| Concorrente (asyncio) | 3,00 | **3,33** |

**Resumo:** no `await asyncio.sleep()` a coroutine **cede a vez** ao *event loop*, que segue com as outras consultas. O `asyncio.gather()` dispara todas juntas. Tudo roda em **uma thread só**: é concorrência, e não paralelismo. Só ajuda quando o programa fica **esperando**.

---

## 🔥 4. CPU-bound: soma dos dígitos de 1 até N

Para cada número de 1 a N, soma os seus dígitos (`numero % 10` pega o último dígito, `numero // 10` o remove) e acumula tudo.

- **N = 40.000.000** → resultado esperado: **1.320.000.004** (todas as versões têm que dar esse valor)
- Complexidade: **O(n log n)**
- Teste rápido: de 1 a 99 o resultado é **900**

```bash
cd CPU-Bound
python3 exemplo_pequeno.py     # mostra a conta número por número (N = 12 → 51)
```

### 3a: Sequencial

```bash
python3 sequencial.py          # com GIL  → 15,15 s
python3.14t sequencial.py      # sem GIL  → 15,92 s (sem GIL é um pouco mais lento com 1 thread)
```

### 3b: Threads (com e sem GIL)

O programa pergunta o número de threads: digite **1, 2, 4 e 8**.

```bash
python3 threads.py             # COM GIL
python3.14t threads.py         # SEM GIL
```

### 3c: Multiprocessing

```bash
python3 processos.py           # digite 1, 2, 4 e 8
```

### 3d: OpenMP em C

```bash
gcc -fopenmp openmp.c -o openmp   # compila (sem mensagem = sucesso)
./openmp                          # digite 1, 2, 4 e 8
```

---

## 📊 5. Resultados

**Speedup** = tempo com 1 thread ÷ tempo com N  ·  **Eficiência** = speedup ÷ N

### Tempo (s)

| N | Threads com GIL | Threads sem GIL | Multiprocessing | OpenMP (C) |
|---|---|---|---|---|
| 1 | 15,66 | 16,25 | 15,89 | 0,9500 |
| 2 | 13,65 | 11,29 | 9,84 | 0,5134 |
| 4 | 13,87 | 8,18 | 6,79 | 0,3722 |
| 8 | 13,90 | 7,32 | 5,85 | **0,2735** |

### Speedup

| N | Threads com GIL | Threads sem GIL | Multiprocessing | OpenMP (C) | Ideal |
|---|---|---|---|---|---|
| 2 | 1,15 | 1,44 | 1,61 | 1,85 | 2 |
| 4 | 1,13 | 1,99 | 2,34 | 2,55 | 4 |
| 8 | 1,13 | 2,22 | 2,72 | **3,47** | 8 |

### Eficiência

| N | Threads com GIL | Threads sem GIL | Multiprocessing | OpenMP (C) |
|---|---|---|---|---|
| 2 | 57,4% | 72,0% | 80,7% | 92,5% |
| 4 | 28,2% | 49,7% | 58,5% | 63,8% |
| 8 | 14,1% | 27,7% | 33,9% | 43,4% |

### O que concluir

- **Threads com GIL:** quase nenhum ganho. Só uma thread executa Python por vez.
- **Threads sem GIL:** o tempo cai a cada aumento, porque agora há paralelismo de verdade.
- **Multiprocessing:** a melhor opção em Python. Cada processo tem o seu próprio interpretador e o seu próprio GIL.
- **OpenMP (C):** cerca de **16× mais rápido** que Python já com 1 thread (compilado × interpretado), e **~55×** com 8 threads.
- Ninguém chega ao ideal: há custos para criar threads e processos, a frequência da CPU cai com todos os núcleos ocupados, são só 4 núcleos físicos e o Linux roda no WSL2.

---

## 🧠 6. Conceitos-chave (para explicar ao professor)

| Conceito | Em uma frase |
|---|---|
| **IO-bound** | Passa a maior parte do tempo **esperando** (rede, disco); a CPU fica ociosa. |
| **CPU-bound** | Passa o tempo todo **calculando**; a CPU fica 100% ocupada. |
| **asyncio** | Concorrência em **1 thread**: enquanto uma tarefa espera (`await`), outra roda. |
| **GIL** | Trava do Python: só **uma thread** executa código Python por vez. |
| **free-threading** | Python compilado com `--disable-gil`: as threads rodam em paralelo. |
| **`resultados.append()`** (threads) | As threads compartilham memória, então uma lista comum funciona. |
| **`Queue`** (processos) | Processos **não** compartilham memória, então os resultados vão por uma fila. |
| **`if __name__ == "__main__":`** | Evita que cada processo filho execute o programa inteiro de novo. |
| **`#pragma omp parallel for`** | O OpenMP divide as voltas do `for` entre as threads sozinho. |
| **`reduction(+:total)`** | Cada thread soma na sua cópia de `total` e o OpenMP junta no fim (evita condição de corrida). |
| **`long long`** | `int` em C vai só até ~2,1 bilhões; o total (1,32 bilhão) fica perto do limite. |
| **Speedup / Eficiência** | `T(1) / T(N)` e `Speedup / N`. |

---

## 🛠️ 7. Erros que aconteceram (e a solução)

| Erro | Causa | Solução |
|---|---|---|
| `pythom: command not found` | Erro de digitação | `python3` (use **Tab** para completar) |
| `python: command not found` | No Ubuntu o comando é `python3` | `python3 arquivo.py` |
| O programa rodou o código **antigo** ou não mostrou nada | O arquivo **não estava salvo** (aba com ●) | `Ctrl+S`; confira o que está no disco com `cat arquivo.py` |
| `AttributeError: ... '_is_gil_enabled'` | Essa função só existe no Python ≥ 3.13 | Use o Python 3.14 |
| `python3.14t: command not found` | Terminal aberto antes de mudar o PATH, ou terminal do PowerShell | `source ~/.bashrc` e use o terminal **Ubuntu (WSL)** |
| `python3.14 ... GIL: True` | O `python3.14` é o do Ubuntu, não o compilado | Use `python3.14t` |
