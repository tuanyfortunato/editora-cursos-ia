# Pontos para alinhar com o cliente

Lista do que preciso confirmar antes de fechar escopo, prazo e valor. Os primeiros são os que mais mudam o projeto.

## LMS e integração

- Qual é o LMS? É próprio ou de mercado? Qual versão?
- Tem API para criar e atualizar cursos? Aceita SCORM, xAPI ou LTI?
- Existe ambiente de testes? Quando conseguimos acesso?
- Como o LMS organiza empresas e usuários hoje?
- Quem é a pessoa técnica do LMS para tirar dúvidas?

## Conteúdo

- Quantos cursos por mês vocês esperam produzir no começo? E depois de um ano?
- Algum segmento do varejo é prioridade (supermercado, moda, farmácia, materiais de construção)?
- Quais temas não podem faltar no lançamento?
- Quem vai aprovar os cursos antes de publicar? Vocês têm uma equipe pedagógica?
- Existe especialista para revisar temas sensíveis, como direito do consumidor e segurança?
- Há algum padrão visual, tom de voz ou marca a seguir?
- Só texto no MVP, ou áudio e vídeo também são esperados?
- Existem materiais internos (manuais, procedimentos) que a pesquisa pode usar?

## Empresas clientes

- Quantas empresas usam a plataforma hoje?
- As empresas querem personalizar cursos com os próprios procedimentos ou só escolher do catálogo?
- As empresas querem receber atualizações automaticamente ou aprovar antes?

## Infraestrutura e custos

- Vocês já usam AWS? A solução roda na conta de vocês?
- Os custos de AWS e de IA ficam com vocês, separados do desenvolvimento?
- Existe um orçamento mensal de referência para a operação?

## Dados, segurança e direitos

- Os conteúdos gerados ficam com vocês? (Minha sugestão é que sim.)
- Algum dado de funcionário vai entrar no fluxo? Se sim, precisamos tratar a LGPD.
- Existe exigência de segurança ou auditoria da área de TI de vocês?
- Como fica a responsabilidade pelo conteúdo publicado, já que sempre há aprovação humana antes?

## Projeto

- Quem é o responsável do lado de vocês e com que frequência conseguimos conversar?
- O orçamento cabe nas duas entregas propostas ou preferem começar só pelo diagnóstico?
- Depois do MVP, vão querer suporte e evolução contínuos?

## Premissas que estou assumindo

- LMS com API ou suporte a SCORM e ambiente de testes liberado na primeira semana
- Aprovação humana obrigatória antes de publicar
- Conteúdo em português, só texto e áudio no MVP
- Infraestrutura e custo de IA na conta do cliente

## Riscos

- **Integração com o LMS:** é a maior incerteza; o diagnóstico na primeira semana existe para isso.
- **Precisão do conteúdo:** mitigado com fontes, revisão em três camadas e especialista para temas sensíveis.
- **Gargalo na aprovação humana:** se ninguém do cliente aprovar os cursos, nada é publicado. Precisa de uma pessoa definida para isso.
- **Custo de IA acima do esperado:** mitigado com modelos em camadas, teto por execução e alertas.
