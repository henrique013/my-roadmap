# Research dump - Headers exchange e metadados de roteamento

## Metadados do Node

- Roadmap de origem: `rabbitmq-exchanges`
- Tema humano do roadmap: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nivel do node: `basico`
- Node ID: `basico/05-headers-e-metadados-de-roteamento`
- Slug do node: `05-headers-e-metadados-de-roteamento`
- Label do node: Headers exchange e metadados de roteamento
- Posicao local: 5 de 6
- Node anterior no nivel para incrementalidade: `basico/04-direct-fanout-e-topic` - Direct, fanout e topic
- Proximo node no nivel: `basico/06-filas-consumidores-e-entrega` - Filas, consumidores e entrega
- Node anterior na sequencia global: `basico/04-direct-fanout-e-topic` - Direct, fanout e topic
- Proximo node na sequencia global: `basico/06-filas-consumidores-e-entrega` - Filas, consumidores e entrega
- Data da pesquisa: 2026-06-08
- Observacoes temporais: a documentacao oficial consultada esta na serie RabbitMQ 4.3 em 2026-06-08. O comportamento central de headers exchange vem do AMQP 0-9-1 e e estavel, mas as variantes `all-with-x` e `any-with-x` foram conferidas na documentacao atual do RabbitMQ.

## Contrato Extraido do Roadmap

- Papel do node na corrente: completa os tipos classicos com roteamento por atributos, util quando uma routing key textual ficaria artificial.
- Papel do nivel no roadmap tri-level: estabilizar fundamentos, vocabulario indispensavel e modelos mentais antes de separar filas, consumidores, acknowledgements e decisoes intermediarias.
- Pre-requisitos herdados:
  - Entender direct, fanout e topic como roteamento por key ou padrao.
  - Entender que o node 04 ja comparou tipos baseados em routing key textual, padrao por segmentos ou copia ampla.
  - Entender que bindings sao regras que conectam a exchange a destinos.
- O que o node introduz pela primeira vez:
  - Headers exchange.
  - `x-match`.
  - Roteamento por headers.
  - Payload opaco para o broker.
- O que deve cobrir:
  - Explicar que headers exchange ignora routing key e avalia headers da mensagem.
  - Diferenciar `x-match=all`, `x-match=any`, `all-with-x` e `any-with-x` em nivel conceitual.
  - Mostrar quando multiplos atributos independentes justificam headers.
  - Reforcar que o broker nao interpreta o payload para rotear.
- O que nao deve cobrir:
  - Nao tratar headers como substituto automatico de topic.
  - Nao cobrir serializers ou payload schema.
  - Nao discutir plugins de exchange especializada ainda.
- Perguntas do node:
  - Por que headers exchange ignora routing key?
  - Quando `topic` e mais legivel que headers?
  - Que risco aparece quando o roteamento depende de headers mal padronizados?
- Vocabulario conceitual:
  - headers exchange
  - message headers
  - `x-match`
  - all
  - any
  - routing by attributes
  - opaque payload
- Exemplos e diagramas permitidos:
  - Cenario conceitual de mensagens com `tenant=acme`, `format=pdf`, `priority=high`.
  - Tabela de escolha entre topic e headers para categorias hierarquicas versus atributos independentes.
- Armadilhas:
  - Criar muitos headers de roteamento sem contrato.
  - Misturar dados de negocio sensiveis em headers usados so para roteamento.
  - Forcar headers quando uma routing key simples resolveria.
- Criterio de dominio: consegue explicar headers exchange sem confundir headers de mensagem com corpo da mensagem ou com routing key textual.
- Handoff: com os tipos classicos cobertos, o proximo node separa definitivamente fila, consumidor, ack e distribuicao de trabalho.
- Referencias especificas herdadas do contrato: F1 e F2 do roadmap, expandidas neste dump com a especificacao AMQP 0-9-1.

## Matriz Anti-Repeticao Aplicavel

- Conteudo ja coberto no node 01:
  - Publisher publica em uma exchange.
  - Exchange roteia e nao armazena como destino final.
  - Filas armazenam mensagens e consumidores recebem de filas.
- Conteudo ja coberto no node 02:
  - A default exchange e uma direct exchange especial.
  - `exchange=""` nao significa ausencia de exchange.
  - A aparente publicacao direta em fila e conveniencia da default exchange.
- Conteudo ja coberto no node 03:
  - Binding e regra de roteamento entre source exchange e destino.
  - Routing key acompanha a publicacao.
  - Binding key e criterio registrado no binding.
  - Uma publicacao pode chegar a zero, um ou varios destinos.
- Conteudo ja coberto no node 04:
  - Direct usa igualdade exata entre routing key e binding key.
  - Fanout ignora routing key e envia copia para todos os destinos ligados.
  - Topic interpreta routing key textual por segmentos e wildcards.
  - `#` pode ampliar demais um binding topic.
- Conteudo que este node adiciona:
  - A exchange pode decidir rota por headers da mensagem em vez da routing key.
  - Os criterios de match ficam nos argumentos do binding.
  - `x-match` define se todos ou qualquer atributo precisam combinar.
  - O corpo da mensagem continua opaco para o broker no roteamento.
  - Headers sao uteis quando os eixos de decisao sao atributos independentes, nao uma hierarquia textual natural.
- Conteudo reservado a nodes futuros:
  - `basico/06-filas-consumidores-e-entrega`: filas, consumidores, acknowledgement, entrega e competicao por trabalho.
  - `intermediario/01-contrato-de-topologia-e-roteamento`: desenho de contratos de topologia e convencoes de rotas.
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: tratamento de mensagens sem rota.
  - `intermediario/05-policies-x-arguments-e-permissoes`: policies, permissoes e governanca ampla de argumentos.
  - `avancado/02-tipos-especializados-e-plugins`: plugins e tipos especializados.
- Exemplos que nao devem ser repetidos:
  - Nao repetir a comparacao completa direct/fanout/topic do node 04.
  - Nao transformar `tenant`, `format` e `priority` em schema de payload ou contrato corporativo completo.
  - Nao usar exemplo operacional com comandos, fila real ou cliente especifico.
- Termos que ainda precisam ser introduzidos neste node:
  - headers exchange, message headers, `x-match`, `all`, `any`, `all-with-x`, `any-with-x`, payload opaco.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentacao oficial  
Data consultada: 2026-06-08  
Versao ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: define exchanges, bindings, argumentos opcionais de binding e exchange, e registra headers como tipo de exchange disponivel no RabbitMQ.  
Topicos cobertos: exchange como roteador, binding, argumentos de binding, exchange type, headers como tipo, x-arguments em exchanges.  
Limites da fonte: a pagina atual lista headers e cita argumentos usados por headers exchange, mas a explicacao detalhada de `x-match` esta melhor no guia de conceitos e na especificacao.

ID: F2  
URL: https://www.rabbitmq.com/tutorials/amqp-concepts  
Tipo: guia oficial  
Data consultada: 2026-06-08  
Versao ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: explica headers exchange, roteamento por multiplos atributos, ignorar routing key, uso de `x-match`, `any`, `all`, `any-with-x` e `all-with-x`, alem de metadados de mensagem e payload opaco.  
Topicos cobertos: headers exchange, message headers, routing key ignorada, `x-match`, atributos de mensagem, payload opaco ao broker.  
Limites da fonte: e um guia conceitual amplo; detalhes normativos de presenca sem valor e regras AMQP originais foram conferidos na especificacao.

ID: F3  
URL: https://www.rabbitmq.com/assets/files/amqp0-9-1-43a54a005e97180a4fbe6e567a125d84.pdf  
Tipo: especificacao  
Data consultada: 2026-06-08  
Versao ou data da fonte, quando relevante: AMQP 0-9-1, PDF publicado pelo RabbitMQ  
Motivo de uso: ancora o comportamento normativo do headers exchange: bindings com tabela de argumentos, headers da mensagem, routing key nao usada, `x-match=all|any`, presenca sem valor e field tables.  
Topicos cobertos: headers exchange type, `x-match`, matching por nome e valor de header, field tables, content header e content body.  
Limites da fonte: a especificacao original descreve `all` e `any` e reserva campos `x-`; as variantes `all-with-x` e `any-with-x` devem seguir a documentacao RabbitMQ atual.

## Sintese por Fonte

F1 permite manter o node dentro do modelo de exchanges e bindings ja usado pelo roadmap. A fonte afirma que exchanges roteiam mensagens para filas, streams ou outras exchanges, que o tipo da exchange e as propriedades do binding implementam a logica de roteamento, e que bindings podem ter um mapa opcional de argumentos usado por alguns tipos, como headers exchange.

F2 fornece a explicacao principal do node: headers exchange e desenhada para rotear por multiplos atributos mais naturais como headers da mensagem do que como routing key. A fonte diz que esse tipo ignora a routing key, usa o atributo `headers`, compara valores de headers com valores especificados no binding e usa `x-match` para decidir se basta qualquer match ou se todos precisam bater. Tambem registra que `any-with-x` e `all-with-x` incluem headers iniciados por `x-` na avaliacao.

F3 confirma a regra de protocolo: uma fila e ligada a uma headers exchange com uma tabela de argumentos, o publisher envia uma mensagem cuja propriedade `headers` contem nomes e valores, e a mensagem vai para a fila se os headers combinarem com os argumentos do binding. A especificacao tambem detalha que um argumento sem valor pode significar presenca de um header de mesmo nome, e que `x-match` controla `all` ou `any`.

## Afirmacoes Tecnicas Importantes

Afirmação: headers exchange roteia por atributos da propriedade `headers` da mensagem, nao pela routing key.  
Base: F2, F3  
Condicao ou limite: o comportamento vale para o tipo headers; outros tipos podem usar ou ignorar a routing key de formas diferentes.  
Impacto didatico: separa o node dos tipos baseados em key textual vistos no node anterior.

Afirmação: os criterios de roteamento de uma headers exchange ficam nos argumentos do binding.  
Base: F1, F2, F3  
Condicao ou limite: o exemplo do HTML usa argumentos conceituais pequenos; governanca ampla de `x-arguments` e policies fica para node intermediario.  
Impacto didatico: mostra que a regra continua sendo topologia, nao logica escondida no consumidor.

Afirmação: uma mensagem combina quando o valor de um header da mensagem e igual ao valor especificado no binding.  
Base: F2, F3  
Condicao ou limite: a especificacao tambem admite argumento sem valor para testar presenca de header, mas o HTML usa principalmente igualdade por valor para manter o basico claro.  
Impacto didatico: permite construir uma tabela pequena de match sem laboratorio.

Afirmação: `x-match=all` exige que todos os pares relevantes combinem, enquanto `x-match=any` aceita uma combinacao de qualquer par relevante.  
Base: F2, F3  
Condicao ou limite: `x-match` e argumento especial do binding; nao e header de negocio.  
Impacto didatico: explica por que a mesma lista de atributos pode ser restritiva ou permissiva.

Afirmação: no RabbitMQ atual, `all` e `any` nao usam headers com prefixo `x-` para avaliar matches, enquanto `all-with-x` e `any-with-x` tambem consideram esses headers.  
Base: F2  
Condicao ou limite: F3 registra a regra AMQP original de reservar `x-`; o HTML deve dizer que as variantes `with-x` sao comportamento documentado no RabbitMQ 4.3.  
Impacto didatico: diferencia as quatro opcoes pedidas sem abrir implementacao de cliente.

Afirmação: o broker pode usar alguns metadados da mensagem, mas o restante e opaco para ele e usado pelas aplicacoes que recebem a mensagem.  
Base: F2  
Condicao ou limite: no recorte deste node, o ponto e que o corpo/payload nao e lido pela exchange para decidir rota.  
Impacto didatico: evita confundir headers de mensagem com payload ou schema do corpo.

## Conceitos Essenciais

Conceito: atributos independentes de roteamento  
Explicacao simples: criterios que nao formam naturalmente uma hierarquia textual unica, como tenant, formato e prioridade.  
Necessidade no node: prepara a necessidade antes de nomear headers exchange.  
Relacao com conceitos anteriores: contrasta com topic, que funciona bem quando a key e segmentada por uma convencao textual legivel.  
Relacao com conceitos futuros: contratos e padronizacao desses atributos ficam para topologia intermediaria.  
Riscos de confusao: transformar todo dado de negocio em header de roteamento.  
Fonte base: F2 e inferencia do contrato do roadmap.

Conceito: message headers  
Explicacao simples: mapa de metadados carregado junto da mensagem, separado do corpo.  
Necessidade no node: e a fonte dos atributos avaliados pela headers exchange.  
Relacao com conceitos anteriores: substitui a routing key como dado lido por este tipo de exchange.  
Relacao com conceitos futuros: nao deve virar discussao de serializers ou schema de payload.  
Riscos de confusao: confundir header com corpo da mensagem ou com qualquer campo interno do broker.  
Fonte base: F2, F3.

Conceito: headers exchange  
Explicacao simples: tipo de exchange que usa headers da mensagem para comparar com argumentos do binding.  
Necessidade no node: e o tema central e completa os tipos classicos do nivel basico.  
Relacao com conceitos anteriores: herda exchange, binding e multiplos destinos; muda o dado usado para match.  
Relacao com conceitos futuros: tipos especializados e plugins ficam fora; headers nao deve virar solucao padrao para tudo.  
Riscos de confusao: tratar headers exchange como topic com sintaxe diferente.  
Fonte base: F2, F3.

Conceito: argumentos do binding  
Explicacao simples: pares nome/valor registrados na ligacao entre exchange e destino, usados por alguns tipos para decidir match.  
Necessidade no node: mostram onde a regra de headers fica registrada.  
Relacao com conceitos anteriores: aprofunda binding sem reensinar source/destination.  
Relacao com conceitos futuros: policies, permissoes e governanca de argumentos ficam no intermediario.  
Riscos de confusao: confundir argumento de binding com argumento de declaracao de exchange ou com payload.  
Fonte base: F1, F2, F3.

Conceito: `x-match`  
Explicacao simples: argumento especial do binding que diz se todos os criterios precisam bater ou se qualquer criterio basta.  
Necessidade no node: sem ele, uma lista de headers fica ambigua.  
Relacao com conceitos anteriores: e o equivalente conceitual da pergunta "como interpretar a regra", mas agora em argumentos de binding.  
Relacao com conceitos futuros: nao abrir policies nem governanca ampla de `x-arguments`.  
Riscos de confusao: tratar `x-match` como header da mensagem em vez de configuracao do binding.  
Fonte base: F2, F3.

Conceito: `all` e `any`  
Explicacao simples: modos de match em que todos os pares precisam combinar ou qualquer par pode combinar.  
Necessidade no node: concretizam como `x-match` muda a seletividade.  
Relacao com conceitos anteriores: semelhante a mudar a amplitude de um padrao topic, mas sem usar segmentos.  
Relacao com conceitos futuros: nao virar linguagem de query.  
Riscos de confusao: achar que `any` significa qualquer header da mensagem, mesmo sem estar no binding.  
Fonte base: F2, F3.

Conceito: `all-with-x` e `any-with-x`  
Explicacao simples: variantes documentadas no RabbitMQ que tambem consideram headers iniciados por `x-` na avaliacao.  
Necessidade no node: o contrato pede diferenciacao conceitual dessas opcoes.  
Relacao com conceitos anteriores: nenhuma direta, alem de manter `x-match` como argumento especial.  
Relacao com conceitos futuros: nao abrir detalhes de protocolo alem da fronteira necessaria.  
Riscos de confusao: usar prefixo `x-` como convencao casual sem contrato.  
Fonte base: F2.

Conceito: payload opaco  
Explicacao simples: o corpo da mensagem nao e interpretado pela exchange para decidir o roteamento.  
Necessidade no node: separa roteamento por header de leitura de conteudo.  
Relacao com conceitos anteriores: preserva a ideia de exchange como roteador de metadados/topologia, nao processador de negocio.  
Relacao com conceitos futuros: serializers e schema de payload ficam fora.  
Riscos de confusao: achar que o broker abre JSON, XML ou binario para escolher fila.  
Fonte base: F2, F3.

## Relacoes Causais e Estruturais

- Atributos independentes -> routing key artificial: quando os criterios nao formam uma hierarquia unica, uma key textual pode ficar longa, instavel ou arbitraria.
- Headers exchange -> routing key ignorada: nesse tipo, o campo de routing key pode existir na publicacao, mas nao participa do match.
- Binding arguments -> regra de match: a exchange compara headers da mensagem contra pares registrados no binding.
- `x-match=all` -> regra restritiva: todos os pares relevantes precisam combinar para que a mensagem seja roteada para aquele destino.
- `x-match=any` -> regra permissiva: um par relevante que combine ja basta para aquele destino entrar na rota.
- `all-with-x` e `any-with-x` -> inclusao de headers `x-`: no RabbitMQ atual, essas variantes tambem avaliam headers iniciados por `x-`.
- Payload opaco -> fronteira de responsabilidade: se a decisao depende de ler o corpo, nao e uma decisao de headers exchange; e desenho de aplicacao ou outro mecanismo fora deste node.
- Headers mal padronizados -> topologia dificil de ler: muitos atributos independentes sem contrato tornam a rota menos previsivel, mesmo quando o mecanismo funciona.

## Exemplos Tecnicos Possiveis

Exemplo: mensagem com headers `tenant=acme`, `format=pdf`, `priority=high`.  
Mudanca ou contraste mostrado: a routing key deixa de ser o centro; a exchange avalia atributos independentes.  
Conceitos introduzidos: message headers, headers exchange, argumentos do binding.  
Risco de escopo: virar schema de payload ou politica multitenant.  
Como manter conceitual: usar tres atributos pequenos e nao discutir origem, seguranca ou contrato corporativo completo.

Exemplo: binding exige `tenant=acme` e `format=pdf` com `x-match=all`.  
Mudanca ou contraste mostrado: a fila so recebe quando todos os criterios registrados combinam.  
Conceitos introduzidos: `x-match`, all.  
Risco de escopo: parecer configuracao executavel.  
Como manter conceitual: mostrar como tabela de leitura, nao comando.

Exemplo: binding aceita `priority=high` ou `format=pdf` com `x-match=any`.  
Mudanca ou contraste mostrado: a mesma familia de atributos pode ser mais permissiva.  
Conceitos introduzidos: any.  
Risco de escopo: sugerir que `any` e sempre melhor por ser flexivel.  
Como manter conceitual: explicitar consequencia de amplitude.

Exemplo condutor escolhido para o HTML: uma mensagem de relatorio chega com `tenant=acme`, `format=pdf`, `priority=high` e corpo opaco. A pagina acompanha como a exchange decide rota usando os headers e como `x-match` muda a seletividade.  
Motivo: o exemplo reduz abstracao, mostra diferenca com routing key textual e nao exige comando, cliente, fila real ou exercicio.

## Obrigacoes de Concretizacao Didatica

Conceito ou relacao: headers da mensagem versus routing key versus payload.  
Tipo de demanda: fronteira  
Primitiva visual escolhida: componente HTML/CSS com tres zonas da publicacao.  
Justificativa da primitiva: a pessoa precisa ver que headers e corpo viajam juntos, mas so os headers participam da decisao da headers exchange.  
Exemplo candidato: routing key ignorada, headers `tenant/format/priority`, payload marcado como opaco.  
Fonte: F2, F3  
Por que a prosa pode nao bastar: sem fronteira visual, o leitor pode concluir que o broker le o corpo.  
Risco de virar laboratorio ou excesso: baixo se nao houver comando nem cliente.  
Como manter conceitual e minimo: mostrar nomes de campos e consequencia, nao API.  
Fronteira com nodes futuros: nao abrir serializers, payload schema, consumidores ou acks.

Conceito ou relacao: argumentos do binding comparados com headers da mensagem.  
Tipo de demanda: estado/contraste  
Primitiva visual escolhida: tabela curta de match.  
Justificativa da primitiva: o mecanismo depende de comparar pares nome/valor; uma tabela e a forma mais direta.  
Exemplo candidato: binding `tenant=acme`, `format=pdf`, `priority=high` versus mensagem com os mesmos headers.  
Fonte: F2, F3  
Por que a prosa pode nao bastar: a palavra "atributos" e abstrata sem ver pares concretos.  
Risco de virar laboratorio ou excesso: medio se parecer configuracao completa.  
Como manter conceitual e minimo: rotular como leitura conceitual e limitar a tres atributos.  
Fronteira com nodes futuros: nao discutir policies, permissoes ou `x-arguments` em geral.

Conceito ou relacao: `x-match=all` versus `x-match=any` e variantes `with-x`.  
Tipo de demanda: contraste  
Primitiva visual escolhida: tabela comparativa.  
Justificativa da primitiva: quatro opcoes com nomes parecidos precisam de leitura lado a lado.  
Exemplo candidato: linhas para `all`, `any`, `all-with-x`, `any-with-x`.  
Fonte: F2, F3  
Por que a prosa pode nao bastar: repetir em paragrafo aumenta risco de trocar inclusao de headers `x-`.  
Risco de virar laboratorio ou excesso: baixo se a tabela explicar sem comando.  
Como manter conceitual e minimo: nao listar bibliotecas, so efeito de match.  
Fronteira com nodes futuros: nao transformar `x-` em convencao de governanca.

Conceito ou relacao: quando topic e mais legivel que headers.  
Tipo de demanda: contraste  
Primitiva visual escolhida: tabela de decisao curta.  
Justificativa da primitiva: o contrato exige nao tratar headers como substituto automatico de topic.  
Exemplo candidato: hierarquia textual `audit.user.login` versus atributos independentes `tenant/format/priority`.  
Fonte: F2 e inferencia a partir do node 04.  
Por que a prosa pode nao bastar: a escolha pode parecer preferencia de estilo sem exemplos comparaveis.  
Risco de virar laboratorio ou excesso: baixo.  
Como manter conceitual e minimo: duas ou tres linhas de decisao.  
Fronteira com nodes futuros: nao abrir contrato de nomenclatura nem governanca completa.

## Riscos, Armadilhas e Erros Comuns

- Achar que headers exchange le o payload: F2 afirma que metadados podem ser usados pelo broker e o restante e opaco; F3 separa content header e content body.
- Tratar `x-match` como header da mensagem: F2 e F3 colocam `x-match` nos argumentos do binding.
- Usar headers quando topic seria mais legivel: inferencia do node 04 e F2; se a classificacao e hierarquica e textual, topic pode ser mais simples.
- Criar muitos headers de roteamento sem contrato: risco derivado do contrato do roadmap e da natureza de multiplos atributos; manter como cuidado, nao como topico de governanca.
- Colocar dado sensivel em header por conveniencia: inferencia de fronteira operacional; o HTML pode mencionar como cuidado curto sem abrir seguranca.
- Misturar a discussao de `x-arguments` de exchanges, policies e permissoes: F1 menciona argumentos opcionais e policies, mas o node atual deve restringir-se a argumentos de binding usados pelo headers exchange.

## Limites e Fora de Escopo

- Este node explica:
  - headers exchange como roteamento por headers da mensagem.
  - routing key ignorada nesse tipo.
  - argumentos do binding como local da regra.
  - `x-match=all`, `x-match=any`, `all-with-x` e `any-with-x` em nivel conceitual.
  - payload opaco para o broker no roteamento.
  - criterio basico para escolher topic ou headers.
- Este node apenas menciona como fronteira:
  - Headers mal padronizados dificultam leitura da topologia.
  - Dados sensiveis em headers exigem cuidado.
  - O proximo node separa fila, consumidor, entrega e ack.
- Este node nao cobre:
  - Serializers, schema de payload, JSON, XML ou formato do corpo.
  - Comandos, cliente de linguagem, UI ou configuracao executavel.
  - Policies, permissoes, operator policies e governanca completa de argumentos.
  - Plugins de exchange especializada.
  - DLX, AE, mandatory, returns, publisher confirms.
  - Consumers, acknowledgements e distribuicao de trabalho.

## Divergencias, Versoes e Notas Temporais

- A documentacao RabbitMQ consultada esta na versao 4.3 e prevalece para as variantes `all-with-x` e `any-with-x`.
- A especificacao AMQP 0-9-1 descreve `x-match` com valores `all` e `any` e diz que campos iniciados por `x-` fora de `x-match` sao reservados/ignorados. A documentacao RabbitMQ 4.3 acrescenta explicitamente `all-with-x` e `any-with-x` para tambem considerar headers `x-` no match.
- Nao ha divergencia sobre o ponto central: headers exchange ignora routing key e usa headers da mensagem comparados com argumentos do binding.
- O HTML deve evitar afirmar que todos os brokers AMQP implementam as variantes `with-x`; a frase deve ficar ancorada em RabbitMQ atual.

## Mapa Fonte -> Topico

| Topico | Fontes | Observacao |
|---|---|---|
| Exchange roteia por tipo e binding | F1, F2 | Base herdada do roadmap. |
| Headers exchange ignora routing key | F2, F3 | Essencial para separar do node 04. |
| Headers da mensagem e metadados | F2, F3 | F2 explica metadados; F3 detalha content header e field tables. |
| Argumentos do binding | F1, F2, F3 | F3 ancora a tabela de argumentos. |
| `x-match=all` e `x-match=any` | F2, F3 | F3 e especificacao; F2 e guia atual. |
| `all-with-x` e `any-with-x` | F2 | Comportamento documentado no RabbitMQ 4.3. |
| Payload opaco para o broker | F2, F3 | F2 da frase didatica; F3 separa header e body. |
| Topic versus headers | F2 e node 04 | Escolha conceitual por hierarquia textual versus atributos independentes. |

## Lacunas Pesquisadas e Resolvidas

Lacuna: headers exchange usa a routing key como fallback?  
Busca feita: guia oficial AMQP concepts e especificacao AMQP 0-9-1.  
Fonte que resolveu: F2, F3.  
Decisao: afirmar que headers exchange ignora routing key; a rota depende dos headers.

Lacuna: `x-match` fica na mensagem ou no binding?  
Busca feita: guia oficial e especificacao.  
Fonte que resolveu: F2, F3.  
Decisao: apresentar `x-match` como argumento especial do binding.

Lacuna: o match exige igualdade de valor ou so presenca do header?  
Busca feita: guia oficial e especificacao.  
Fonte que resolveu: F2, F3.  
Decisao: usar igualdade por valor no HTML principal e registrar no dump que a especificacao tambem admite argumento sem valor para testar presenca.

Lacuna: como diferenciar `all-with-x` e `any-with-x` de `all` e `any`?  
Busca feita: guia oficial RabbitMQ 4.3 e especificacao.  
Fonte que resolveu: F2, com limite temporal em relacao a F3.  
Decisao: explicar que as variantes `with-x` tambem consideram headers iniciados por `x-`, sem generalizar para outros brokers.

Lacuna: o broker interpreta o corpo da mensagem para headers exchange?  
Busca feita: guia oficial e especificacao.  
Fonte que resolveu: F2, F3.  
Decisao: afirmar que o corpo/payload e opaco para o broker no recorte do roteamento.

## Lacunas Remanescentes

Nao ha lacuna remanescente que bloqueie o HTML. A pagina deve preservar os limites: nao abrir serializers, payload schema, policies, permissoes, plugins, consumers, acks, DLX, AE ou laboratorio operacional.

## Ordem de Introducao Conceitual

Conceito: atributos independentes de roteamento  
Necessidade: antes de nomear headers exchange, a pessoa precisa ver por que uma routing key textual pode ficar artificial.  
Explicacao antes do nome: "a decisao depende de tres etiquetas independentes, nao de uma frase hierarquica unica".  
Nomeacao: na abertura da narrativa, antes de `message headers`.  
Depende de: routing key, topic e binding herdados.  
Pode usar depois para: justificar headers exchange.

Conceito: message headers  
Necessidade: nomear o lugar onde esses atributos viajam com a mensagem.  
Explicacao antes do nome: "alem da key e do corpo, a mensagem carrega um mapa de metadados".  
Nomeacao: depois de separar key, mapa de metadados e corpo.  
Depende de: mensagem e publicacao herdadas.  
Pode usar depois para: explicar match da headers exchange.

Conceito: payload opaco  
Necessidade: impedir que o leitor pense que a exchange le o corpo.  
Explicacao antes do nome: "o corpo segue junto, mas nao entra na pergunta de roteamento da exchange".  
Nomeacao: ainda na primeira fronteira visual.  
Depende de: mensagem e message headers.  
Pode usar depois para: limitar serializers e schema.

Conceito: headers exchange  
Necessidade: nomear o tipo que usa headers da mensagem para rotear.  
Explicacao antes do nome: "a exchange passa a comparar os metadados da mensagem com a regra do binding".  
Nomeacao: apos a necessidade por atributos independentes.  
Depende de: message headers, binding.  
Pode usar depois para: explicar routing key ignorada e `x-match`.

Conceito: argumentos do binding  
Necessidade: mostrar onde ficam os criterios que a mensagem precisa satisfazer.  
Explicacao antes do nome: "a ligacao registra pares nome/valor que a exchange vai comparar".  
Nomeacao: antes da tabela de match.  
Depende de: binding e headers exchange.  
Pode usar depois para: explicar `x-match`.

Conceito: `x-match`  
Necessidade: quando ha mais de um par no binding, a exchange precisa saber se exige todos ou aceita qualquer um.  
Explicacao antes do nome: "falta um seletor que diga se a lista e uma conjuncao ou uma alternativa".  
Nomeacao: antes da tabela `all/any`.  
Depende de: argumentos do binding.  
Pode usar depois para: diferenciar `all`, `any`, `all-with-x`, `any-with-x`.

Conceito: `all`  
Necessidade: nomear a regra restritiva de todos os criterios combinarem.  
Explicacao antes do nome: "a fila so entra na rota quando cada par relevante bate".  
Nomeacao: na tabela de `x-match`.  
Depende de: `x-match`.  
Pode usar depois para: explicar decisao restritiva.

Conceito: `any`  
Necessidade: nomear a regra permissiva de qualquer criterio combinar.  
Explicacao antes do nome: "a fila entra na rota quando ao menos um par relevante bate".  
Nomeacao: na tabela de `x-match`, depois de `all`.  
Depende de: `x-match`.  
Pode usar depois para: explicar decisao permissiva.

Conceito: `all-with-x` e `any-with-x`  
Necessidade: cumprir o contrato do node e diferenciar comportamento atual do RabbitMQ.  
Explicacao antes do nome: "alguns headers com prefixo especial podem ficar fora ou dentro da avaliacao conforme a variante escolhida".  
Nomeacao: depois de `all` e `any`.  
Depende de: `x-match`, headers com prefixo `x-`.  
Pode usar depois para: tabela comparativa final.

## Candidatos de Narrativa para o HTML

- Narrativa escolhida: fronteira conceitual e construcao incremental. A pagina abre com uma mensagem que tem criterios independentes (`tenant`, `format`, `priority`) e acompanha onde esses criterios vivem, como a exchange os compara e quando isso e melhor ou pior que topic.
- Narrativa rejeitada: lista seca de opcoes `x-match`. Falharia porque comecaria pelo parametro antes de mostrar a necessidade.
- Narrativa rejeitada: comparacao corretiva "headers nao e payload, nao e topic, nao e routing key". Falharia por abrir em tom negativo.
- Situacao de abertura: uma publicacao precisa separar relatorios por tenant, formato e prioridade. Transformar isso em uma routing key longa deixaria a regra artificial.
- Transformacao acompanhada: a pessoa passa de "key textual decide rota" para "atributos da mensagem podem decidir rota, desde que a regra esteja clara no binding".
- Momento de nomeacao: headers exchange depois de mostrar atributos independentes; `x-match` depois de mostrar uma lista com mais de um criterio.
- Risco de tom corretivo: a fronteira com payload deve aparecer como mecanismo, nao como bronca.

## Necessidades Reais de Visualizacao

- Um componente HTML/CSS separando routing key, headers e payload e necessario para fixar a fronteira.
- Uma tabela de match entre binding e mensagem e necessaria para concretizar nomes e valores.
- Uma tabela de `x-match` e necessaria para diferenciar `all`, `any`, `all-with-x` e `any-with-x` sem ambiguidade.
- Uma tabela curta de escolha topic versus headers e necessaria para evitar a conclusao de que headers substitui topic.
- Nao ha necessidade de ASCII excepcional.
