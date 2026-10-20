from __future__ import annotations

from ..llm import LLM, Trace, dump
from ..schemas import Catalogo, Microaula
from .base import Config, carregar_prompt


def organizar(llm: LLM, cfg: Config, trace: Trace, *, aula: Microaula) -> Catalogo:
    return llm.gerar(
        agente="organizacao", modelo=cfg.modelo_rapido, sistema=carregar_prompt("organizacao"),
        prompt=f"Microaula aprovada:\n{dump(aula)}", saida=Catalogo, trace=trace, temperatura=0.1,
    )
