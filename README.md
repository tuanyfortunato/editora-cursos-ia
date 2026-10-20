# editora-cursos-ia

Protótipo de uma editora de microcursos para quem trabalha no varejo. Cinco agentes, rodando sobre o Amazon Bedrock, fazem o trabalho de uma linha de produção editorial: pesquisam o que precisa ser ensinado, escolhem o tema, escrevem a aula, revisam e organizam no catálogo.

```
Pesquisa -> Curadoria -> Produção <-> Revisão -> Organização -> Biblioteca
```

Pesquisa, curadoria e organização usam um modelo mais barato. Produção e revisão, que é onde a qualidade aparece, usam um modelo mais forte.

Algumas decisões que tomei:

- Os agentes trocam dados num formato fixo, validado com Pydantic. Se o modelo devolve algo fora do esperado, o próprio agente pede a correção.
- A legibilidade é calculada por código (índice de Flesch adaptado ao português). Se a aula ficar difícil de ler, ela não é aprovada, mesmo que o revisor goste.
- São no máximo duas rodadas de correção. Se não passar, a aula vai para uma pessoa revisar em vez de ser publicada.
- Os prompts e a rubrica de revisão ficam em arquivos (`pipeline/prompts/` e `rubricas/`), versionados junto com o código.
- Cada execução guarda o histórico completo: etapas, modelos, tokens, tempo e pareceres.

A documentação de como seria o projeto completo está em [`docs/`](docs/README.md).

## Como rodar

Você vai precisar de Python 3.11 ou mais novo, credenciais da AWS configuradas e acesso aos modelos liberado no console do Bedrock.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # ajuste a região e os modelos

# Com um tema já definido
python -m pipeline.orchestrator --tema "Como atender um cliente irritado no caixa" --publico "operador de caixa"

# Ou deixando a pesquisa escolher, a partir de um segmento
python -m pipeline.orchestrator --segmento "supermercados"
```

O resultado fica em `demo/output/<nome-do-curso>/`. O arquivo principal é o `index.html`, que mostra a aula do jeito que o funcionário veria e, ao lado, como ela foi produzida. Os outros arquivos (`microaula.json`, `pareceres.json`, `catalogo.json`, `trace.json`) guardam os dados de cada etapa.

## Testes

```bash
pytest
```

Os testes usam um modelo simulado, então rodam sem AWS.
