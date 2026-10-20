from __future__ import annotations

from ..legibilidade import faixa, indice_flesch
from ..llm import LLM, Trace, dump
from ..schemas import Microaula, Parecer
from .base import Config, carregar_prompt, carregar_rubrica


CRITERIOS = [
    "Linguagem simples", "Precisão", "Aplicabilidade", "Adequação ao público",
    "Segurança", "Avaliação", "Acessibilidade",
]


def texto_para_leitura(m: Microaula) -> str:
    """Texto que o aluno efetivamente lê, para medir legibilidade."""
    blocos = [m.objetivo, m.abertura]
    for p in m.passos:
        blocos += [p.titulo + ".", p.explicacao, p.exemplo_fala or ""]
    blocos += m.o_que_evitar + [m.exercicio_situacao, m.exercicio_resposta_modelo]
    blocos += m.material_apoio
    return "\n".join(b for b in blocos if b)


def revisar(llm: LLM, cfg: Config, trace: Trace, *, aula: Microaula) -> tuple[Parecer, float]:
    indice = indice_flesch(texto_para_leitura(aula))
    sistema = carregar_prompt("revisao") + "\n\n" + carregar_rubrica("revisao")
    prompt = (
        f"Avalie EXATAMENTE estes critérios, com estes nomes: {', '.join(CRITERIOS)}.\n"
        f"Índice de legibilidade Flesch-PT calculado: {indice} ({faixa(indice)}). "
        f"Meta: ≥ {cfg.meta_legibilidade}.\n\nMicroaula:\n{dump(aula)}"
    )
    parecer = llm.gerar(
        agente="revisao", modelo=cfg.modelo_forte, sistema=sistema,
        prompt=prompt, saida=Parecer, trace=trace, temperatura=0.0,
    )
    # Regras duras em código: o LLM não aprova sozinho.
    avaliados = {c.criterio.strip().lower() for c in parecer.criterios}
    faltando = [c for c in CRITERIOS if c.lower() not in avaliados]
    motivos = []
    if indice < cfg.meta_legibilidade:
        motivos.append(f"legibilidade {indice} abaixo da meta {cfg.meta_legibilidade}")
    if any(c.nota < 4 for c in parecer.criterios):
        motivos.append("algum critério com nota menor que 4")
    if faltando:
        motivos.append("critérios não avaliados: " + ", ".join(faltando))
    if motivos:
        if parecer.aprovado:
            parecer.problemas.append("Reprovado por regra automática: " + "; ".join(motivos) + ".")
        parecer.aprovado = False
    return parecer, indice
