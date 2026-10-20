"""Testes do fluxo com um LLM falso (sem AWS). Validam orquestração, laço de revisão e saída."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from pipeline.agents.base import Config
from pipeline.agents.revisao import CRITERIOS
from pipeline.legibilidade import contar_silabas, indice_flesch
from pipeline.llm import Chamada
from pipeline.orchestrator import executar, salvar
from pipeline.schemas import (Catalogo, Microaula, Parecer, ResultadoCuradoria,
                              ResultadoPesquisa)

TEMA = "Como atender um cliente irritado no caixa"

AULA = {
    "titulo": TEMA, "objetivo": "Acalmar o cliente e resolver o problema.", "duracao_min": 5,
    "abertura": "A fila está grande. O cliente reclama alto. Você respira fundo.",
    "passos": [
        {"titulo": "Escute sem interromper", "explicacao": "Deixe a pessoa falar. Olhe nos olhos.",
         "exemplo_fala": "Entendo. Me conta o que aconteceu."},
        {"titulo": "Fale com calma", "explicacao": "Use voz baixa e frases curtas."},
        {"titulo": "Chame o líder se precisar", "explicacao": "Você não está sozinho."},
    ],
    "o_que_evitar": ["Discutir.", "Levar para o lado pessoal."],
    "exercicio_situacao": "O cartão do cliente foi recusado e ele grita.",
    "exercicio_resposta_modelo": "Fale baixo. Ofereça outra forma de pagamento.",
    "quiz": [{"pergunta": f"Pergunta {i}?", "alternativas": ["A", "B", "C"], "correta": 0,
              "explicacao": "Porque sim."} for i in range(3)],
    "material_apoio": ["Escute.", "Respire.", "Chame ajuda."],
}


class LLMFalso:
    def __init__(self, reprovar_primeira: bool = True):
        self.revisoes = 0
        self.reprovar_primeira = reprovar_primeira

    def gerar(self, *, agente, modelo, sistema, prompt, saida, trace, temperatura=0.4):
        trace.registrar(Chamada(agente, modelo, 100, 50, 10))
        if saida is ResultadoPesquisa:
            return saida(temas=[{"titulo": t, "publico": "operador de caixa", "problema_real": "x",
                                 "justificativa": "y", "categoria": "atendimento"}
                                for t in (TEMA, "Pix que não cai", "Troca sem nota")])
        if saida is ResultadoCuradoria:
            return saida(ranking=[{"titulo": TEMA, "impacto": 5, "urgencia": 4, "viabilidade": 5,
                                   "comentario": "ok"}], escolhido=TEMA, motivo_escolha="Frequente.")
        if saida is Microaula:
            return saida.model_validate(AULA)
        if saida is Parecer:
            self.revisoes += 1
            ok = not (self.reprovar_primeira and self.revisoes == 1)
            nota = 5 if ok else 3
            return saida(criterios=[{"criterio": c, "nota": nota, "observacao": "-"} for c in CRITERIOS],
                         problemas=[] if ok else ["Frase longa"], sugestoes=[], aprovado=ok)
        if saida is Catalogo:
            return saida(slug="cliente-irritado-caixa", categoria="Atendimento",
                         subcategoria="Conflitos", nivel="basico", publico_alvo=["operador de caixa"],
                         tags=["caixa", "conflito", "atendimento"], resumo_catalogo="Aprenda a acalmar.")
        raise AssertionError(saida)


def test_fluxo_completo_com_laco_de_revisao(tmp_path):
    llm = LLMFalso()
    res = executar(llm, Config(), segmento="supermercados")
    assert res.aprovado
    assert len(res.pareceres) == 2  # reprovou, corrigiu, aprovou
    agentes = [c.agente for c in res.trace.chamadas]
    assert agentes == ["pesquisa", "curadoria", "producao", "revisao", "producao", "revisao", "organizacao"]

    pasta = salvar(res, tmp_path)
    for arq in ("index.html", "microaula.md", "trace.json", "catalogo.json", "pareceres.json"):
        assert (pasta / arq).exists()
    assert TEMA in (pasta / "index.html").read_text(encoding="utf-8")


def test_tema_manual_pula_pesquisa():
    res = executar(LLMFalso(reprovar_primeira=False), Config(), tema=TEMA)
    assert [e.status for e in res.etapas[:2]] == ["pulada", "pulada"]
    assert res.trace.chamadas[0].agente == "producao"


def test_nao_aprova_sem_revisao_humana_apos_limite():
    class SempreReprova(LLMFalso):
        def __init__(self):
            super().__init__(reprovar_primeira=True)
            self.revisoes = -100  # nunca chega a aprovar

        def gerar(self, **kw):
            if kw["saida"] is Parecer:
                kw["trace"].registrar(Chamada("revisao", "m", 1, 1, 1))
                return Parecer(criterios=[{"criterio": "x", "nota": 2, "observacao": "-"}],
                               problemas=["ruim"], sugestoes=[], aprovado=False)
            return super().gerar(**kw)

    res = executar(SempreReprova(), Config(max_rodadas_revisao=2), tema=TEMA)
    assert not res.aprovado and res.catalogo is None
    assert len(res.pareceres) == 3
    assert res.etapas[-1].status == "pulada"


def test_legibilidade():
    assert contar_silabas("cliente") == 3
    facil = "Escute o cliente. Fale com calma. Chame o líder."
    dificil = ("A implementação de estratégias multidimensionais de relacionamento organizacional "
               "pressupõe a internalização sistemática de competências comportamentais transversais.")
    assert indice_flesch(facil) > 70
    assert indice_flesch(dificil) < 25


def test_quiz_rejeita_resposta_inexistente():
    with pytest.raises(ValidationError):
        Microaula.model_validate({**AULA, "quiz": [
            {"pergunta": "?", "alternativas": ["A", "B", "C"], "correta": 3, "explicacao": "-"}] * 3})


def test_slug_vira_nome_de_pasta_seguro():
    c = Catalogo(slug="../Atendimento: Cliente Irritado!", categoria="a", subcategoria="b",
                 nivel="basico", publico_alvo=["x"], tags=["a", "b", "c"], resumo_catalogo="r")
    assert c.slug == "atendimento-cliente-irritado"


def test_revisor_nao_aprova_se_pular_criterio():
    class PulaCriterio(LLMFalso):
        def gerar(self, **kw):
            if kw["saida"] is Parecer:
                kw["trace"].registrar(Chamada("revisao", "m", 1, 1, 1))
                return Parecer(criterios=[{"criterio": "Linguagem simples", "nota": 5, "observacao": "-"}],
                               problemas=[], sugestoes=[], aprovado=True)
            return super().gerar(**kw)

    res = executar(PulaCriterio(), Config(max_rodadas_revisao=0), tema=TEMA)
    assert not res.aprovado
    assert "não avaliados" in res.pareceres[-1][0].problemas[-1]
