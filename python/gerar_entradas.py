"""Geracao deterministica das entradas usadas nos benchmarks do KMP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TAMANHOS = {
    "pequena": 1_000,
    "media": 10_000,
    "grande": 100_000,
}

CENARIOS = ("melhor", "medio", "pior")
ALFABETO_VARIADO = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
PADRAO_MELHOR = "KMPBUSCAEFICIENTE"
PADRAO_PIOR = "aaaaab"
TAMANHO_PADRAO_MEDIO = 32


@dataclass(frozen=True)
class EntradaKMP:
    tamanho_nome: str
    n: int
    cenario: str
    texto: str
    padrao: str


def _lcg_caracteres(tamanho: int, seed: int, alfabeto: str = ALFABETO_VARIADO) -> str:
    """Gera caracteres por LCG para manter entradas reprodutiveis."""
    estado = seed & 0x7FFFFFFF
    caracteres: list[str] = []

    for _ in range(tamanho):
        estado = (1103515245 * estado + 12345) & 0x7FFFFFFF
        caracteres.append(alfabeto[estado % len(alfabeto)])

    return "".join(caracteres)


def gerar_entrada(tamanho_nome: str, cenario: str) -> EntradaKMP:
    """Gera uma entrada para um tamanho e cenario especificos."""
    if tamanho_nome not in TAMANHOS:
        raise ValueError(f"Tamanho invalido: {tamanho_nome}")
    if cenario not in CENARIOS:
        raise ValueError(f"Cenario invalido: {cenario}")

    n = TAMANHOS[tamanho_nome]

    if cenario == "melhor":
        padrao = PADRAO_MELHOR
        restante = max(0, n - len(padrao))
        texto = padrao + _lcg_caracteres(restante, seed=n + 101, alfabeto="bcdefghijklmnopqrstuvwxyz")
    elif cenario == "medio":
        padrao = _lcg_caracteres(TAMANHO_PADRAO_MEDIO, seed=n * 17 + 13)
        texto = _lcg_caracteres(n, seed=n * 31 + 7)
    else:
        padrao = PADRAO_PIOR
        texto = "a" * n

    return EntradaKMP(tamanho_nome=tamanho_nome, n=n, cenario=cenario, texto=texto, padrao=padrao)


def gerar_todas_as_entradas() -> list[EntradaKMP]:
    entradas: list[EntradaKMP] = []
    for tamanho_nome in TAMANHOS:
        for cenario in CENARIOS:
            entradas.append(gerar_entrada(tamanho_nome, cenario))
    return entradas


def salvar_entradas(diretorio: Path) -> None:
    diretorio.mkdir(parents=True, exist_ok=True)
    for entrada in gerar_todas_as_entradas():
        base = f"{entrada.tamanho_nome}_{entrada.cenario}"
        (diretorio / f"{base}_texto.txt").write_text(entrada.texto, encoding="utf-8")
        (diretorio / f"{base}_padrao.txt").write_text(entrada.padrao, encoding="utf-8")


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    destino = raiz / "entradas"
    salvar_entradas(destino)
    print(f"Entradas salvas em: {destino}")
