# Agentes

Cada agente faz uma coisa só. Todos registram qual modelo usaram, quantos tokens gastaram e quanto tempo levaram, o que alimenta o painel e o controle de custo.

## Pesquisa

Levanta o que o pessoal da operação precisa aprender agora. Na demo ele trabalha só com o conhecimento do modelo. No MVP ele passa a receber informação de verdade: o catálogo atual, o que as pessoas procuraram na biblioteca e não acharam, pedidos das empresas e algumas fontes externas escolhidas com o cliente (notícias do setor, Procon, mudanças em meios de pagamento).

O resultado é uma lista de temas, cada um com o público, a situação real que resolve e o motivo de ser relevante. Uma regra importante: nada de "tendência" sem fonte.

## Curadoria

Recebe os temas e decide o que vira aula primeiro. Dá nota de 1 a 5 para impacto, urgência e se o assunto cabe numa aula curta, e evita repetir o que já existe no catálogo. Pelo painel, o editor pode mudar a ordem ou vetar um tema.

## Produção

Escreve a microaula. O formato é sempre o mesmo: abre com uma cena que a pessoa reconhece, segue com 3 a 6 passos práticos (com uma frase pronta para falar, quando faz sentido), o que evitar, um exercício com uma resposta de exemplo, um quiz curto e o cartão de bolso.

As regras de escrita são bem diretas: frases curtas, palavras do dia a dia, falar com "você", exemplos de loja e nenhum número ou regra sem fonte. Quando a aula é reprovada, ele recebe o parecer e reescreve corrigindo cada ponto.

## Revisão

Faz a checagem antes de alguém da equipe gastar tempo com a aula. Avalia sete critérios (linguagem, precisão, aplicabilidade, adequação ao público, segurança, avaliação e acessibilidade) e recebe também um índice de legibilidade que é calculado por código, e não pela IA.

Algumas regras ficam no código de propósito, para não depender do modelo "concordar": a aula é reprovada se a legibilidade ficar abaixo da meta, se qualquer critério tiver nota menor que 4 ou se algum critério não for avaliado. São no máximo duas rodadas de correção. Se ainda não passar, vai para uma pessoa revisar.

## Organização

Prepara o curso aprovado para o catálogo: categoria, subcategoria, nível, público, tags e um resumo curto para a vitrine.

## Próximos agentes que fazem sentido

Um agente de atualização, que relê cursos antigos e sugere uma nova versão quando o assunto muda. Um agente que prepara o roteiro de áudio. E, para temas jurídicos ou de segurança, um verificador de fatos dedicado.
