# Custos

O cliente pediu uma arquitetura "preparada para produção contínua e controle de custos". Na prática, o maior custo variável aqui é o uso dos modelos de IA, então é nele que concentro os cuidados.

## Como o custo fica baixo

**Modelo certo para cada tarefa.** Pesquisa, curadoria e organização usam um modelo mais barato. Só a produção e a revisão, que é onde a qualidade aparece, usam o modelo mais forte.

**Limite de rodadas.** A revisão tem no máximo duas rodadas de correção. Uma aula que não melhora não fica gastando indefinidamente; vai para uma pessoa.

**Cache de prompt.** As instruções dos agentes são longas e se repetem em toda chamada. O Bedrock permite cachear essa parte, o que reduz o custo das chamadas seguintes.

**Processamento em lote.** Quando não há pressa (por exemplo, a atualização de cursos antigos), dá para usar o modo em lote do Bedrock, que costuma sair mais barato que o modo sob demanda.

**Infraestrutura serverless.** Fora da IA, quase tudo é cobrado por uso. Sem produção rodando, o custo fica perto de zero.

## Como o custo é acompanhado

Cada chamada registra o modelo e os tokens usados. Com a tabela de preços do modelo, o painel mostra o custo por curso, por etapa e por mês. Também dá para configurar:

- um teto de gasto por execução, que interrompe a linha se for ultrapassado;
- alertas de orçamento no AWS Budgets;
- um relatório mensal de custo por curso publicado.

## Estimativa

Prefiro não cravar um valor por curso antes de rodar a demo com volume real, porque depende do tamanho dos prompts, de quantas aulas passam de primeira e do modelo escolhido. Depois das primeiras execuções, passo para o cliente o custo médio medido e uma projeção para o volume que ele quer produzir por mês.

Os custos de AWS e de IA são da conta do cliente e ficam fora do valor do desenvolvimento.
