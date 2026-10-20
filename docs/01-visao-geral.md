# Visão geral e escopo

## O problema

Quem trabalha na operação do varejo (caixa, reposição, atendimento, estoque) precisa de treinamento o tempo todo, mas tem pouco tempo e nem sempre tem facilidade com leitura ou tecnologia. Produzir esse conteúdo na mão é caro e ele envelhece rápido.

## A proposta

Montar um módulo, ligado ao LMS que já existe, que funcione como uma pequena editora. Agentes de IA cuidam de cada etapa: descobrir o que precisa ser ensinado, escolher o que vem primeiro, escrever a aula, revisar e organizar no catálogo. Os cursos aprovados vão para uma biblioteca geral, e cada empresa escolhe quais quer liberar para o seu pessoal.

Algumas coisas que guiaram as decisões:

- Aula curta (5 a 7 minutos) e prática, pensada para ser usada no turno seguinte.
- Qualidade que dá para medir. Parte da checagem é feita por código, parte pela IA e a palavra final é de uma pessoa.
- Saber sempre de onde cada curso veio, quem revisou e quando foi aprovado.
- Custo sob controle desde o começo, e não como ajuste depois.
- Acessibilidade de verdade: funcionar bem no celular, com leitor de tela e em áudio.

## O que entra no MVP

- Os cinco agentes funcionando em sequência (pesquisa, curadoria, produção, revisão e organização)
- O formato da microaula: uma cena de abertura, o passo a passo, o que evitar, um exercício, um quiz curto e um "cartão de bolso" com o resumo
- Aprovação de uma pessoa antes de qualquer curso ser publicado
- Biblioteca geral com categorias, busca e filtros
- Seleção de cursos por empresa
- Painel para acompanhar as etapas, o status, a qualidade e o custo de cada curso
- Controle de versões e atualização dos cursos
- Integração com o LMS (o formato depende do diagnóstico, ver o doc 06)
- Infraestrutura na AWS descrita em código

## O que fica para depois

Deixei de fora do MVP coisas que fazem sentido, mas que aumentariam muito o prazo: vídeo gerado por IA, personalização das aulas com a marca e os procedimentos de cada empresa, trilhas automáticas, recomendação de cursos por função, outros idiomas e uso dos dados de desempenho dos alunos para orientar a pesquisa.
