# Research dump - Contrato de topologia e roteamento

## Metadados do Node

- Roadmap de origem: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: intermediario
- `node_id`: `intermediario/01-contrato-de-topologia-e-roteamento`
- Slug do node: `01-contrato-de-topologia-e-roteamento`
- Label do node: Contrato de topologia e roteamento
- Posição numérica local no nível: 01 de 07
- Node anterior e próximo do mesmo nível para incrementalidade: anterior ausente; próximo `intermediario/02-broadcast-vs-consumidores-competindo`
- Node anterior e próximo na sequência global do roadmap: anterior `basico/06-filas-consumidores-e-entrega`; próximo `intermediario/02-broadcast-vs-consumidores-competindo`
- Data da pesquisa: 2026-06-09
- Observações temporais: documentação oficial consultada na versão RabbitMQ 4.3. O recorte é RabbitMQ 4.3 e AMQP 0-9-1. O protocolo AMQP 0-9-1 citado é a especificação de 13 de novembro de 2008, usada como base estável de modelo.

## Contrato Extraído do Roadmap

- Papel do node na corrente: ensinar a escolher exchanges como contrato entre producers e topologia, reduzindo acoplamento com filas internas.
- Papel do nível no roadmap tri-level: arquitetura, relações, decisões e trade-offs.
- Pré-requisitos herdados: dominar vocabulário básico, tipos clássicos de exchange, bindings, routing keys, filas, consumidores e entrega.
- Introduz pela primeira vez:
  - Contrato de routing key.
  - Ownership de exchange.
  - Fronteira publisher-topology-consumer.
- Deve cobrir:
  - Definir quando o producer deve conhecer uma routing key, mas não a fila final.
  - Estabelecer convenções de nomes de exchanges por domínio ou fluxo.
  - Comparar uma exchange por domínio, por evento, por severidade e por tenant.
  - Explicar como mudanças de consumidores podem ocorrer via bindings sem alterar publishers quando o contrato é estável.
- Não deve cobrir:
  - Não reexplicar tipos básicos; eles são pré-requisito.
  - Não discutir permissões e policies em profundidade; isso fica em node próprio.
  - Não desenhar topologias multi-cluster.
- Perguntas do node:
  - Que parte do contrato pertence ao publisher?
  - Como adicionar um novo consumidor sem mudar o produtor?
  - Quando uma routing key vira contrato público demais?
- Vocabulário conceitual:
  - topology contract
  - event contract
  - exchange ownership
  - routing key convention
  - consumer group queue
- Exemplos e diagramas permitidos:
  - Matriz de decisão com domínio `orders`, routing keys `orders.created` e filas internas por serviço.
  - Cenário de evolução: adicionar auditoria sem redeploy do publisher.
- Armadilhas:
  - Nomear fila como routing key pública quando a fila é detalhe interno.
  - Criar uma exchange por consumidor em vez de por contrato de publicação.
  - Trocar routing key sem plano de compatibilidade.
- Critério de domínio: consegue propor uma topologia onde producers conhecem o contrato de publicação, mas não os nomes das filas consumidoras.
- Handoff: com contrato definido, o próximo node aprofunda a decisão entre broadcast e competição por fila.
- Referências específicas do contrato: F1 `https://www.rabbitmq.com/docs/exchanges`; F3 `https://www.rabbitmq.com/docs/publishers`.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto:
  - O básico já apresentou exchange como entidade de roteamento, bindings, routing keys, direct, fanout, topic, headers, filas, consumers e entrega.
  - O node anterior global já separou exchange, fila e consumer; aqui a fila pode ser usada como detalhe interno de consumo, não como novo assunto.
- Conteúdo reservado a nodes futuros:
  - `intermediario/02-broadcast-vs-consumidores-competindo`: decisão entre várias filas recebendo cópias e vários consumers competindo na mesma fila.
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: falha de rota inicial, mandatory e alternate exchange.
  - `intermediario/04-dead-letter-exchanges-e-retry-conceitual`: saída posterior da fila, DLX e retry.
  - `intermediario/05-policies-x-arguments-e-permissoes`: policies, argumentos opcionais e permissões.
  - `intermediario/06-exchange-to-exchange-bindings`: composição de roteamento entre exchanges.
  - `intermediario/07-publisher-confirms-e-confiabilidade`: aceitação pelo broker, confirms e confiabilidade.
  - `avancado/01-diagnostico-de-roteamento-e-observabilidade`: investigação de incidentes de roteamento.
  - `avancado/05-governanca-e-limites-de-complexidade`: governança ampla de topologia.
- Exemplos que não devem ser repetidos:
  - Não repetir a explicação básica de tipos de exchange.
  - Não repetir a fila `emails` do node anterior como exemplo condutor principal.
  - Não usar exemplos de DLX, alternate exchange, confirms, permissions ou E2E.
- Definições que podem ser tratadas como pré-requisito:
  - Exchange roteia; fila armazena até entrega; consumer processa.
  - Binding liga source exchange a um destino.
  - Routing key é enviada pelo publisher e usada conforme o tipo de exchange.
- Termos que ainda precisam ser introduzidos no HTML:
  - Contrato de publicação.
  - Ownership de exchange.
  - Convenção de routing key.
  - Fila de grupo consumidor.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-09  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta exchange como destino de publicação e entidade que roteia para filas, streams ou outras exchanges por tipo e bindings.  
Tópicos cobertos: exchanges, bindings, routing logic, default exchange, propriedades, durabilidade, optional arguments, alternate exchange como fronteira futura.  
Limites da fonte: cobre comportamento de exchange em geral; não define convenção de domínio da aplicação.

ID: F2  
URL: https://www.rabbitmq.com/docs/publishers  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-09  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta que publishers AMQP 0-9-1 publicam em exchanges e que o broker aceita, roteia e armazena quando há filas.  
Tópicos cobertos: publisher, destination por protocolo, efeitos de resource alarms, unroutable e confirms como fronteiras futuras.  
Limites da fonte: entra em confiabilidade de publicação; neste node isso só aparece como limite, não como explicação central.

ID: F3  
URL: https://www.rabbitmq.com/tutorials/amqp-concepts  
Tipo: guia oficial RabbitMQ  
Data consultada: 2026-06-09  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: consolida o modelo AMQP 0-9-1 de queues, exchanges e bindings, incluindo que aplicações definem entidades e esquemas de roteamento.  
Tópicos cobertos: AMQP entities, protocol programmability, exchanges, routing schemes, default exchange.  
Limites da fonte: é guia conceitual; detalhes operacionais devem ser confirmados em páginas específicas.

ID: F4  
URL: https://www.rabbitmq.com/assets/files/amqp0-9-1-43a54a005e97180a4fbe6e567a125d84.pdf  
Tipo: especificação AMQP 0-9-1  
Data consultada: 2026-06-09  
Versão ou data da fonte: AMQP 0-9-1, 13 de novembro de 2008  
Motivo de uso: sustenta o modelo normativo de exchange como agente de roteamento em um virtual host e a relação routing key, exchange e queue.  
Tópicos cobertos: exchange class, exchange lifecycle, exchange como routing agent, direct exchange, routing key, queue bind.  
Limites da fonte: não cobre extensões modernas do RabbitMQ nem práticas de design de domínio.

ID: F5  
URL: https://www.rabbitmq.com/docs/queues  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-09  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta que queue names existem para aplicações referenciá-las e que server-named queues devem ser conhecidas apenas pela aplicação que as declara, com publishers usando exchanges bem conhecidas.  
Tópicos cobertos: nomes de filas, filas geradas pelo broker, relação com exchanges conhecidas, fronteira fila interna versus contrato público.  
Limites da fonte: foco é fila; neste node ela só sustenta a fronteira do contrato.

ID: F6  
URL: https://www.rabbitmq.com/docs/definitions  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-09  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta que users, vhosts, queues, exchanges, bindings e runtime parameters formam schema, metadata ou topology em RabbitMQ, chamados definitions.  
Tópicos cobertos: topology como metadado, definitions export/import, preconfiguração.  
Limites da fonte: detalhes de export/import não entram no HTML; a fonte apenas justifica a ideia de topologia como artefato explícito.

ID: F7  
URL: https://www.rabbitmq.com/docs/access-control  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-09  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: confirmar que permissions são um tema separado e vhost-scoped, para manter fora de escopo no HTML atual.  
Tópicos cobertos: permissões configure/write/read em vhost.  
Limites da fonte: não deve aparecer como referência visível no HTML deste node para não invadir `intermediario/05`.

## Síntese por Fonte

- F1 permite afirmar que, em AMQP 0-9-1, publishers publicam em exchanges; a finalidade da exchange é rotear mensagens para um ou mais destinos; o tipo da exchange e as propriedades do binding implementam a lógica de roteamento. Também permite afirmar que uma exchange recém-declarada é uma tabela de roteamento vazia até receber bindings.
- F2 permite afirmar que o publisher é uma aplicação que produz mensagens, que em AMQP 0-9-1 a publicação acontece em exchanges, e que o broker aceita mensagens, roteia e armazena se houver fila de destino.
- F3 permite afirmar que AMQP 0-9-1 é programável: aplicações declaram queues/exchanges, definem bindings e esquemas de roteamento. Isso sustenta tratar topologia como decisão de aplicação, não só como detalhe administrativo.
- F4 permite afirmar que a exchange é um agente de roteamento nomeado por virtual host, aceita mensagens e routing information, principalmente routing key, e passa mensagens para queues ou serviços internos. Também sustenta que a direct exchange compara routing key do publisher com routing key do binding.
- F5 permite afirmar que nomes de fila são referências de aplicação, mas filas geradas pelo servidor devem ser internas ao consumidor; publishers devem usar exchanges conhecidas em vez de nomes de fila gerados.
- F6 permite afirmar que queues, exchanges e bindings compõem schema/metadata/topology em RabbitMQ. A topologia pode ser exportada/importada como definitions, mas o HTML não deve virar guia operacional.
- F7 apenas delimita fora de escopo: permissões têm semântica própria e serão tratadas em outro node.

## Afirmações Técnicas Importantes

Afirmação: Em AMQP 0-9-1, o publisher publica em uma exchange, não diretamente em uma fila de domínio, salvo o caso especial da default exchange que parece publicação direta por nome de fila.  
Base: F1, F2, F3, F4  
Condição ou limite: a default exchange tem semântica especial e já foi tratada no básico; este node foca topologias explícitas.  
Impacto didático: sustenta separar o contrato público de publicação dos nomes internos de filas.

Afirmação: A topologia útil para este node é a combinação de exchange, binding, routing key e filas consumidoras.  
Base: F1, F3, F4, F6  
Condição ou limite: policies, permissions, alternate exchanges e E2E existem, mas ficam fora do recorte atual.  
Impacto didático: permite falar em contrato de topologia sem transformar o node em inventário completo de RabbitMQ.

Afirmação: Um producer pode conhecer uma exchange e uma convenção de routing key sem conhecer a fila final, porque bindings conectam a exchange aos destinos.  
Base: F1, F2, F4; inferência declarada: se a exchange recebe a publicação e bindings definem destinos, o publisher não precisa codificar o nome da fila para cada consumidor.  
Condição ou limite: a aplicação que declara ou opera a topologia precisa conhecer filas e bindings; o desacoplamento é do publisher em relação aos consumidores.  
Impacto didático: é o centro do node.

Afirmação: Adicionar um novo consumidor pode ser mudança de topologia quando o contrato de publicação permanece estável: cria-se a fila do consumidor e adiciona-se um binding compatível.  
Base: F1, F3, F5; inferência declarada a partir de bindings como regras de roteamento e filas como destinos.  
Condição ou limite: não entra na escolha entre broadcast e competição; isso fica no próximo node.  
Impacto didático: mostra valor prático do contrato estável.

Afirmação: Usar nome de fila como routing key pública acopla producer a uma implementação de consumo.  
Base: F5 e inferência declarada a partir do contrato do roadmap.  
Condição ou limite: a default exchange pode usar nome de fila como routing key em casos simples; aqui o recorte é topologia explícita de domínio.  
Impacto didático: evita a armadilha principal sem reabrir a aula de default exchange.

Afirmação: Exchange por domínio, evento, severidade ou tenant são recortes possíveis, mas cada um muda ownership, cardinalidade e estabilidade da routing key.  
Base: F1, F3, F6 e inferência de design sobre o contrato de aplicação.  
Condição ou limite: RabbitMQ não impõe uma dessas estratégias; o node deve apresentá-las como critérios, não como regra universal.  
Impacto didático: atende à comparação exigida no contrato sem inventar comportamento do broker.

## Conceitos Essenciais

### Contrato de publicação

- Explicação simples: o conjunto mínimo que o producer precisa respeitar para publicar de forma compreensível para a topologia: exchange alvo, formato da routing key e significado esperado da mensagem.
- Por que é necessário: sem esse contrato, cada consumer tende a vazar para o publisher por nome de fila ou regra interna.
- Relação com conceitos anteriores: usa exchange, binding, routing key e fila já estabelecidos.
- Relação com conceitos futuros: prepara broadcast versus competição, falha de rota e confirms.
- Riscos de confusão: confundir contrato de publicação com contrato de payload inteiro ou com permissão de usuário.
- Fonte base: F1, F2, F3.

### Convenção de routing key

- Explicação simples: regra humana e técnica para formar a string que representa a intenção de roteamento.
- Por que é necessário: o broker trata a routing key conforme o tipo da exchange; a equipe precisa dar significado estável à string.
- Relação com conceitos anteriores: routing key já existe; aqui ganha papel de contrato.
- Relação com conceitos futuros: mudanças e compatibilidade aparecem em alternate exchange e diagnóstico, mas não devem ser aprofundadas agora.
- Riscos de confusão: usar nome de fila ou nome de consumer como se fosse evento de domínio.
- Fonte base: F1, F4, F5.

### Ownership de exchange

- Explicação simples: responsabilidade por nome, semântica, evolução e compatibilidade da exchange.
- Por que é necessário: uma exchange compartilhada sem dono vira ponto de acoplamento difuso.
- Relação com conceitos anteriores: exchange é entidade de roteamento.
- Relação com conceitos futuros: governança ampla fica para nodes avançados; aqui basta ownership mínimo por domínio ou fluxo.
- Riscos de confusão: transformar ownership em discussão de permissão.
- Fonte base: F1, F6; inferência de design.

### Fronteira publisher-topology-consumer

- Explicação simples: divisão entre o que o producer publica, o que a topologia decide e o que cada fila/consumer processa.
- Por que é necessário: é o modelo visual do node.
- Relação com conceitos anteriores: fila e consumer já foram separados no node anterior.
- Relação com conceitos futuros: broadcast/competição aprofunda a parte consumer.
- Riscos de confusão: achar que desacoplar publisher elimina responsabilidade por compatibilidade.
- Fonte base: F1, F2, F5.

### Fila de grupo consumidor

- Explicação simples: fila nomeada para o ponto de consumo de um serviço ou grupo, não para o contrato público de publicação.
- Por que é necessário: permite mostrar a fila como detalhe interno mesmo quando o nome precisa ser estável para a aplicação consumidora.
- Relação com conceitos anteriores: fila acumula e entrega.
- Relação com conceitos futuros: o próximo node decide quando uma fila representa grupo competindo ou quando várias filas recebem cópias.
- Riscos de confusão: antecipar broadcast versus competição.
- Fonte base: F5 e contrato do roadmap.

## Relações Causais e Estruturais

- Se o producer publica em uma exchange com routing key de domínio, então bindings podem ser alterados para adicionar destinos sem mudar a chamada de publicação, desde que a exchange e a routing key continuem compatíveis.
- Se a routing key usa nome de fila, então a fila deixa de ser detalhe interno e vira parte do contrato público; renomear ou dividir consumers passa a pressionar o publisher.
- Se a exchange é por domínio, o contrato tende a favorecer eventos de negócio estáveis; se é por severidade, favorece roteamento por categoria operacional; se é por tenant, aumenta isolamento por cliente, mas também cardinalidade e gestão de topologia.
- Se não há owner claro para a exchange e sua convenção, mudanças de routing key podem quebrar consumers por vias indiretas.
- Se a topologia é tratada como definitions, ela pode ser revisada como artefato, mas o HTML deve preservar a explicação como relação conceitual, sem ensinar export/import.

## Exemplos Técnicos Possíveis

### Exemplo condutor escolhido

- Domínio: pedidos.
- Exchange pública: `orders.events`.
- Routing keys: `orders.created`, `orders.cancelled`.
- Filas internas de consumo: `billing.orders-created`, `audit.orders-events`, `email.orders-notifications`.
- Mudança acompanhada: antes existe billing; depois entra audit via novo binding sem alteração no producer.
- Conceitos introduzidos: contrato de publicação, convenção de routing key, ownership de exchange, fila de grupo consumidor.
- Risco de escopo: pode virar discussão de broadcast versus competição. Controle: dizer apenas que cada fila representa um ponto de consumo e deixar o próximo node decidir cópia versus competição.
- Por que não vira laboratório: não há comandos, client library nem passo a passo; é leitura conceitual de topologia.

### Exemplo complementar

- Matriz de decisão: exchange por domínio, evento, severidade ou tenant.
- Mudança mostrada: como cada recorte escolhe quem é dono do contrato e qual semântica aparece na routing key.
- Risco de escopo: tenant pode puxar isolamento, vhost e permissões. Controle: tratar tenant apenas como recorte de roteamento e cardinalidade.

### Visual de relação material

- Forma: cards HTML/CSS com exchange pública, filas internas e bindings.
- O que mostra: topologia como relação explícita, não como código do publisher.
- Risco: virar decoração. Controle: cada card responde o que o producer conhece, o que consumidores conhecem e onde bindings costuram a relação.

## Obrigações de Concretização Didática

Conceito ou relação: producer conhece exchange e routing key, mas não fila final.  
Tipo de demanda: fronteira e topologia.  
Primitiva visual escolhida: componente HTML/CSS de topologia.  
Justificativa da primitiva: a relação entre publisher, exchange, bindings e filas é espacial; prosa isolada tende a esconder quem conhece quem.  
Exemplo candidato: `orders-api` publica em `orders.events`; bindings levam para filas de billing, audit e email.  
Fonte: F1, F2, F5.  
Por que a prosa pode não bastar: a frase "não conhece fila" fica abstrata sem mostrar a fila atrás da exchange.  
Risco de virar laboratório ou excesso: inserir código de client library.  
Como manter conceitual e mínimo: usar nomes fictícios e setas visuais, sem comandos.  
Fronteira com nodes futuros: não explicar broadcast versus competição.

Conceito ou relação: adicionar consumidor sem mudar publisher.  
Tipo de demanda: estado antes/depois.  
Primitiva visual escolhida: estado comparativo em cards.  
Justificativa da primitiva: a mudança é topológica, não procedural; o contraste antes/depois mostra o valor do contrato estável.  
Exemplo candidato: adicionar fila de auditoria com binding para `orders.*`.  
Fonte: F1, F3, F6.  
Por que a prosa pode não bastar: sem estado anterior e posterior, parece promessa genérica de desacoplamento.  
Risco de virar laboratório ou excesso: ensinar criação de fila/binding por comando.  
Como manter conceitual e mínimo: mostrar "o que muda" e "o que não muda".  
Fronteira com nodes futuros: não falar de alternate exchange ou confirmações.

Conceito ou relação: contrato materializado em relações de topologia.  
Tipo de demanda: forma e fronteira.  
Primitiva visual escolhida: componente HTML/CSS em cards.  
Justificativa da primitiva: fonte F6 trata topology como definitions, mas mostrar JSON tornaria a página mais operacional do que conceitual; cards preservam a relação sem virar guia de import/export.  
Exemplo candidato: exchange pública, filas internas e bindings que conectam os lados.  
Fonte: F6 e F1.  
Por que a prosa pode não bastar: "topologia como contrato" pode soar abstrato sem uma forma visível da relação.  
Risco de virar laboratório ou excesso: incluir comando, arquivo completo ou endpoint.  
Como manter conceitual e mínimo: usar cards de relação, sem JSON e sem comando.  
Fronteira com nodes futuros: não entrar em policies nem permissions.

Conceito ou relação: escolher recorte de exchange.  
Tipo de demanda: contraste.  
Primitiva visual escolhida: tabela de decisão.  
Justificativa da primitiva: domínio, evento, severidade e tenant são alternativas com trade-offs comparáveis.  
Exemplo candidato: `orders.events`, `orders.created`, `logs.severity`, `tenant-a.events`.  
Fonte: F1, F3 e inferência declarada.  
Por que a prosa pode não bastar: uma lista longa esconderia consequência por recorte.  
Risco de virar fórmula universal.  
Como manter conceitual e mínimo: apresentar como leitura de decisão, não recomendação absoluta.  
Fronteira com nodes futuros: não virar governança ampla.

## Riscos, Armadilhas e Erros Comuns

- Nome de fila como routing key pública: base F5 e contrato do roadmap. Risco: o producer passa a saber quem consome.
- Exchange por consumidor: base inferida de F1/F3. Risco: topology cresce junto com consumidores e não com contratos de publicação.
- Routing key carregando detalhe interno: base F1/F4 e inferência. Risco: mudança interna vira breaking change pública.
- Mudança de routing key sem compatibilidade: base inferida de bindings e contrato. Risco: mensagens deixam de alcançar destinos planejados; detalhes de unroutable ficam no node 03.
- Topologia sem owner: base F6 e inferência. Risco: definitions existem como artefato, mas ninguém governa semântica.

## Limites e Fora de Escopo

- Este node explica:
  - contrato de publicação entre producer e topologia;
  - convenção de routing key;
  - ownership mínimo de exchange;
  - fila como detalhe interno de consumidor;
  - comparação de recortes de exchange;
  - evolução por binding sem alterar publisher.
- Este node apenas menciona como fronteira:
  - alterações de consumidor que preservam o contrato;
  - falhas quando routing key perde compatibilidade;
  - definitions como forma de enxergar topologia.
- Fica para outro node:
  - broadcast versus consumidores competindo;
  - unroutable, mandatory e alternate exchange;
  - DLX e retry;
  - policies, x-arguments e permissões;
  - exchange-to-exchange bindings;
  - publisher confirms;
  - observabilidade e diagnóstico.
- Não pertence ao roadmap ou não entra aqui:
  - implementação por linguagem;
  - comandos operacionais;
  - setup local;
  - UI de management;
  - topologias multi-cluster.

## Divergências, Versões e Notas Temporais

- RabbitMQ 4.3 é a versão corrente consultada nas páginas oficiais em 2026-06-09.
- A especificação AMQP 0-9-1 é de 2008; ela sustenta o modelo de exchange/routing key/queue, mas não substitui a documentação RabbitMQ para extensões e comportamento atual.
- F1 indica que suporte a semi-durable e transient bindings será removido no futuro; isso não entra no HTML porque pertence a durabilidade/configuração, não ao contrato de publicação deste node.
- F6 mostra definitions como import/export e preconfiguração; o HTML usa apenas a ideia de topologia como artefato, sem comandos.

## Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| Exchange como ponto de publicação e roteamento | F1, F2, F4 | Base central do node |
| Bindings como regras que conectam destinos | F1, F3, F4 | Sustenta evolução sem mudar publisher |
| Queue como detalhe interno de consumo | F5, F1 | Usar sem reexplicar filas |
| Topologia como artefato explícito | F6, F3 | Usar visual de relação sem comandos |
| Recortes de exchange por domínio/evento/severidade/tenant | F1, F3, inferência | RabbitMQ não impõe estratégia |
| Permissões e policies fora de escopo | F7, F1 | Não usar como conteúdo visível |

## Lacunas Pesquisadas e Resolvidas

Lacuna: RabbitMQ trata topologia como algo exportável ou apenas runtime?  
Busca feita: documentação oficial de definitions.  
Fonte que resolveu: F6.  
Decisão: usar a noção de topology/schema/metadata como apoio conceitual, sem ensinar import/export.

Lacuna: o publisher deve conhecer fila final em topologia explícita?  
Busca feita: docs de exchanges, publishers e queues.  
Fonte que resolveu: F1, F2, F5.  
Decisão: HTML deve separar exchange/routing key como contrato público e fila como destino atrás do binding.

Lacuna: comparar exchange por tenant exige falar de vhost e permissions?  
Busca feita: docs de vhosts/access-control e contrato do roadmap.  
Fonte que resolveu: F7 e contrato do node.  
Decisão: mencionar tenant apenas como recorte de nome/roteamento; deixar isolamento e permissões fora do HTML.

## Lacunas Remanescentes

Não há lacuna bloqueante. A documentação oficial não define uma convenção universal de nomes por domínio/evento/severidade/tenant; o HTML deve apresentar isso como decisão de design baseada no modelo de exchange/binding, não como recomendação normativa do RabbitMQ.

## Ordem de Introdução Conceitual

Conceito: contrato de publicação  
Necessidade: mostrar que o publisher precisa de uma parte estável para publicar sem conhecer consumidores.  
Explicação antes do nome: situação em que `orders-api` publica eventos e novos consumidores surgem depois.  
Nomeação: depois de explicar exchange + routing key como parte visível para o publisher.  
Depende de: exchange, routing key, fila.  
Pode usar depois para: estabilidade, evolução e ownership.  
Não entrar ainda em: payload schema completo, permissions, confirms.  
Visual possível: topologia publisher -> exchange -> bindings -> filas.  
Fonte base: F1, F2, F3.

Conceito: convenção de routing key  
Necessidade: a string precisa ter semântica estável para o time, não só combinar tecnicamente.  
Explicação antes do nome: `orders.created` representa o acontecimento publicado, não a fila que vai receber.  
Nomeação: após mostrar o exemplo `orders.events`.  
Depende de: routing key básica.  
Pode usar depois para: matriz de decisão e riscos de acoplamento.  
Não entrar ainda em: topic wildcards avançados e migração via AE.  
Visual possível: tabela curta de exemplos bons/ruins.  
Fonte base: F1, F4, F5.

Conceito: ownership de exchange  
Necessidade: alguém deve proteger o significado de `orders.events`.  
Explicação antes do nome: nome da exchange vira ponto compartilhado por publishers e topologia.  
Nomeação: após definir contrato estável.  
Depende de: contrato de publicação.  
Pode usar depois para: comparação de recortes.  
Não entrar ainda em: governança avançada.  
Visual possível: tabela de decisão.  
Fonte base: F1, F6 e inferência.

Conceito: fronteira publisher-topology-consumer  
Necessidade: mostrar quem conhece o quê.  
Explicação antes do nome: publisher conhece exchange/routing key; topologia conhece bindings; consumer conhece fila.  
Nomeação: após o visual de topologia.  
Depende de: contrato de publicação e fila interna.  
Pode usar depois para: evolução sem redeploy do publisher.  
Não entrar ainda em: diagnóstico operacional.  
Visual possível: topologia com faixas.  
Fonte base: F1, F2, F5.

Conceito: fila de grupo consumidor  
Necessidade: nomear a fila como destino de consumo, sem transformá-la em contrato público.  
Explicação antes do nome: cada serviço pode ter sua fila por trás do binding.  
Nomeação: depois da topologia `orders`.  
Depende de: fila e consumer do node anterior.  
Pode usar depois para: próximo node de broadcast/competição.  
Não entrar ainda em: competing consumers.  
Visual possível: cards de destino.  
Fonte base: F5.

## Insumos para o Ledger Editorial

### Conceitos que podem aparecer no HTML

Conceito: contrato de publicação  
Tipo: termo  
Pode aparecer depois de: situação do producer publicando em exchange com routing key sem conhecer fila.  
Explicação mínima antes do nome: exchange + routing key como parte que o producer respeita.  
Primeira nomeação permitida: após a abertura e antes do primeiro visual.  
Aliases e paráfrases: acordo de publicação; parte pública da topologia; contrato entre producer e topologia.  
Pode ser usado depois para: estabilidade, compatibilidade, evolução.  
Não usar para: payload schema completo ou garantia de entrega.  
Pode aparecer em título/lead/tabela/visual/referência: título sim depois da abertura; lead não; tabela sim; visual sim; referência sim se já preparado.  
Fronteira com nodes futuros: não entrar em confirms.  
Fonte base: F1, F2.

Conceito: convenção de routing key  
Tipo: termo  
Pode aparecer depois de: exemplo `orders.created` como intenção de publicação.  
Explicação mínima antes do nome: string que carrega significado de roteamento.  
Primeira nomeação permitida: seção de routing key.  
Aliases e paráfrases: padrão de routing key; vocabulário de routing; formato de routing key.  
Pode ser usado depois para: avaliar se a key está pública demais.  
Não usar para: explicar wildcards do topic em profundidade.  
Pode aparecer em título/lead/tabela/visual/referência: corpo e tabela sim; lead não.  
Fronteira com nodes futuros: migração de keys fica para AE/unroutable.  
Fonte base: F1, F4.

Conceito: ownership de exchange  
Tipo: papel  
Pode aparecer depois de: mostrar que a exchange é ponto compartilhado.  
Explicação mínima antes do nome: responsabilidade por nome, significado e evolução.  
Primeira nomeação permitida: tabela de decisão.  
Aliases e paráfrases: dono da exchange; responsabilidade pela exchange; ownership do contrato.  
Pode ser usado depois para: comparar domínio, evento, severidade e tenant.  
Não usar para: permissions.  
Pode aparecer em título/lead/tabela/visual/referência: corpo e tabela sim; lead não.  
Fronteira com nodes futuros: governança avançada fica no avançado.  
Fonte base: F6 e inferência.

Conceito: fila de grupo consumidor  
Tipo: papel  
Pode aparecer depois de: explicar que a fila fica atrás do binding.  
Explicação mínima antes do nome: fila usada por um serviço/grupo consumidor como detalhe de consumo.  
Primeira nomeação permitida: após topologia `orders`.  
Aliases e paráfrases: fila do serviço; fila interna de consumo; fila de destino de um consumer group.  
Pode ser usado depois para: separar público/interno.  
Não usar para: decidir competing consumers.  
Pode aparecer em título/lead/tabela/visual/referência: corpo e visual sim; título não.  
Fronteira com nodes futuros: broadcast/competição fica no próximo node.  
Fonte base: F5.

### Conceitos permitidos só no dump

Conceito: permissions  
Motivo: node próprio reservado.  
Por que não deve aparecer no HTML: discutir configure/write/read invadiria `intermediario/05`.  
Aliases bloqueados no HTML: permissions; permissões; configure permission; write permission; read permission.  
Fonte base: F7.

Conceito: policy  
Motivo: node próprio reservado.  
Por que não deve aparecer no HTML: policies e x-arguments ficam em `intermediario/05`.  
Aliases bloqueados no HTML: policy; policies; política; políticas; x-arguments; argumentos opcionais.  
Fonte base: F1, F7.

Conceito: alternate exchange  
Motivo: node próprio reservado.  
Por que não deve aparecer no HTML: fallback de roteamento fica em `intermediario/03`.  
Aliases bloqueados no HTML: alternate exchange; AE; exchange alternativa; fallback de roteamento.  
Fonte base: F1.

### Conceitos reservados a nodes futuros

Conceito: broadcast vs consumidores competindo  
Node responsável: Broadcast vs consumidores competindo  
Node ID responsável: `intermediario/02-broadcast-vs-consumidores-competindo`  
Menção permitida no HTML atual: handoff final curto.  
Aliases bloqueados: competing consumers; consumidores competindo; broadcast; cópia por consumidor.  
Condição de exceção: apenas mencionar que o próximo node aprofunda a decisão entre cópia e competição.

Conceito: publisher confirms  
Node responsável: Publisher confirms e confiabilidade  
Node ID responsável: `intermediario/07-publisher-confirms-e-confiabilidade`  
Menção permitida no HTML atual: nenhuma.  
Aliases bloqueados: confirms; confirmação do publisher; publisher confirm.  
Condição de exceção: nenhuma neste HTML.

Conceito: exchange-to-exchange bindings  
Node responsável: Exchange-to-exchange bindings  
Node ID responsável: `intermediario/06-exchange-to-exchange-bindings`  
Menção permitida no HTML atual: nenhuma.  
Aliases bloqueados: E2E; exchange-to-exchange; exchange para exchange.  
Condição de exceção: nenhuma neste HTML.

### Títulos de fontes e termos de referência

Fonte: F1  
Termos carregados pelo título: exchanges  
Pode aparecer visível no HTML: sim  
Forma visível recomendada: Documentação oficial de exchanges  
Decisão: permitido porque exchange é pré-requisito e usado no node.

Fonte: F2  
Termos carregados pelo título: publishers  
Pode aparecer visível no HTML: sim  
Forma visível recomendada: Guia oficial de publishers  
Decisão: permitido porque publisher é parte do contrato.

Fonte: F3  
Termos carregados pelo título: AMQP 0-9-1  
Pode aparecer visível no HTML: sim  
Forma visível recomendada: Guia oficial do modelo AMQP 0-9-1  
Decisão: permitido porque o roadmap usa esse recorte.

Fonte: F6  
Termos carregados pelo título: schema definitions  
Pode aparecer visível no HTML: não  
Forma visível recomendada: manter apenas no dump  
Decisão: o HTML atual usa a noção de relação explícita sem renderizar definitions como referência visível.

## Candidatos de Narrativa para o HTML

Pergunta-motor possível:
- Como um producer publica um evento sem gravar no código quem vai consumir esse evento hoje ou amanhã?

Situação de abertura possível:
- `orders-api` publica `orders.created`; primeiro só billing consome, depois auditoria precisa receber a mesma intenção sem redeploy do publisher.

Transformação acompanhada:
- Começar com um publisher ligado mentalmente a uma fila; transformar em publisher ligado a um contrato de exchange + routing key; mostrar bindings evoluindo atrás do contrato.

Narrativa dominante:
- Topológica com construção incremental.

Por que esta narrativa combina com o node:
- O assunto é fronteira entre partes e conhecimento de cada parte. Topologia visual e evolução incremental mostram o valor do contrato melhor que checklist.

Exemplo condutor possível:
- Exchange `orders.events`, routing key `orders.created`, fila `billing.orders-created`; depois entra `audit.orders-events`.

Momento de nomeação dos conceitos:
- Contrato de publicação após explicar exchange + routing key como parte pública.
- Convenção de routing key após mostrar `orders.created`.
- Ownership após mostrar que a exchange compartilhada precisa de responsabilidade.

Abstrações que precisam virar visual:
- Quem conhece quem na topologia.
- O que muda ao adicionar consumidor.
- Comparação de recortes de exchange.

Contrastes realmente necessários:
- Routing key de domínio versus nome de fila.
- Exchange por domínio/evento/severidade/tenant.

Riscos, limites e armadilhas que devem ficar no bastidor:
- Permissions, policies, alternate exchange, confirms, E2E.

Riscos de virar fórmula:
- Transformar a matriz de decisão em regra universal.

Risco de tom corretivo:
- Médio. A armadilha de nomear fila como key é importante, mas deve aparecer depois do modelo positivo.

## Validação do Dump

- Contrato do roadmap extraído: passa.
- Matriz anti-repetição aplicada: passa.
- Fontes primárias priorizadas: passa.
- Afirmações importantes com fonte ou inferência: passa.
- Conceitos essenciais com dependências explícitas: passa.
- Relações causais e estruturais claras: passa.
- Riscos, limites e divergências registrados: passa.
- Lacunas relevantes resolvidas ou declaradas: passa.
- Ordem de introdução conceitual existe: passa.
- Insumos para o ledger editorial existem: passa.
- Obrigações de concretização didática existem e são reais: passa.
- Conceitos classificados para HTML/dump/futuro: passa.
- Títulos de fontes analisados: passa.
- Candidatos de narrativa existem: passa.
- O dump não virou outline do HTML: passa.
