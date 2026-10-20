# Como pensei a solução

Os outros documentos explicam o que vai ser feito. Este aqui explica por quê: o raciocínio por trás de cada escolha, as alternativas que considerei e o que pesou na decisão.

## Ponto de partida

Lendo o pedido, ficou claro que o desafio não é fazer a IA escrever um curso. Isso qualquer modelo faz em segundos. O difícil é outra coisa:

1. **Garantir que o conteúdo é bom e correto** para um público que não pode receber informação errada e que, muitas vezes, tem dificuldade de leitura.
2. **Fazer isso de forma contínua**, sem que o custo e o controle saiam da mão conforme o volume cresce.
3. **Encaixar tudo num LMS que já existe** e num modelo de negócio em que várias empresas compartilham a mesma biblioteca.

Quase todas as decisões abaixo partem desses três pontos.

## Por que cinco agentes e não um só

Daria para pedir a um único modelo: "pesquise um tema e escreva um curso". Funcionaria numa demonstração, mas ficaria impossível de controlar. Quando um curso sai ruim, você não sabe se o problema foi o tema, a escrita ou a revisão.

Separando em etapas, cada agente tem uma tarefa clara, um prompt menor e uma saída que dá para conferir. Também dá para usar um modelo mais barato onde a tarefa é simples e um mais caro só onde a qualidade depende disso. E o cliente pediu exatamente isso: acompanhar o status de cada etapa.

## Por que a revisão não fica só com a IA

Pedir para uma IA revisar o texto de outra IA tem um problema conhecido: ela tende a aprovar. Por isso a revisão tem três camadas.

A primeira é código puro. Coisas objetivas, como o gabarito do quiz estar certo ou o texto ser fácil de ler, não precisam de opinião. A legibilidade é medida com o índice de Flesch adaptado para o português, um cálculo conhecido e que não depende do humor do modelo.

A segunda é a IA revisando com uma rubrica fechada, com critérios e notas. E algumas regras ficam no código para que ela não consiga "passar a mão": se qualquer critério tiver nota baixa, a aula é reprovada, mesmo que o revisor diga que está tudo bem.

A terceira é uma pessoa. Nada é publicado sem aprovação humana. Para o MVP, considero isso inegociável: o risco de um conteúdo errado chegar a milhares de funcionários é maior do que o ganho de publicar sem revisão.

## Por que limitar as rodadas de correção

Sem limite, uma aula ruim pode ficar indo e voltando entre produção e revisão, gastando dinheiro sem melhorar. Duas rodadas resolvem a maioria dos casos. O que não resolver, uma pessoa olha.

## Por que esse formato de aula

Pensei em quem vai assistir: alguém no intervalo do turno, pelo celular, que quer saber o que fazer na próxima vez que a situação acontecer.

- **A cena de abertura** faz a pessoa se reconhecer logo de cara.
- **O passo a passo com frases prontas** é o que ela realmente vai usar no balcão.
- **O "o que evitar"** costuma ser tão útil quanto o que fazer.
- **O exercício e o quiz** fixam o conteúdo e geram dado para saber se a aula funcionou.
- **O cartão de bolso** é para lembrar depois, sem precisar ver a aula de novo.

Manter o formato fixo também facilita a revisão, a comparação entre cursos e a exportação para o LMS.

## Por que texto e áudio, e não vídeo

Vídeo gerado por IA chama atenção, mas é caro, demorado de gerar, difícil de revisar e de corrigir. Para o MVP, texto bem escrito com narração em áudio entrega quase todo o valor: funciona em celular simples, gasta pouco dado e atende quem tem dificuldade de leitura. Vídeo fica como evolução, quando o fluxo de qualidade estiver provado.

## Por que a biblioteca guarda uma cópia só de cada curso

A primeira ideia seria copiar o curso para a biblioteca de cada empresa que o escolhe. O problema aparece na primeira correção: seria preciso atualizar dezenas de cópias, e alguma sempre fica para trás.

Guardando o curso uma vez e só a lista de escolhas por empresa, a correção chega para todos de uma vez. Para quem não quer receber mudanças sem conferir, existe a opção de fixar a versão.

## Por que AWS e Bedrock

- O Bedrock dá acesso a vários modelos pela mesma API. Se aparecer um modelo melhor ou mais barato, a troca é uma configuração, não uma reescrita.
- Os dados ficam na conta AWS do cliente, sem passar por serviços de terceiros, o que facilita conversas sobre segurança e LGPD.
- Os outros serviços de que a solução precisa (orquestração, armazenamento, áudio, agendamento) estão no mesmo lugar.
- Além disso, é o ecossistema em que tenho mais experiência e certificação.

## Por que Step Functions e não um framework de agentes

Considerei frameworks como LangGraph e CrewAI. Eles são ótimos para fluxos em que os agentes conversam livremente entre si e decidem o próximo passo. Aqui o fluxo é previsível: as etapas são sempre as mesmas, na mesma ordem.

Para um fluxo assim, o Step Functions entrega de graça o que o cliente pediu: histórico de cada execução, status por etapa, retentativa em caso de falha e a pausa para esperar a aprovação humana, mesmo que ela leve dias. E é um serviço gerenciado, sem servidor para manter. Na demo uso um orquestrador simples em Python para ficar fácil de rodar; ele vira Step Functions no MVP.

## Por que validar os dados entre os agentes

Cada agente devolve um formato fixo, validado com Pydantic. Se o modelo devolver algo fora do esperado, o próprio agente pede a correção antes de seguir. Isso evita que um erro pequeno no começo se espalhe pela linha inteira e torna possível guardar um histórico confiável de cada curso.

## Por que começar pelo diagnóstico do LMS

O pedido fala em integrar com "a plataforma LMS existente", sem dizer qual é. Sem saber se ela tem API, se aceita SCORM ou se é um sistema próprio, qualquer prazo para essa parte seria chute. Prefiro reservar a primeira semana para entender isso e ser transparente sobre essa premissa do que prometer algo que pode não se confirmar.

## Por que esse recorte de MVP

O pedido completo é grande. Tentei separar o que prova o conceito do que pode esperar:

- **Entra:** tudo o que mostra que a linha de produção funciona com qualidade, que a biblioteca atende várias empresas e que o custo está sob controle.
- **Fica para depois:** o que aumenta o valor, mas depende de o básico já estar rodando (vídeo, personalização por empresa, trilhas, recomendação).

Com isso o MVP cabe em seis semanas, com três entregas em que o cliente vê algo funcionando e pode ajustar o rumo cedo.

## O que ainda pode mudar

Essas decisões partem das informações do anúncio. Várias delas dependem das respostas do cliente (ver o doc 09), principalmente sobre o LMS, o volume de cursos e quem vai aprovar o conteúdo. A ideia é revisar este documento depois da primeira conversa.
