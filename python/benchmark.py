"""Benchmark do KMP em Python e geracao de resumo/graficos."""

from __future__ import annotations

import argparse
import csv
import statistics
import time
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from gerar_entradas import CENARIOS, TAMANHOS, gerar_entrada
from kmp import contar_ocorrencias_kmp

RAIZ = Path(__file__).resolve().parents[1]
RESULTADOS = RAIZ / "resultados"
GRAFICOS = RAIZ / "graficos"
CSV_PYTHON = RESULTADOS / "resultados_python.csv"
CSV_JAVA = RESULTADOS / "resultados_java.csv"
CSV_RESUMO = RESULTADOS / "resumo_resultados.csv"

CABECALHO_RAW = [
    "linguagem",
    "tamanho_nome",
    "tamanho_n",
    "cenario",
    "repeticao",
    "padrao_m",
    "ocorrencias",
    "tempo_segundos",
    "tempo_ns",
]

CABECALHO_RESUMO = [
    "linguagem",
    "tamanho_nome",
    "tamanho_n",
    "cenario",
    "padrao_m",
    "execucoes",
    "media_tempo_segundos",
    "desvio_padrao_segundos",
    "media_tempo_ns",
    "desvio_padrao_ns",
]


def executar_benchmark_python(runs: int) -> None:
    RESULTADOS.mkdir(parents=True, exist_ok=True)

    with CSV_PYTHON.open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=CABECALHO_RAW)
        writer.writeheader()

        for tamanho_nome in TAMANHOS:
            for cenario in CENARIOS:
                entrada = gerar_entrada(tamanho_nome, cenario)

                # Aquecimento simples fora das medicoes registradas.
                contar_ocorrencias_kmp(entrada.texto, entrada.padrao)

                for repeticao in range(1, runs + 1):
                    inicio = time.perf_counter()
                    ocorrencias = contar_ocorrencias_kmp(entrada.texto, entrada.padrao)
                    fim = time.perf_counter()

                    tempo_segundos = fim - inicio
                    writer.writerow(
                        {
                            "linguagem": "Python",
                            "tamanho_nome": entrada.tamanho_nome,
                            "tamanho_n": entrada.n,
                            "cenario": entrada.cenario,
                            "repeticao": repeticao,
                            "padrao_m": len(entrada.padrao),
                            "ocorrencias": ocorrencias,
                            "tempo_segundos": f"{tempo_segundos:.12f}",
                            "tempo_ns": int(tempo_segundos * 1_000_000_000),
                        }
                    )

    print(f"Benchmark Python salvo em: {CSV_PYTHON}")


def _ler_csvs_existentes() -> list[dict[str, str]]:
    linhas: list[dict[str, str]] = []
    for caminho in (CSV_PYTHON, CSV_JAVA):
        if not caminho.exists():
            continue
        with caminho.open("r", newline="", encoding="utf-8") as arquivo:
            reader = csv.DictReader(arquivo)
            for linha in reader:
                if linha.get("tempo_segundos"):
                    linhas.append(linha)
    return linhas


def calcular_resumo() -> list[dict[str, str]]:
    linhas = _ler_csvs_existentes()
    grupos: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)

    for linha in linhas:
        chave = (linha["linguagem"], linha["tamanho_nome"], linha["cenario"])
        grupos[chave].append(linha)

    resumo: list[dict[str, str]] = []
    for (linguagem, tamanho_nome, cenario), itens in sorted(
        grupos.items(), key=lambda item: (item[0][0], int(item[1][0]["tamanho_n"]), item[0][2])
    ):
        tempos_s = [float(item["tempo_segundos"]) for item in itens]
        tempos_ns = [float(item["tempo_ns"]) for item in itens]
        desvio_s = statistics.stdev(tempos_s) if len(tempos_s) > 1 else 0.0
        desvio_ns = statistics.stdev(tempos_ns) if len(tempos_ns) > 1 else 0.0

        resumo.append(
            {
                "linguagem": linguagem,
                "tamanho_nome": tamanho_nome,
                "tamanho_n": itens[0]["tamanho_n"],
                "cenario": cenario,
                "padrao_m": itens[0]["padrao_m"],
                "execucoes": len(itens),
                "media_tempo_segundos": f"{statistics.mean(tempos_s):.12f}",
                "desvio_padrao_segundos": f"{desvio_s:.12f}",
                "media_tempo_ns": f"{statistics.mean(tempos_ns):.3f}",
                "desvio_padrao_ns": f"{desvio_ns:.3f}",
            }
        )

    RESULTADOS.mkdir(parents=True, exist_ok=True)
    with CSV_RESUMO.open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=CABECALHO_RESUMO)
        writer.writeheader()
        writer.writerows(resumo)

    print(f"Resumo salvo em: {CSV_RESUMO}")
    return resumo


def _agrupar_media(linhas: Iterable[dict[str, str]], campos: tuple[str, ...]) -> dict[tuple[str, ...], float]:
    acumulador: dict[tuple[str, ...], list[float]] = defaultdict(list)
    for linha in linhas:
        chave = tuple(linha[campo] for campo in campos)
        acumulador[chave].append(float(linha["media_tempo_segundos"]))
    return {chave: statistics.mean(valores) for chave, valores in acumulador.items()}


def gerar_graficos(resumo: list[dict[str, str]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib nao esta instalado. Execute: python -m pip install matplotlib")
        return

    if not resumo:
        print("Sem dados reais para gerar graficos. Execute os benchmarks primeiro.")
        return

    GRAFICOS.mkdir(parents=True, exist_ok=True)
    tamanhos = sorted({int(linha["tamanho_n"]) for linha in resumo})

    por_linguagem = _agrupar_media(resumo, ("linguagem", "tamanho_n"))
    plt.figure(figsize=(8, 5))
    for linguagem in sorted({linha["linguagem"] for linha in resumo}):
        y = [por_linguagem.get((linguagem, str(n))) for n in tamanhos]
        plt.plot(tamanhos, y, marker="o", label=linguagem)
    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo medio (segundos)")
    plt.title("Comparacao entre Python e Java")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "comparacao_python_java.png", dpi=160)
    plt.close()

    por_cenario = _agrupar_media(resumo, ("cenario", "tamanho_n"))
    plt.figure(figsize=(8, 5))
    for cenario in sorted({linha["cenario"] for linha in resumo}):
        y = [por_cenario.get((cenario, str(n))) for n in tamanhos]
        plt.plot(tamanhos, y, marker="o", label=cenario)
    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo medio (segundos)")
    plt.title("Comparacao entre melhor, medio e pior caso")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "casos_kmp.png", dpi=160)
    plt.close()

    observados_por_n = _agrupar_media(resumo, ("tamanho_n",))
    y_observado = [observados_por_n[(str(n),)] for n in tamanhos]
    max_observado = max(y_observado)
    curva_teorica = [n + 32 for n in tamanhos]
    max_teorico = max(curva_teorica)
    y_teorico = [(valor / max_teorico) * max_observado for valor in curva_teorica]

    plt.figure(figsize=(8, 5))
    plt.plot(tamanhos, y_observado, marker="o", label="Tempo medio observado")
    plt.plot(tamanhos, y_teorico, linestyle="--", label="O(n + m) normalizada")
    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo medio (segundos)")
    plt.title("Tempo observado e curva teorica normalizada")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "curva_teorica.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    for linguagem in sorted({linha["linguagem"] for linha in resumo}):
        y = [por_linguagem.get((linguagem, str(n))) for n in tamanhos]
        plt.plot(tamanhos, y, marker="o", label=linguagem)
    plt.yscale("log")
    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo medio (segundos, escala log)")
    plt.title("Comparacao com escala logaritmica")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAFICOS / "escala_logaritmica.png", dpi=160)
    plt.close()

    print(f"Graficos salvos em: {GRAFICOS}")


def criar_csvs_vazios_se_necessario() -> None:
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    for caminho in (CSV_PYTHON, CSV_JAVA):
        if not caminho.exists():
            with caminho.open("w", newline="", encoding="utf-8") as arquivo:
                csv.writer(arquivo).writerow(CABECALHO_RAW)
    if not CSV_RESUMO.exists():
        with CSV_RESUMO.open("w", newline="", encoding="utf-8") as arquivo:
            csv.writer(arquivo).writerow(CABECALHO_RESUMO)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark do KMP em Python.")
    parser.add_argument("--runs", type=int, default=30, help="Numero de execucoes por combinacao.")
    parser.add_argument("--somente-resumo", action="store_true", help="Nao executa Python; apenas recalcula resumo.")
    parser.add_argument("--graficos", action="store_true", help="Gera graficos a partir do resumo.")
    args = parser.parse_args()

    if args.runs <= 0:
        raise ValueError("--runs deve ser maior que zero")

    criar_csvs_vazios_se_necessario()

    if not args.somente_resumo:
        executar_benchmark_python(args.runs)

    resumo = calcular_resumo()
    if args.graficos:
        gerar_graficos(resumo)


if __name__ == "__main__":
    main()
