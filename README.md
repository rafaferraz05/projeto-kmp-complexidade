# Projeto KMP: Teoria da Complexidade e Analise de Tempo

Este projeto implementa o algoritmo Knuth-Morris-Pratt (KMP) em Python e Java, executa benchmarks com tres tamanhos de entrada e tres cenarios experimentais, salva os resultados em CSV, calcula media e desvio-padrao e gera graficos comparativos.

 Os CSVs deste repositorio contem os resultados reais obtidos nos benchmarks com 30 execucoes por combinacao.

## Estrutura

```text
projeto-kmp-complexidade/
├── README.md
├── python/
│   ├── kmp.py
│   ├── benchmark.py
│   └── gerar_entradas.py
├── java/
│   ├── KMP.java
│   └── BenchmarkKMP.java
├── resultados/
│   ├── resultados_python.csv
│   ├── resultados_java.csv
│   └── resumo_resultados.csv
├── graficos/
│   ├── comparacao_python_java.png
│   ├── casos_kmp.png
│   ├── curva_teorica.png
│   └── escala_logaritmica.png
├── relatorio/
│   └── relatorio.md
├── slides/
│   └── roteiro_apresentacao.md
├── docs/
│   └── referencias.md
└── entradas/
```

## Requisitos

- Windows, Linux ou macOS.
- Python 3.10 ou superior.
- Java JDK 17 ou superior, com `javac` e `java` no PATH.
- Biblioteca Python `matplotlib` para gerar graficos.

Instale o `matplotlib`, se necessario:

```powershell
python -m pip install matplotlib
```

## Como rodar no Windows PowerShell

Entre na pasta do projeto:

```powershell
cd caminho\para\projeto-kmp-complexidade
```

Opcionalmente, gere os arquivos de entrada para conferencia:

```powershell
python .\python\gerar_entradas.py
```

Execute o benchmark em Python, com 30 repeticoes por combinacao:

```powershell
python .\python\benchmark.py --runs 30
```

Compile e execute o benchmark em Java:

```powershell
javac .\java\KMP.java .\java\BenchmarkKMP.java
java -cp .\java BenchmarkKMP 30
```

Depois de gerar os CSVs de Python e Java, calcule o resumo final e crie os graficos:

```powershell
python .\python\benchmark.py --somente-resumo --graficos
```

## Saidas geradas

Os benchmarks criam ou atualizam estes arquivos:

- `resultados/resultados_python.csv`: 270 linhas esperadas, pois sao 3 tamanhos x 3 cenarios x 30 execucoes.
- `resultados/resultados_java.csv`: 270 linhas esperadas.
- `resultados/resumo_resultados.csv`: medias e desvios-padrao agrupados por linguagem, tamanho e cenario.
- `graficos/comparacao_python_java.png`: compara Python e Java por tamanho de entrada.
- `graficos/casos_kmp.png`: compara melhor caso, caso medio e pior caso.
- `graficos/curva_teorica.png`: compara tempos observados com curva normalizada de O(n + m).
- `graficos/escala_logaritmica.png`: versao com eixo Y em escala logaritmica.

## Tamanhos e cenarios

Tamanhos de entrada:

- Pequena: `n = 1.000` caracteres.
- Media: `n = 10.000` caracteres.
- Grande: `n = 100.000` caracteres.

Cenarios:

- Melhor caso: padrao encontrado logo no inicio e texto com baixa repeticao.
- Caso medio: texto e padrao gerados por sequencia pseudoaleatoria deterministica.
- Pior caso: texto com muitas repeticoes de `a` e padrao `aaaaab`, forcando consultas frequentes a tabela LPS.

Mesmo no pior caso, o KMP continua linear: `O(n + m)`, onde `n` e o tamanho do texto e `m` e o tamanho do padrao.

## Observacoes sobre medicao

- O benchmark Python mede apenas a chamada ao KMP usando `time.perf_counter()`.
- O benchmark Java mede apenas a chamada ao KMP usando `System.nanoTime()`.
- A geracao das entradas acontece antes da medicao, para nao contaminar o tempo do algoritmo.
- Cada combinacao de linguagem, tamanho e cenario e executada 30 vezes.
- Pequenas variacoes sao normais por causa de escalonamento do sistema operacional, aquecimento da JVM, cache, frequencia da CPU e processos em segundo plano.

## Comandos uteis

Limpar `.class` gerados pelo Java:

```powershell
Remove-Item .\java\*.class
```

Executar uma versao rapida de teste, com 3 repeticoes:

```powershell
python .\python\benchmark.py --runs 3
javac .\java\KMP.java .\java\BenchmarkKMP.java
java -cp .\java BenchmarkKMP 3
python .\python\benchmark.py --somente-resumo --graficos
```


