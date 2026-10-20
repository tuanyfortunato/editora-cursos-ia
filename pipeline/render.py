"""Renderiza a microaula (visão do aluno) e os bastidores do pipeline (visão do editor)."""
from __future__ import annotations

from html import escape as e
from typing import TYPE_CHECKING

from .legibilidade import faixa

if TYPE_CHECKING:
    from .orchestrator import Resultado


def renderizar_markdown(res: "Resultado") -> str:
    a = res.aula
    linhas = [f"# {a.titulo}", "", f"**Objetivo:** {a.objetivo}  ", f"**Duração:** {a.duracao_min} min", "",
              a.abertura, "", "## Passo a passo", ""]
    for i, p in enumerate(a.passos, 1):
        linhas.append(f"{i}. **{p.titulo}**: {p.explicacao}")
        if p.exemplo_fala:
            linhas.append(f"   > “{p.exemplo_fala}”")
    linhas += ["", "## O que evitar", ""] + [f"- {x}" for x in a.o_que_evitar]
    linhas += ["", "## Pratique", "", a.exercicio_situacao, "", f"**Resposta-modelo:** {a.exercicio_resposta_modelo}",
               "", "## Quiz", ""]
    for i, q in enumerate(a.quiz, 1):
        linhas.append(f"**{i}. {q.pergunta}**")
        for j, alt in enumerate(q.alternativas):
            marca = "✅" if j == q.correta else "◻️"
            linhas.append(f"- {marca} {alt}")
        linhas += [f"  _{q.explicacao}_", ""]
    linhas += ["## Cartão de bolso", ""] + [f"- {x}" for x in a.material_apoio]
    return "\n".join(linhas) + "\n"


_NIVEL = {"basico": "básico", "intermediario": "intermediário", "avancado": "avançado"}

_CSS = """
:root{--bg:#f6f4ef;--card:#fff;--ink:#1d1d1b;--muted:#5d5a54;--line:#e3dfd6;--accent:#b4400f;
--accent-soft:#fbe9df;--ok:#1f7a4d;--ok-soft:#e2f3ea;--warn:#9a5b00;--warn-soft:#fdf0d8;--skip:#77736b}
@media (prefers-color-scheme:dark){:root{--bg:#161513;--card:#1f1e1b;--ink:#f1eee8;--muted:#aaa59b;
--line:#34322d;--accent:#f08a54;--accent-soft:#3a2418;--ok:#5fcf95;--ok-soft:#173226;--warn:#f2b555;
--warn-soft:#33270f;--skip:#8d887e}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:24px 16px;display:grid;gap:24px;grid-template-columns:1fr}
@media (min-width:920px){.wrap{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)}}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px}
.eyebrow{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0}
h1{font-size:28px;line-height:1.2;margin:6px 0 10px}h2{font-size:20px;margin:28px 0 10px}
.meta{color:var(--muted);font-size:15px;margin:0 0 16px}
.cena{background:var(--accent-soft);border-left:4px solid var(--accent);padding:14px 16px;border-radius:8px}
ol.passos{list-style:none;padding:0;counter-reset:p;margin:0}
ol.passos li{counter-increment:p;position:relative;padding:12px 0 12px 48px;border-bottom:1px solid var(--line)}
ol.passos li::before{content:counter(p);position:absolute;left:0;top:12px;width:34px;height:34px;border-radius:50%;
background:var(--accent);color:#fff;display:grid;place-items:center;font-weight:700}
.fala{display:block;margin-top:6px;font-style:italic;color:var(--muted)}
ul.evitar li::marker{content:"✕  ";color:var(--accent)}
details{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:10px 0}
summary{cursor:pointer;font-weight:600}
.q{border:1px solid var(--line);border-radius:10px;padding:14px;margin:12px 0}
.q fieldset{border:0;margin:0;padding:0}.q legend{font-weight:600;margin-bottom:8px}
.q label{display:flex;gap:10px;align-items:flex-start;padding:8px;border-radius:8px;cursor:pointer}
.q label:hover{background:var(--bg)}.q input{margin-top:5px;accent-color:var(--accent)}
.fb{margin:8px 0 0;font-size:15px;min-height:1em}.fb.ok{color:var(--ok)}.fb.no{color:var(--warn)}
.bolso{background:var(--ink);color:var(--bg);border-radius:12px;padding:18px 20px}
.bolso h2{margin-top:0;color:var(--bg)}.bolso li{margin:4px 0}
aside h2{margin-top:0}.etapas{list-style:none;padding:0;margin:0}
.etapas li{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-bottom:1px solid var(--line);font-size:15px}
.pill{font-size:12px;font-weight:700;padding:2px 8px;border-radius:99px;white-space:nowrap}
.concluida{background:var(--ok-soft);color:var(--ok)}.reprovada{background:var(--warn-soft);color:var(--warn)}
.pulada{background:var(--line);color:var(--skip)}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0}
.kpi{border:1px solid var(--line);border-radius:10px;padding:10px;text-align:center}
.kpi b{display:block;font-size:22px}.kpi span{font-size:12px;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:6px 4px;border-bottom:1px solid var(--line);text-align:left}
.nota{font-weight:700;text-align:right}.small{font-size:14px;color:var(--muted)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
"""

_JS = """
document.querySelectorAll('.q').forEach(q=>{
  const c=+q.dataset.correta, fb=q.querySelector('.fb');
  q.querySelectorAll('input').forEach(i=>i.addEventListener('change',()=>{
    const ok=+i.value===c; fb.className='fb '+(ok?'ok':'no');
    fb.textContent=(ok?'Isso mesmo! ':'Ainda não. ')+q.dataset.explicacao;
  }));
});
"""


def renderizar_html(res: "Resultado") -> str:
    a = res.aula
    passos = "".join(
        f"<li><strong>{e(p.titulo)}</strong><br>{e(p.explicacao)}"
        + (f'<span class="fala">“{e(p.exemplo_fala)}”</span>' if p.exemplo_fala else "")
        + "</li>" for p in a.passos)
    evitar = "".join(f"<li>{e(x)}</li>" for x in a.o_que_evitar)
    quiz = ""
    for i, q in enumerate(a.quiz):
        alts = "".join(
            f'<label><input type="radio" name="q{i}" value="{j}"> <span>{e(alt)}</span></label>'
            for j, alt in enumerate(q.alternativas))
        quiz += (f'<div class="q" data-correta="{q.correta}" data-explicacao="{e(q.explicacao)}">'
                 f'<fieldset><legend>{i + 1}. {e(q.pergunta)}</legend>{alts}</fieldset>'
                 f'<p class="fb" aria-live="polite"></p></div>')
    bolso = "".join(f"<li>{e(x)}</li>" for x in a.material_apoio)

    rotulo = {"concluida": "concluída", "reprovada": "reprovada", "pulada": "pulada"}
    etapas = "".join(
        f'<li><span class="pill {s.status}">{rotulo.get(s.status, s.status)}</span>'
        f'<span><strong>{e(s.nome)}</strong><br><span class="small">{e(s.detalhe)}</span></span></li>'
        for s in res.etapas)
    parecer, indice = res.pareceres[-1]
    criterios = "".join(
        f"<tr><td>{e(c.criterio)}<br><span class='small'>{e(c.observacao)}</span></td>"
        f"<td class='nota'>{c.nota}/5</td></tr>" for c in parecer.criterios)
    rodadas = len(res.pareceres)
    status = "Aprovada" if res.aprovado else "Aguardando revisão humana"
    catalogo = ""
    if res.catalogo:
        c = res.catalogo
        catalogo = (f"<h2>Catálogo</h2><p class='small'>{e(c.categoria)} › {e(c.subcategoria)} · "
                    f"nível {_NIVEL.get(c.nivel, c.nivel)}</p><p>{e(c.resumo_catalogo)}</p>"
                    f"<p class='small'>Tags: {e(', '.join(c.tags))}</p>")

    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(a.titulo)}</title><style>{_CSS}</style></head>
<body><main class="wrap">
<article class="card" aria-labelledby="titulo">
  <p class="eyebrow">Microaula · {a.duracao_min} min</p>
  <h1 id="titulo">{e(a.titulo)}</h1>
  <p class="meta"><strong>Ao final, você vai:</strong> {e(a.objetivo)}</p>
  <p class="cena">{e(a.abertura)}</p>
  <h2>Passo a passo</h2><ol class="passos">{passos}</ol>
  <h2>O que evitar</h2><ul class="evitar">{evitar}</ul>
  <h2>Pratique</h2><p>{e(a.exercicio_situacao)}</p>
  <details><summary>Ver uma boa resposta</summary><p>{e(a.exercicio_resposta_modelo)}</p></details>
  <h2>Teste rápido</h2>{quiz}
  <section class="bolso" aria-labelledby="bolso"><h2 id="bolso">Cartão de bolso</h2><ul>{bolso}</ul></section>
</article>
<aside class="card" aria-labelledby="bastidores">
  <p class="eyebrow">Bastidores da editora</p>
  <h2 id="bastidores">{e(status)}</h2>
  <div class="kpis">
    <div class="kpi"><b>{indice}</b><span>legibilidade ({e(faixa(indice))})</span></div>
    <div class="kpi"><b>{rodadas}</b><span>rodada(s) de revisão</span></div>
    <div class="kpi"><b>{len(res.trace.chamadas)}</b><span>chamadas de IA</span></div>
  </div>
  <h2>Linha de produção</h2><ul class="etapas">{etapas}</ul>
  <h2>Parecer do revisor</h2><table>{criterios}</table>
  {catalogo}
  <p class="small">{res.trace.total_tokens:,} tokens · {res.duracao_s}s · gerado em {e(res.gerado_em[:16].replace('T', ' '))} UTC</p>
</aside>
</main><script>{_JS}</script></body></html>
"""
