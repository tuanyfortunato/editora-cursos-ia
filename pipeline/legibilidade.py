"""Métrica objetiva de legibilidade, calculada em código (não pelo LLM).

Índice Flesch adaptado ao português (Martins et al., 1996):
    248,835 − 1,015 × (palavras/frase) − 84,6 × (sílabas/palavra)

Referência de leitura:
    75–100  muito fácil   (séries iniciais do fundamental)
    50–75   fácil         (fundamental II)
    25–50   difícil       (ensino médio / superior)
     0–25   muito difícil (acadêmico)

Para o público operacional do varejo, a meta é ≥ 50.
"""
from __future__ import annotations

import re

_VOGAIS = "aeiouáéíóúâêôãõàü"
_PALAVRA = re.compile(r"[a-zA-ZÀ-ÿ]+")
_FIM_FRASE = re.compile(r"[.!?…]+|\n+")


def contar_silabas(palavra: str) -> int:
    palavra = palavra.lower()
    total = 0
    for m in re.finditer(f"[{_VOGAIS}]+", palavra):
        g = m.group()
        antes = palavra[m.start() - 1] if m.start() > 0 else ""
        # Hiatos acentuados (ex.: "aí", "saúde")
        total += 1 + len(re.findall(r"[aeo][íú]|[íú][aeo]", g))
        # i/u seguido de a/e/o costuma ser hiato ("cli-en-te", "gi-a"),
        # exceto depois de q/g ("quando", "água", "guerra")
        hiatos = re.findall(r"[iu][aeo]", g)
        if hiatos and antes in "qg" and g[0] == "u":
            hiatos = hiatos[1:]
        total += len(hiatos)
    return max(1, total)


def indice_flesch(texto: str) -> float:
    frases = [f for f in _FIM_FRASE.split(texto) if _PALAVRA.search(f)]
    palavras = _PALAVRA.findall(texto)
    if not frases or not palavras:
        return 0.0
    silabas = sum(contar_silabas(p) for p in palavras)
    valor = 248.835 - 1.015 * (len(palavras) / len(frases)) - 84.6 * (silabas / len(palavras))
    return round(max(0.0, min(100.0, valor)), 1)


def faixa(indice: float) -> str:
    if indice >= 75:
        return "muito fácil"
    if indice >= 50:
        return "fácil"
    if indice >= 25:
        return "difícil"
    return "muito difícil"
