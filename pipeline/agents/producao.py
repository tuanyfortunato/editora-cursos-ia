from __future__ import annotations

from ..llm import LLM, Trace, dump
from ..schemas import Microaula, Parecer
from .base import Config, carregar_prompt


def produzir(llm: LLM, cfg: Config, trace: Trace, *, tema: str, publico: str,
             contexto: str = "", versao_anterior: Microaula | None = None,
             parecer: Parecer | None = None) -> Microaula:
    partes = [f"Tema: {tema}", f"Público principal: {publico}"]
    if contexto:
        partes.append(f"Contexto: {contexto}")
    if versao_anterior and parecer:
        partes.append(
            "Esta é uma NOVA VERSÃO. Corrija todos os pontos do parecer.\n"
            f"Versão anterior:\n{dump(versao_anterior)}\n\nParecer da revisão:\n{dump(parecer)}"
        )
    return llm.gerar(
        agente="producao", modelo=cfg.modelo_forte, sistema=carregar_prompt("producao"),
        prompt="\n\n".join(partes), saida=Microaula, trace=trace, temperatura=0.6,
    )
