# Roteiro de apresentacao: KMP e analise de complexidade

Duracao sugerida: 5 a 8 minutos.

## 1. Abertura (30s)

Apresentar o tema:

- Algoritmo escolhido: Knuth-Morris-Pratt, ou KMP.
- Problema: encontrar ocorrencias de um padrao dentro de um texto.
- Objetivo do trabalho: comparar teoria de complexidade com medicoes praticas em Python e Java.

## 2. Problema resolvido (45s)

Explicar com exemplo simples:

```text
Texto:   ababcabcabababd
Padrao:  ababd
Saida: posicao 10
```

Comentar que a busca ingenua pode repetir muitas comparacoes e ficar cara em entradas desfavoraveis.

## 3. Ideia principal do KMP (1min)

Explicar:

- O KMP evita voltar no texto.
- Quando ha erro de comparacao, ele usa informacao do proprio padrao.
- Essa informacao fica na tabela LPS.

Frase-chave: o texto e percorrido de forma linear.

## 4. Tabela LPS (1min)

Mostrar o exemplo:

```text
Padrao: a a a a a b
LPS:    0 1 2 3 4 0
```

Explicar que a LPS indica o maior prefixo proprio que tambem e sufixo. Isso permite reposicionar o indice do padrao sem desperdicar comparacoes ja feitas.

## 5. Complexidade (1min)

Apresentar:

- Construcao da LPS: `O(m)`.
- Busca no texto: `O(n)`.
- Total: `O(n + m)`.
- Para busca completa: `Theta(n + m)`.
- Memoria auxiliar: `O(m)`.

Conectar com classe P: o problema e resolvido em tempo polinomial, na verdade linear.

## 6. Metodologia experimental (1min)

Explicar:

- Implementacoes em Python e Java.
- Python medido com `time.perf_counter()`.
- Java medido com `System.nanoTime()`.
- Tamanhos: 1.000, 10.000 e 100.000 caracteres.
- Cenarios: melhor, medio e pior caso.
- 30 execucoes por combinacao.
- Resultados salvos em CSV, com media e desvio-padrao.

## 7. Resultados e graficos (1min30s)

Mostrar os graficos gerados:

- Comparacao Python x Java.
- Comparacao entre cenarios.
- Curva teorica normalizada `O(n + m)`.
- Versao com escala logaritmica.

Pontos para comentar:

- O crescimento acompanha uma tendencia linear.
- Java pode ter constantes menores, mas a classe assintotica e a mesma.
- O pior caso aumenta o trabalho pratico, mas nao muda a complexidade.

## 8. Limitacoes e relacao com NP (45s)

Explicar:

- KMP resolve busca exata de um padrao.
- Nao cobre busca aproximada, multiplos padroes ou expressoes regulares complexas.
- A versao de decisao esta em P e tambem em NP, mas nao e NP-completa.

## 9. Conclusao (30s)

Fechar com tres ideias:

- A tabela LPS e o recurso que evita retrabalho.
- O KMP garante `Theta(n + m)`.
- Os experimentos mostram a diferenca entre tempo assintotico e tempo real de execucao em linguagens diferentes.
