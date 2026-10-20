from __future__ import annotations

from ..llm import LLM, Trace
from ..schemas import ResultadoPesquisa
from .base import Config, carregar_prompt


def pesquisar(llm: LLM, cfg: Config, trace: Trace, *, segmento: str, quantidade: int = 5) -> ResultadoPesquisa:
    """Levanta temas candidatos para um segmento do varejo.

    Na demo, a pesquisa usa o conhecimento do modelo. No MVP, este agente
    recebe também fontes externas (notícias do setor, Procon, dúvidas dos
    funcionários na própria plataforma, buscas sem resultado na biblioteca).
    """
    prompt = (
        f"Segmento: {segmento}\n"
        f"Proponha {quantidade} temas de microaula com alta necessidade de capacitação."
    )
    return llm.gerar(
        agente="pesquisa", modelo=cfg.modelo_rapido, sistema=carregar_prompt("pesquisa"),
        prompt=prompt, saida=ResultadoPesquisa, trace=trace, temperatura=0.8,
    )
