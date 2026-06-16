# Relatorio: Teoria da Complexidade e Analise de Tempo do Algoritmo KMP

## 1. Introducao

Este relatorio apresenta um estudo teorico e experimental do algoritmo Knuth-Morris-Pratt (KMP), usado para busca exata de padroes em textos. O objetivo e relacionar a analise assintotica do algoritmo com medicoes empiricas feitas em duas linguagens de programacao: Python e Java.

O experimento mede o tempo de execucao em entradas pequenas, medias e grandes, considerando melhor caso, caso medio e pior caso. Os resultados devem ser obtidos por execucao local dos benchmarks, evitando qualquer valor ficticio.

## 2. Problema resolvido

O problema tratado e a busca de todas as ocorrencias de um padrao `P` dentro de um texto `T`.

- Entrada: texto `T` de tamanho `n` e padrao `P` de tamanho `m`.
- Saida: posicoes em que `P` aparece dentro de `T`.

A busca ingenua pode comparar repetidamente os mesmos caracteres e chegar a `O(nm)` em casos desfavoraveis. O KMP evita esse retrabalho usando uma tabela auxiliar chamada LPS.

## 3. Descricao do algoritmo

O KMP e um algoritmo de casamento de padroes. Sua ideia central e nao voltar o indice do texto quando ocorre uma diferenca entre texto e padrao. Em vez disso, o algoritmo usa informacoes internas do proprio padrao para decidir quantos caracteres do padrao ainda podem ser aproveitados.

O algoritmo tem duas fases:

1. Construcao da tabela LPS do padrao.
2. Varredura do texto usando a tabela LPS para controlar os deslocamentos.

## 4. Logica geral

Durante a busca, existem dois indices:

- `i`: posicao atual no texto.
- `j`: posicao atual no padrao.

Quando `texto[i] == padrao[j]`, ambos avancam. Quando ha divergencia, o indice `i` nao volta. O indice `j` e reposicionado usando `lps[j - 1]`, que informa o maior prefixo do padrao que ainda pode ser aproveitado.

## 5. Pseudocodigo

```text
KMP(texto, padrao):
    lps = construir_lps(padrao)
    i = 0
    j = 0
    ocorrencias = lista vazia

    enquanto i < tamanho(texto):
        se texto[i] == padrao[j]:
            i = i + 1
            j = j + 1

            se j == tamanho(padrao):
                adicionar i - j em ocorrencias
                j = lps[j - 1]
        senao se j != 0:
            j = lps[j - 1]
        senao:
            i = i + 1

    retornar ocorrencias
```

```text
construir_lps(padrao):
    lps = vetor de zeros
    tamanho_prefixo = 0
    i = 1

    enquanto i < tamanho(padrao):
        se padrao[i] == padrao[tamanho_prefixo]:
            tamanho_prefixo = tamanho_prefixo + 1
            lps[i] = tamanho_prefixo
            i = i + 1
        senao se tamanho_prefixo != 0:
            tamanho_prefixo = lps[tamanho_prefixo - 1]
        senao:
            lps[i] = 0
            i = i + 1

    retornar lps
```

## 6. Explicacao da tabela LPS

LPS significa `longest proper prefix that is also suffix`, isto e, maior prefixo proprio que tambem e sufixo. Para cada posicao do padrao, a tabela indica o tamanho do maior trecho inicial do padrao que tambem aparece como final do prefixo analisado.

Exemplo com o padrao `aaaaab`:

```text
padrao: a a a a a b
indice: 0 1 2 3 4 5
LPS:    0 1 2 3 4 0
```

Quando ocorre uma falha depois de varias letras `a`, o algoritmo sabe que parte do prefixo ainda pode ser reutilizada. Isso reduz comparacoes repetidas.

## 7. Analise Big-O

A construcao da tabela LPS percorre o padrao em tempo linear, `O(m)`. A busca percorre o texto em tempo linear, `O(n)`, porque o indice do texto nunca retrocede.

Assim, o tempo total e:

```text
O(n + m)
```

A memoria adicional usada pela tabela LPS e:

```text
O(m)
```

## 8. Analise Big-Omega

Mesmo no melhor caso, o algoritmo precisa pelo menos processar a tabela LPS do padrao. Na busca, se o padrao e encontrado logo no inicio, o tempo observado pode ser muito baixo, mas a implementacao deste projeto continua varrendo o texto inteiro para contar todas as ocorrencias.

Para busca de todas as ocorrencias, o limite inferior e:

```text
Omega(n + m)
```

Se a implementacao parasse na primeira ocorrencia, o melhor caso pratico poderia se aproximar de `Omega(m)` para busca, alem da construcao da LPS.

## 9. Analise Big-Theta

Como o limite superior e o limite inferior sao lineares para a busca completa, o KMP tem:

```text
Theta(n + m)
```

Essa e a caracteristica mais importante do algoritmo: mesmo em entradas desfavoraveis, ele permanece linear.

## 10. Melhor caso

No melhor caso deste projeto, o texto tem baixa repeticao e o padrao aparece logo no inicio. Isso reduz a quantidade de consultas relevantes a tabela LPS, pois ocorrem poucas divergencias custosas.

Entrada usada:

- Texto com caracteres variados.
- Padrao `KMPBUSCAEFICIENTE` no inicio.

## 11. Caso medio

No caso medio, texto e padrao sao gerados por uma sequencia pseudoaleatoria deterministica. Essa escolha permite repetir o experimento nas duas linguagens com entradas de comportamento tipico.

Entrada usada:

- Texto pseudoaleatorio.
- Padrao pseudoaleatorio de tamanho 32.

## 12. Pior caso

No pior caso, o texto e o padrao tem muitos prefixos e sufixos repetidos.

Entrada usada:

- Texto: repeticao de `a`.
- Padrao: `aaaaab`.

Esse cenario forca muitas consultas a tabela LPS. Ainda assim, o algoritmo nao volta no texto e mantem complexidade `O(n + m)`.

## 13. Metodologia experimental

Foram implementadas duas versoes do KMP:

- Python, medindo tempo com `time.perf_counter()`.
- Java, medindo tempo com `System.nanoTime()`.

Foram definidos tres tamanhos de entrada:

| Nome | n |
|---|---:|
| Pequena | 1.000 |
| Media | 10.000 |
| Grande | 100.000 |

Foram definidos tres cenarios:

| Cenario | Descricao |
|---|---|
| Melhor | Padrao no inicio e baixa repeticao |
| Medio | Texto e padrao pseudoaleatorios |
| Pior | Repeticoes de `a` e padrao `aaaaab` |

Cada combinacao de linguagem, tamanho e cenario deve ser executada 30 vezes.

## 14. Ambiente de execucao

Ambiente usado nos testes:

- Sistema operacional: Microsoft Windows 11 Pro 64 bits, versao 10.0.26200.
- Processador: 12th Gen Intel(R) Core(TM) i7-12700K.
- Nucleos e threads: 12 nucleos fisicos e 20 processadores logicos.
- Memoria RAM visivel pelo sistema: aproximadamente 15,8 GB.
- Versao do Python: Python 3.13.0.
- Versao do Java/JDK: OpenJDK 21.0.8 LTS, distribuicao Zulu.
- Data da execucao: 16/06/2026.
- Observacoes sobre processos em segundo plano: os testes foram executados em ambiente de uso normal do Windows, portanto pequenas variacoes podem ocorrer por escalonamento do sistema operacional, cache, aquecimento da JVM e outros processos ativos.

## 15. Protocolo de testes

1. Abrir terminal na pasta do projeto.
2. Executar benchmark Python.
3. Compilar e executar benchmark Java.
4. Recalcular resumo e gerar graficos.
5. Conferir os arquivos CSV e PNG.
6. Registrar o ambiente de execucao no relatorio.

Comandos:

```powershell
python .\python\benchmark.py --runs 30
javac .\java\KMP.java .\java\BenchmarkKMP.java
java -cp .\java BenchmarkKMP 30
python .\python\benchmark.py --somente-resumo --graficos
```

## 16. Resultados

Os resultados abaixo foram obtidos a partir de 30 execucoes para cada combinacao de linguagem, tamanho de entrada e cenario. A tabela foi produzida a partir de `resultados/resumo_resultados.csv`.

| Linguagem | Tamanho | Cenario | m | Execucoes | Media (s) | Desvio-padrao (s) |
|---|---:|---|---:|---:|---:|---:|
| Java | 1.000 | medio | 32 | 30 | 0.000025066667 | 0.000000875070 |
| Java | 1.000 | melhor | 17 | 30 | 0.000026220000 | 0.000005563948 |
| Java | 1.000 | pior | 6 | 30 | 0.000034620000 | 0.000014446820 |
| Java | 10.000 | medio | 32 | 30 | 0.000096453333 | 0.000002592793 |
| Java | 10.000 | melhor | 17 | 30 | 0.000095006667 | 0.000007651321 |
| Java | 10.000 | pior | 6 | 30 | 0.000194326667 | 0.000024398105 |
| Java | 100.000 | medio | 32 | 30 | 0.000159533333 | 0.000004294129 |
| Java | 100.000 | melhor | 17 | 30 | 0.000186650000 | 0.000036330008 |
| Java | 100.000 | pior | 6 | 30 | 0.000341530000 | 0.000083208148 |
| Python | 1.000 | medio | 32 | 30 | 0.000052733334 | 0.000002249342 |
| Python | 1.000 | melhor | 17 | 30 | 0.000050360000 | 0.000003165286 |
| Python | 1.000 | pior | 6 | 30 | 0.000106393333 | 0.000003549253 |
| Python | 10.000 | medio | 32 | 30 | 0.000503966667 | 0.000011732341 |
| Python | 10.000 | melhor | 17 | 30 | 0.000497846667 | 0.000011675667 |
| Python | 10.000 | pior | 6 | 30 | 0.001065696667 | 0.000076054765 |
| Python | 100.000 | medio | 32 | 30 | 0.005020890000 | 0.000090852986 |
| Python | 100.000 | melhor | 17 | 30 | 0.004868503334 | 0.000079471711 |
| Python | 100.000 | pior | 6 | 30 | 0.010360833333 | 0.000271363297 |

Os resultados completos de cada execucao individual estao em `resultados/resultados_python.csv` e `resultados/resultados_java.csv`.

## 17. Analise dos graficos

Os graficos foram gerados a partir dos resultados reais dos benchmarks. Em geral, os dados confirmam a expectativa teorica de crescimento linear do KMP, especialmente na implementacao em Python, em que a passagem de `n = 10.000` para `n = 100.000` produziu aumento proximo de 10 vezes no tempo medio.

No grafico de comparacao entre Python e Java, Java apresentou tempos absolutos menores na maioria dos casos. Isso nao altera a complexidade assintotica do algoritmo, mas indica diferencas de constantes, otimizacoes de runtime e custo de interpretacao. Python manteve comportamento bastante regular, enquanto Java mostrou tempos muito pequenos, mais sensiveis a efeitos de JVM, cache e otimizacao.

No grafico de comparacao dos casos, o pior caso foi mais caro nas duas linguagens. Em Python, para `n = 100.000`, o pior caso teve media de aproximadamente `0.01036 s`, enquanto o melhor caso teve aproximadamente `0.00487 s`. Em Java, o pior caso tambem foi o maior para `n = 100.000`, com media de aproximadamente `0.00034 s`. Isso mostra que o pior caso aumenta a constante de tempo, mas nao muda a classe de complexidade.

O grafico da curva teorica normalizada `O(n + m)` serve para comparar a forma de crescimento, nao os valores absolutos. A curva observada acompanha a tendencia esperada de aumento com o tamanho da entrada. Como `m` e pequeno em todos os testes, o termo dominante e `n`.

O grafico com escala logaritmica ajuda a visualizar melhor as diferencas entre Python e Java, pois os tempos absolutos ficam em faixas diferentes. Essa escala tambem facilita comparar os tres tamanhos de entrada quando ha diferencas grandes entre os valores.

Arquivos esperados:

- `graficos/comparacao_python_java.png`
- `graficos/casos_kmp.png`
- `graficos/curva_teorica.png`
- `graficos/escala_logaritmica.png`

## 18. Comparacao Python x Java

Java apresentou tempos menores que Python nos testes executados. Por exemplo, no caso medio com `n = 100.000`, Java teve media de `0.000159533333 s`, enquanto Python teve media de `0.005020890000 s`. No pior caso com `n = 100.000`, Java teve media de `0.000341530000 s`, enquanto Python teve media de `0.010360833333 s`.

Essa diferenca ocorre principalmente porque Java roda sobre a JVM, que pode aplicar otimizacoes em tempo de execucao, enquanto Python tem maior overhead de interpretacao. Porem, o objetivo principal nao e provar que uma linguagem e sempre mais rapida, mas observar que ambas seguem a mesma tendencia assintotica.

A analise deve separar:

- Complexidade assintotica: igual nas duas implementacoes, `Theta(n + m)`.
- Constantes e overheads: diferentes por causa da linguagem, runtime, alocacao e otimizacoes.

Tambem e importante notar que os tempos de Java ficaram muito baixos, principalmente nos casos melhor e medio. Nessa faixa de tempo, pequenas variacoes do ambiente podem influenciar bastante a medicao. Por isso, a comparacao mais importante para Teoria da Complexidade e a tendencia de crescimento, nao apenas o valor absoluto de uma execucao.

## 19. Aplicabilidade

O KMP e util em problemas de busca textual, processamento de strings, analise de arquivos, bioinformatica, ferramentas de busca e qualquer contexto em que seja necessario localizar padroes exatos com garantia de tempo linear.

## 20. Limitacoes

O KMP resolve busca exata de um unico padrao. Ele nao resolve diretamente buscas aproximadas, padroes com expressoes regulares, multiplos padroes simultaneos ou problemas com edicao de caracteres. Para esses casos, outros algoritmos podem ser mais adequados.

## 21. Reflexao sobre classe P

O problema de buscar um padrao exato em um texto pertence a classe P, pois existe um algoritmo deterministico que resolve o problema em tempo polinomial. No caso do KMP, o tempo e linear em relacao ao tamanho da entrada, `O(n + m)`, que e uma forma particularmente eficiente de tempo polinomial.

## 22. Discussao sobre versao NP

Uma versao de decisao do problema poderia ser formulada assim: dado um texto `T` e um padrao `P`, existe pelo menos uma ocorrencia de `P` em `T`? Essa versao tambem esta em P, pois o KMP responde a essa pergunta em tempo linear.

Estar em NP significa que, dada uma solucao candidata, e possivel verifica-la em tempo polinomial. Para a busca de padrao, se alguem fornece uma posicao `i`, basta verificar se `T[i:i+m]` e igual a `P`, o que leva `O(m)`. Portanto, o problema tambem pertence a NP, mas isso nao o torna NP-completo.

## 23. Problemas relacionados a NP-completos

A busca exata de padroes nao e NP-completa, pois ha solucao linear conhecida. Entretanto, existem problemas mais gerais envolvendo strings que podem ficar mais dificeis, dependendo da formulacao, como certas variacoes de alinhamento, busca aproximada com restricoes adicionais, inferencia de padroes e problemas combinatorios sobre sequencias.

Essa comparacao e importante porque mostra que pequenas mudancas na definicao do problema podem alterar bastante sua dificuldade computacional.

## 24. Conclusao

O KMP demonstra como pre-processamento pode melhorar significativamente um algoritmo. Ao construir a tabela LPS, ele evita comparacoes repetidas e garante tempo `Theta(n + m)` para busca completa.

Os experimentos em Python e Java devem confirmar a tendencia linear prevista pela teoria, ainda que os tempos absolutos sejam diferentes por causa das caracteristicas de cada linguagem e ambiente de execucao.
