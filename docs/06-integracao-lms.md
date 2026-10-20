# Integração com o LMS

Esse é o ponto com mais incerteza, porque tudo depende de qual LMS é e do que ele permite. Por isso a primeira semana do projeto é para entender isso e escolher o caminho.

## Caminhos possíveis

**Pela API do LMS.** Nosso módulo cria e atualiza os cursos direto no LMS. É o melhor cenário quando o LMS é próprio ou tem API documentada (o Moodle, por exemplo, tem).

**Pacote SCORM.** Cada curso é exportado num pacote padrão que o LMS importa. Funciona com quase todo LMS de mercado, mesmo sem API, mas a atualização dos cursos fica menos automática.

**xAPI.** O conteúdo fica hospedado com a gente e manda o progresso dos alunos para o LMS. Vale a pena se o cliente quiser dados de aprendizagem mais detalhados.

**LTI.** O LMS abre o nosso conteúdo como uma ferramenta externa, com login único. Mais trabalhoso, mas mantém o conteúdo independente do LMS.

**Dentro do código do LMS.** Se o LMS foi desenvolvido pelo próprio cliente e houver acesso ao código, o módulo pode ser construído dentro dele.

## O que vou precisar do cliente

- Qual é o LMS e a versão (ou a stack, se for próprio)
- A documentação da API e um ambiente de testes com acesso
- Como o LMS organiza empresas, usuários e cursos
- Uma pessoa técnica de contato do lado deles

## Premissa do prazo

O prazo que passei considera um LMS com API ou suporte a SCORM e um ambiente de testes liberado na primeira semana. Se o caminho for outro, refaço a estimativa depois do diagnóstico.
