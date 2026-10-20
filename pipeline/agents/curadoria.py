from __future__ import annotations

from ..llm import LLM, Trace, dump
from ..schemas import ResultadoCuradoria, ResultadoPesquisa
from .base import Config, carregar_prompt


def curar(llm: LLM, cfg: Config, trace: Trace, *, pesquisa: ResultadoPesquisa,
          catalogo_existente: list[str] | None = None) -> ResultadoCuradoria:
    existentes = "\n".join(f"- {t}" for t in (catalogo_existente or [])) or "(biblioteca vazia)"
    prompt = (
        f"Temas candidatos:\n{dump(pesquisa)}\n\n"
        f"Cursos que já existem na biblioteca (evite duplicar):\n{existentes}"
    )
    return llm.gerar(
        agente="curadoria", modelo=cfg.modelo_rapido, sistema=carregar_prompt("curadoria"),
        prompt=prompt, saida=ResultadoCuradoria, trace=trace, temperatura=0.2,
    )
