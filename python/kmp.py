"""Implementacao didatica do algoritmo Knuth-Morris-Pratt (KMP)."""

from __future__ import annotations


def construir_lps(padrao: str) -> list[int]:
    """Constroi a tabela LPS (longest proper prefix that is also suffix)."""
    lps = [0] * len(padrao)
    tamanho_prefixo = 0
    i = 1

    while i < len(padrao):
        if padrao[i] == padrao[tamanho_prefixo]:
            tamanho_prefixo += 1
            lps[i] = tamanho_prefixo
            i += 1
        elif tamanho_prefixo != 0:
            tamanho_prefixo = lps[tamanho_prefixo - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def buscar_kmp(texto: str, padrao: str) -> list[int]:
    """Retorna todas as posicoes em que padrao ocorre dentro de texto."""
    if padrao == "":
        return list(range(len(texto) + 1))

    lps = construir_lps(padrao)
    ocorrencias: list[int] = []
    i = 0
    j = 0

    while i < len(texto):
        if texto[i] == padrao[j]:
            i += 1
            j += 1

            if j == len(padrao):
                ocorrencias.append(i - j)
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

    return ocorrencias


def contar_ocorrencias_kmp(texto: str, padrao: str) -> int:
    """Conta ocorrencias sem expor a lista para os benchmarks."""
    return len(buscar_kmp(texto, padrao))


if __name__ == "__main__":
    exemplo_texto = "ababcabcabababd"
    exemplo_padrao = "ababd"
    print("Texto:", exemplo_texto)
    print("Padrao:", exemplo_padrao)
    print("LPS:", construir_lps(exemplo_padrao))
    print("Ocorrencias:", buscar_kmp(exemplo_texto, exemplo_padrao))
