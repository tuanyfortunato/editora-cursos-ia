"""Linha de produção editorial: pesquisa → curadoria → produção ⇄ revisão → organização.

Uso:
    # Fluxo completo, a partir de um segmento do varejo
    python -m pipeline.orchestrator --segmento "supermercados"

    # Tema já definido (pula pesquisa e curadoria)
    python -m pipeline.orchestrator --tema "Como atender um cliente irritado no caixa" \
        --publico "operador de caixa"
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import agents
from .agents.base import RAIZ, Config
from .llm import LLM, Trace
from .schemas import Catalogo, Microaula, Parecer, ResultadoCuradoria, ResultadoPesquisa


@dataclass
class Etapa:
    nome: str
    status: str  # concluida | pulada | reprovada
    detalhe: str = ""


@dataclass
class Resultado:
    aula: Microaula
    catalogo: Catalogo | None
    pareceres: list[tuple[Parecer, float]]
    pesquisa: ResultadoPesquisa | None
    curadoria: ResultadoCuradoria | None
    etapas: list[Etapa]
    trace: Trace
    duracao_s: float
    gerado_em: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def aprovado(self) -> bool:
        return bool(self.pareceres) and self.pareceres[-1][0].aprovado


def executar(llm: LLM, cfg: Config, *, segmento: str | None = None, tema: str | None = None,
             publico: str = "profissionais de loja", catalogo_existente: list[str] | None = None) -> Resultado:
    if not segmento and not tema:
        raise ValueError("Informe --segmento ou --tema.")

    trace, etapas = Trace(), []
    inicio = time.perf_counter()
    pesquisa = curadoria = None
    contexto = ""

    if tema:
        etapas += [Etapa("Pesquisa", "pulada", "Tema definido manualmente"),
                   Etapa("Curadoria", "pulada", "Tema definido manualmente")]
    else:
        pesquisa = agents.pesquisar(llm, cfg, trace, segmento=segmento)
        etapas.append(Etapa("Pesquisa", "concluida", f"{len(pesquisa.temas)} temas candidatos"))
        curadoria = agents.curar(llm, cfg, trace, pesquisa=pesquisa, catalogo_existente=catalogo_existente)
        etapas.append(Etapa("Curadoria", "concluida", f"Escolhido: {curadoria.escolhido}"))
        tema = curadoria.escolhido
        escolhido = next((t for t in pesquisa.temas if t.titulo == tema), None)
        if escolhido:
            publico = escolhido.publico
            contexto = f"{escolhido.problema_real} {escolhido.justificativa}"

    aula = agents.produzir(llm, cfg, trace, tema=tema, publico=publico, contexto=contexto)
    etapas.append(Etapa("Produção", "concluida", "Versão 1"))

    pareceres: list[tuple[Parecer, float]] = []
    for rodada in range(1, cfg.max_rodadas_revisao + 2):
        parecer, indice = agents.revisar(llm, cfg, trace, aula=aula)
        pareceres.append((parecer, indice))
        etapas.append(Etapa(
            "Revisão", "concluida" if parecer.aprovado else "reprovada",
            f"Rodada {rodada} · legibilidade {indice}",
        ))
        if parecer.aprovado or rodada > cfg.max_rodadas_revisao:
            break
        aula = agents.produzir(llm, cfg, trace, tema=tema, publico=publico, contexto=contexto,
                               versao_anterior=aula, parecer=parecer)
        etapas.append(Etapa("Produção", "concluida", f"Versão {rodada + 1} (com correções)"))

    catalogo = None
    if pareceres[-1][0].aprovado:
        catalogo = agents.organizar(llm, cfg, trace, aula=aula)
        etapas.append(Etapa("Organização", "concluida", f"Categoria: {catalogo.categoria}"))
    else:
        etapas.append(Etapa("Organização", "pulada", "Aguardando revisão humana"))

    return Resultado(aula, catalogo, pareceres, pesquisa, curadoria, etapas, trace,
                     round(time.perf_counter() - inicio, 1))


def salvar(res: Resultado, destino: Path) -> Path:
    from .render import renderizar_html, renderizar_markdown

    slug = res.catalogo.slug if res.catalogo else "rascunho-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    pasta = destino / slug
    pasta.mkdir(parents=True, exist_ok=True)

    def grava(nome: str, dados) -> None:
        (pasta / nome).write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    grava("microaula.json", res.aula.model_dump())
    if res.catalogo:
        grava("catalogo.json", res.catalogo.model_dump())
    if res.pesquisa:
        grava("pesquisa.json", res.pesquisa.model_dump())
    if res.curadoria:
        grava("curadoria.json", res.curadoria.model_dump())
    grava("pareceres.json", [{"legibilidade": i, **p.model_dump()} for p, i in res.pareceres])
    grava("trace.json", {
        "gerado_em": res.gerado_em, "duracao_s": res.duracao_s, "aprovado": res.aprovado,
        "total_tokens": res.trace.total_tokens,
        "etapas": [e.__dict__ for e in res.etapas], "chamadas": res.trace.como_dict(),
    })
    (pasta / "microaula.md").write_text(renderizar_markdown(res), encoding="utf-8")
    (pasta / "index.html").write_text(renderizar_html(res), encoding="utf-8")
    return pasta


def main() -> None:
    try:
        from dotenv import load_dotenv
        load_dotenv(RAIZ / ".env")
    except ImportError:
        pass
    from .llm import BedrockLLM

    ap = argparse.ArgumentParser(description="Editora inteligente de microcursos")
    ap.add_argument("--segmento", help="Segmento do varejo para pesquisar temas")
    ap.add_argument("--tema", help="Tema já definido (pula pesquisa e curadoria)")
    ap.add_argument("--publico", default="operador de caixa")
    ap.add_argument("--saida", default=str(RAIZ / "demo" / "output"))
    args = ap.parse_args()

    res = executar(BedrockLLM(), Config(), segmento=args.segmento, tema=args.tema, publico=args.publico)
    pasta = salvar(res, Path(args.saida))
    status = "APROVADA" if res.aprovado else "PENDENTE DE REVISÃO HUMANA"
    print(f"\n✔ Microaula {status}: {res.aula.titulo}")
    print(f"  {len(res.trace.chamadas)} chamadas · {res.trace.total_tokens} tokens · {res.duracao_s}s")
    print(f"  Abra: {pasta / 'index.html'}")


if __name__ == "__main__":
    main()
