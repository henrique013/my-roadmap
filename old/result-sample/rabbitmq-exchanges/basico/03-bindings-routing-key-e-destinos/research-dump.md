# Research dump - Bindings, routing key e destinos

## Metadados do Node

- Roadmap de origem: `rabbitmq-exchanges`
- Tema humano do roadmap: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: `basico`
- Node ID: `basico/03-bindings-routing-key-e-destinos`
- Slug do node: `03-bindings-routing-key-e-destinos`
- Label do node: Bindings, routing key e destinos
- Posição local: 3 de 6
- Node anterior no nível: `basico/02-exchange-padrao-e-publicacao-direta-aparente` - Exchange padrão e publicação direta aparente
- Próximo node no nível: `basico/04-direct-fanout-e-topic` - Direct, fanout e topic
- Data da pesquisa: 2026-06-08
- Observações temporais: a documentação oficial consultada está na série RabbitMQ 4.3 em 2026-06-08. O modelo AMQP 0-9-1 é estável, mas páginas atuais do RabbitMQ devem prevalecer para propriedades e tipos de destino implementados pelo produto.

## Contrato Extraído do Roadmap

- Papel do node na corrente: transforma exchange de conceito abstrato em tabela de roteamento: bindings ligam source exchange a destinos e a routing key participa conforme o tipo.
- Papel do nível no roadmap tri-level: estabilizar fundamentos, vocabulário indispensável e modelos mentais antes de detalhar tipos de exchange, filas, consumidores e decisões intermediárias.
- Pré-requisitos herdados:
  - Entender que exchanges recebem publicações e roteiam para destinos.
  - Entender que o node anterior já resolveu a aparente publicação direta em fila pela default exchange.
- O que introduz pela primeira vez:
  - Binding como regra de roteamento.
  - Routing key da publicação.
  - Binding key como critério de ligação.
  - Destino queue, stream ou exchange.
- O que deve cobrir:
  - Definir source, destination, destination type e argumentos de binding.
  - Explicar zero, uma ou várias rotas possíveis para uma publicação.
  - Separar routing key enviada pelo publisher da regra criada no binding.
  - Mostrar que uma exchange recém-declarada sem bindings é uma tabela de roteamento vazia.
- O que não deve cobrir:
  - Não detalhar comportamento por tipo de exchange além do necessário para preparar o próximo node.
  - Não cobrir E2E em profundidade; apenas indicar que outra exchange pode ser destino.
  - Não tratar mensagens sem rota com `mandatory` e alternate exchange; isso fica no intermediário.
- Perguntas do node:
  - O que muda entre uma exchange vazia e uma fila vazia?
  - Quem define a routing key e quem define o binding?
  - Como uma mesma mensagem pode ser roteada para duas filas diferentes?
- Vocabulário conceitual:
  - `binding`
  - `binding key`
  - `routing key`
  - `source exchange`
  - `destination queue`
  - `destination exchange`
  - `binding arguments`
- Exemplos e diagramas permitidos:
  - Mapa HTML/CSS de uma exchange com três bindings e destinos diferentes.
  - Cenário de `orders.created` indo para fila de e-mail e fila de auditoria por bindings distintos.
- Armadilhas:
  - Tratar binding key e routing key como sinônimos fora de contexto.
  - Esperar que uma exchange sem bindings guarde mensagens para depois.
  - Esquecer que alguns tipos ignoram routing key.
- Critério de domínio: consegue ler uma topologia simples e prever quais filas recebem a mensagem a partir dos bindings.
- Handoff: com bindings e routing keys definidos, o próximo node compara os tipos principais de exchange.
- Referências específicas herdadas do contrato: F1 e F2 do roadmap, expandidas neste dump.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto no node 01:
  - O publisher publica em uma exchange.
  - A exchange roteia e não é o armazenamento final da mensagem.
  - Filas armazenam mensagens e consumidores recebem de filas.
  - O exemplo de pedido usado no node 01 não deve ser repetido como explicação de exchange como conceito geral.
- Conteúdo já coberto no node 02:
  - `exchange=""` seleciona a default exchange; não significa ausência de exchange.
  - O broker cria binding automático entre a default exchange e cada fila, usando o nome da fila como routing key.
  - A default exchange é uma conveniência para casos simples, não uma exchange de domínio com bindings manuais.
- Conteúdo que este node adiciona:
  - Binding explícito como regra que conecta uma exchange de origem a um destino.
  - Routing key como informação enviada na publicação.
  - Binding key como critério registrado na ligação.
  - A mesma publicação pode não encontrar destino, encontrar um destino ou encontrar vários destinos.
  - Uma exchange recém-criada sem bindings tem tabela de roteamento vazia: ela recebe publicações, mas ainda não tem regra de saída.
  - O destino de um binding no RabbitMQ pode ser queue, stream ou outra exchange; este node só abre o vocabulário, sem aprofundar E2E.
- Conteúdo reservado a nodes futuros:
  - `basico/04-direct-fanout-e-topic`: dar nomes e regras específicas para match exato, cópia para todos os destinos e padrões segmentados.
  - `basico/05-headers-e-metadados-de-roteamento`: aprofundar argumentos e headers como critério de roteamento por atributos.
  - `basico/06-filas-consumidores-e-entrega`: diferenciar filas, consumers, entrega, acknowledgements e competição entre consumidores.
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: tratar mensagens sem rota, `mandatory`, returns e alternate exchange.
  - `intermediario/06-exchange-to-exchange-bindings`: aprofundar bindings cujo destino é outra exchange.
  - `avancado/01-diagnostico-de-roteamento-e-observabilidade`: usar bindings e routing keys como evidência de diagnóstico, sem redefinir.
- Fronteiras:
  - Pode mencionar que o tipo de exchange decide como a routing key e os argumentos são interpretados; não deve listar regras completas dos tipos clássicos.
  - Pode mencionar que alguns tipos ignoram a routing key; não deve nomear ou aprofundar esses tipos como explicação central.
  - Pode usar `orders.created` como exemplo de routing key textual, mas sem transformar o node em guia de convenção de nomes de eventos.
  - Pode mostrar destination exchange como forma válida de destino, mas sem explicar composição E2E.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: define exchanges, bindings, routing keys, binding keys, argumentos opcionais, tipos de destino e a ideia de que uma mensagem pode ser roteada para zero, uma ou várias filas.  
Tópicos cobertos: exchange, binding, binding key, routing key, destination type, queue, stream, exchange, comportamento de roteamento por tipo.  
Limites da fonte: também cobre tipos específicos, alternate exchanges e E2E; este node usa apenas o necessário para fundamentos.

ID: F2  
URL: https://www.rabbitmq.com/tutorials/amqp-concepts  
Tipo: guia oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: explica o modelo AMQP 0-9-1 em linguagem conceitual, incluindo publishers, exchanges, queues, bindings, routing keys e a possibilidade de mensagens serem descartadas quando não há rota.  
Tópicos cobertos: modelo de publicação, binding como regra, routing key, zero ou múltiplos destinos, relação entre tipos de exchange e roteamento.  
Limites da fonte: guia didático amplo; detalhes de produto e propriedades atuais usam F1.

ID: F3  
URL: https://www.rabbitmq.com/docs/publishers  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta que publishers publicam em exchanges e que mensagens roteáveis são armazenadas em filas ou streams, com falhas e returns fora do escopo deste node.  
Tópicos cobertos: publicação AMQP 0-9-1 em exchange, roteamento, armazenamento em filas/streams, fronteira com mensagens sem rota.  
Limites da fonte: inclui `mandatory`, returns e confirms; o HTML atual não deve abrir esses sinais.

ID: F4  
URL: https://www.rabbitmq.com/docs/http-api-reference  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: confirma a forma operacional dos dados de binding na API HTTP, com `source`, `destination`, `destination_type`, `routing_key` e `arguments`.  
Tópicos cobertos: shape de um binding como registro de topologia.  
Limites da fonte: é referência de API operacional; no HTML, a forma dos campos deve ser conceitual, não roteiro de chamada HTTP.

ID: F5  
URL: https://www.rabbitmq.com/docs/e2e  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta que RabbitMQ permite bindings exchange-to-exchange, com outra exchange como destino, embora a explicação profunda pertença a node intermediário.  
Tópicos cobertos: destino exchange e fronteira de E2E.  
Limites da fonte: E2E é extensão do RabbitMQ; este node só registra que destination exchange existe.

ID: F6  
URL: https://www.rabbitmq.com/assets/files/amqp0-9-1-43a54a005e97180a4fbe6e567a125d84.pdf  
Tipo: especificação  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: AMQP 0-9-1, documento de 2006-2008 publicado pelo RabbitMQ  
Motivo de uso: fonte primária para exchange, queue, binding e routing key no modelo AMQP 0-9-1.  
Tópicos cobertos: publicação em exchange, binding entre exchange e queue, routing key.  
Limites da fonte: não cobre toda extensão atual do RabbitMQ, como stream como destination type ou E2E.

## Síntese por Fonte

F1 permite afirmar que uma exchange roteia mensagens de acordo com bindings e que a routing key enviada com a publicação participa da decisão dependendo do tipo da exchange. A fonte também sustenta a distinção entre routing key e binding key: a primeira acompanha a mensagem publicada; a segunda é um atributo da ligação. A mesma página registra que bindings têm source, destination, destination type, routing key e argumentos opcionais.

F2 fornece a explicação didática de que binding é a relação entre exchange e queue e que a exchange usa regras de binding para decidir para onde encaminhar mensagens. A fonte também sustenta o fato de que, se uma mensagem não encontra rota, ela pode ser descartada por padrão; neste node essa consequência aparece apenas como limite, sem abrir `mandatory` ou alternate exchange.

F3 reforça a fronteira entre publicar, rotear e armazenar: publishers publicam em exchanges, e mensagens roteadas com sucesso são armazenadas em filas ou streams. A fonte ajuda a evitar a confusão de que uma exchange vazia armazenaria mensagens aguardando bindings futuros.

F4 confirma a forma de um binding como registro de topologia com campos nomeados. Isso sustenta o snippet conceitual mínimo do HTML, sem transformá-lo em operação executável.

F5 confirma que RabbitMQ permite que outra exchange seja destino de um binding. O HTML pode dizer que "destino também pode ser outra exchange" como vocabulário de topologia, mas deve deixar a composição profunda para node posterior.

F6 ancora o vocabulário AMQP clássico: binding liga exchange a queue e a routing key aparece na publicação e na regra de roteamento. Como F6 não cobre toda a superfície atual do RabbitMQ, F1 e F4 prevalecem para tipos de destino e campos de API.

## Afirmações Técnicas Importantes

Afirmação: um binding é uma regra de roteamento criada entre uma exchange de origem e um destino.  
Base: F1, F2, F6  
Condição ou limite: em AMQP clássico o destino central é queue; no RabbitMQ atual a documentação também reconhece stream e destination exchange.  
Impacto didático: transforma a exchange em uma tabela de regras, não em um objeto abstrato.

Afirmação: a routing key é enviada pelo publisher junto da publicação.  
Base: F1, F2, F3, F6  
Condição ou limite: nem todo tipo de exchange usa a routing key do mesmo modo; a regra por tipo fica no próximo node.  
Impacto didático: separa a parte dinâmica da publicação da topologia já declarada.

Afirmação: a binding key é o critério registrado no binding, frequentemente comparado com a routing key em tipos que roteiam por chave textual.  
Base: F1, F2, F6  
Condição ou limite: o termo pode aparecer como `routing_key` em APIs de binding, mas conceitualmente é a key da regra, não a key enviada pelo publisher.  
Impacto didático: evita tratar routing key e binding key como sinônimos universais.

Afirmação: a mesma publicação pode gerar zero, uma ou várias rotas.  
Base: F1, F2  
Condição ou limite: o que acontece com mensagens sem rota depende de opções de publicação e configuração futura; este node não abre `mandatory` nem alternate exchange.  
Impacto didático: prepara a leitura de topologias reais, nas quais uma publicação não tem cardinalidade fixa.

Afirmação: uma exchange recém-declarada sem bindings tem tabela de roteamento vazia.  
Base: F1, F2, F3, inferência declarada a partir da definição de exchange e binding  
Condição ou limite: não significa fila vazia nem buffer temporário; significa ausência de regra para encaminhar a publicação a destinos.  
Impacto didático: responde à pergunta "o que muda entre exchange vazia e fila vazia?".

Afirmação: bindings podem ter argumentos opcionais, lidos por tipos de exchange que dependem de critérios além de uma key textual simples.  
Base: F1, F4  
Condição ou limite: o node não aprofunda headers nem critérios por atributos.  
Impacto didático: mostra que um binding é um registro de regra mais rico que uma seta simples, sem antecipar o node de headers.

Afirmação: destination exchange existe no RabbitMQ, mas aprofundar a composição entre exchanges pertence ao node intermediário sobre E2E.  
Base: F1, F5  
Condição ou limite: no HTML atual, a menção deve ser curta e delimitada.  
Impacto didático: atende o contrato do node sem deslocar o foco de bindings simples.

## Conceitos Essenciais

Conceito: binding  
Explicação simples: regra de topologia que liga uma exchange de origem a um destino e diz quando uma publicação deve seguir por aquela saída.  
Necessidade no node: conceito central. Sem ele, exchange continua parecendo uma caixa opaca.  
Relação com conceitos anteriores: herda a ideia de que a exchange roteia; agora mostra a regra que permite o roteamento.  
Relação com conceitos futuros: tipos de exchange usam bindings de modos diferentes; E2E aprofunda destination exchange.  
Riscos de confusão: achar que binding é mensagem, consumo ou armazenamento.  
Fonte base: F1, F2, F6.

Conceito: source exchange  
Explicação simples: exchange onde o binding começa; é a tabela que recebe a publicação e avalia suas regras.  
Necessidade no node: permite ler o binding como relação direcional.  
Relação com conceitos anteriores: publisher publica em exchange; essa exchange é a source quando seus bindings são avaliados.  
Relação com conceitos futuros: E2E torna a direção source -> destination mais importante.  
Riscos de confusão: inverter source e destination.  
Fonte base: F1, F4, F5.

Conceito: destination / destination type  
Explicação simples: destino é o recurso para onde a rota aponta; destination type diz se esse destino é queue, stream ou exchange.  
Necessidade no node: mostra que binding não liga apenas "exchange a fila" no vocabulário atual do RabbitMQ.  
Relação com conceitos anteriores: fila já apareceu como lugar onde a mensagem fica; stream e destination exchange aparecem apenas como formas de destino.  
Relação com conceitos futuros: filas e consumers entram no node 06; E2E entra no intermediário.  
Riscos de confusão: abrir stream ou E2E em profundidade cedo demais.  
Fonte base: F1, F3, F4, F5.

Conceito: routing key  
Explicação simples: valor textual enviado na publicação, usado por tipos de exchange que roteam por chave ou padrão.  
Necessidade no node: permite entender quem traz a intenção da mensagem no momento da publicação.  
Relação com conceitos anteriores: no node 02, routing key foi nome de fila na default exchange; agora ela vira chave de publicação em topologias explícitas.  
Relação com conceitos futuros: direct/fanout/topic explicam como cada tipo usa ou ignora a key.  
Riscos de confusão: achar que toda routing key é nome de fila ou que todos os tipos a usam.  
Fonte base: F1, F2, F3, F6.

Conceito: binding key  
Explicação simples: valor registrado no binding como critério da regra.  
Necessidade no node: separa regra estática da topologia e informação dinâmica enviada na publicação.  
Relação com conceitos anteriores: no binding automático da default exchange, o nome da fila funcionou como key da regra; agora a regra é explícita.  
Relação com conceitos futuros: tipos clássicos vão comparar, ignorar ou interpretar padrões em cima desse vocabulário.  
Riscos de confusão: usar "routing key" para tudo sem perceber a diferença entre publicação e regra.  
Fonte base: F1, F2, F4, F6.

Conceito: binding arguments  
Explicação simples: mapa opcional de parâmetros da regra de binding, usado por alguns tipos de exchange para critérios adicionais.  
Necessidade no node: completa a forma do registro de binding exigida pelo contrato.  
Relação com conceitos anteriores: nenhum pré-requisito forte além de entender que binding é regra.  
Relação com conceitos futuros: headers exchange aprofunda roteamento por atributos.  
Riscos de confusão: tratar argumentos como payload da mensagem ou configuração global da exchange.  
Fonte base: F1, F4.

Conceito: tabela de roteamento vazia  
Explicação simples: exchange sem bindings ainda recebe publicações, mas não tem saídas configuradas para encaminhar.  
Necessidade no node: responde por que exchange vazia não é como fila vazia.  
Relação com conceitos anteriores: reforça que exchange não armazena como fila, sem redefinir o node 01.  
Relação com conceitos futuros: mensagens sem rota ganham sinais e tratamento no intermediário.  
Riscos de confusão: imaginar que mensagens ficam esperando um binding futuro.  
Fonte base: F1, F2, F3.

## Relações Causais e Estruturais

- Publicação -> routing key: o publisher escolhe a exchange de destino e pode enviar uma routing key. Essa key é dado da publicação, não do binding.
- Exchange -> bindings: a exchange avalia as regras associadas a ela. Sem bindings, não há saídas.
- Binding -> destination: cada binding tem um destino e um destination type. Quando a regra corresponde ao critério do tipo de exchange, a mensagem segue para o destino.
- Uma publicação -> várias rotas: se mais de um binding da mesma source exchange combina com a publicação, mais de um destino pode receber cópia.
- Uma publicação -> zero rotas: se nenhum binding combina, não há destino inicial. O tratamento operacional dessa situação fica fora do HTML atual.
- Binding arguments -> regra enriquecida: argumentos são parte da regra de binding e podem mudar como um tipo de exchange avalia a publicação; não são corpo da mensagem.
- Destination exchange -> composição: outra exchange pode ser destino, mas isso cria uma camada de topologia que será tratada depois.

## Exemplos Técnicos Possíveis

Exemplo: publicação `orders.created` em `orders.events`.  
Mudança de estado que mostra: a publicação entra em uma exchange que já tem bindings explícitos. Dois bindings usam critério compatível com `orders.created`, então duas filas recebem cópias; um terceiro destino só recebe se sua regra também combinar.  
Conceitos introduzidos: routing key, binding key, source exchange, destination queue, múltiplos destinos.  
Riscos de escopo: pode antecipar direct/topic se o texto der nome aos tipos ou regras completas.  
Por que não vira laboratório: não há comando, sequência de execução nem configuração real; os campos são lidos como forma conceitual.

Exemplo: exchange `orders.events` recém-declarada sem bindings.  
Mudança de estado que mostra: antes dos bindings, a tabela de roteamento não possui saída; depois dos bindings, a mesma publicação passa a encontrar destinos.  
Conceitos introduzidos: tabela de roteamento vazia, zero rota, binding como regra.  
Riscos de escopo: pode abrir `mandatory` e alternate exchange; o HTML deve parar antes disso.  
Por que não vira laboratório: é estado conceitual de topologia, não operação executável.

Exemplo: registro mínimo de binding.  
Mudança de estado que mostra: a regra tem campos de origem, destino, tipo de destino, key e argumentos.  
Conceitos introduzidos: source, destination, destination type, binding arguments.  
Riscos de escopo: se parecer payload de API HTTP, vira operacional; deve ser rotulado como leitura conceitual.  
Por que não vira laboratório: o snippet não traz endpoint, comando, credencial, vhost ou sequência de chamada.

## Obrigações de Concretização Didática

Conceito ou relação: separação entre routing key enviada e binding key registrada.  
Tipo de demanda: contraste  
Primitiva visual escolhida: tabela curta e snippet conceitual com highlight semântico  
Justificativa da primitiva: a diferença fica abstrata se aparecer só em prosa, porque os nomes são parecidos e as APIs podem usar `routing_key` para o campo da regra.  
Exemplo candidato: publicação com `routing_key = "orders.created"` e binding com `binding_key = "orders.created"`.  
Fonte: F1, F2, F4  
Por que a prosa pode não bastar: a pessoa precisa ver qual valor está na publicação e qual valor está na topologia.  
Risco de virar laboratório ou excesso: baixo se o snippet não tiver comando, endpoint ou passo executável.  
Como manter conceitual e mínimo: usar apenas campos e leitura, sem cliente, biblioteca ou operação.  
Fronteira com nodes futuros: não explicar match de direct/topic.

Conceito ou relação: exchange sem bindings como tabela de roteamento vazia.  
Tipo de demanda: estado  
Primitiva visual escolhida: componente HTML/CSS de estado antes/depois  
Justificativa da primitiva: o contraste com fila vazia exige mostrar que a exchange não tem "mensagens guardadas", mas sim ausência de regra de saída.  
Exemplo candidato: `orders.events` antes e depois de dois bindings.  
Fonte: F1, F2, F3  
Por que a prosa pode não bastar: a pergunta do contrato é exatamente a diferença entre estados vazios.  
Risco de virar laboratório ou excesso: médio se virar diagnóstico de unroutable; o texto deve parar na ausência de rota.  
Como manter conceitual e mínimo: mostrar a topologia, não o tratamento de erro.  
Fronteira com nodes futuros: `mandatory`, AE e diagnóstico ficam fora.

Conceito ou relação: uma publicação encontrando múltiplos destinos.  
Tipo de demanda: fluxo e topologia  
Primitiva visual escolhida: mapa HTML/CSS com source exchange, bindings e destinos  
Justificativa da primitiva: múltiplas rotas simultâneas são melhor entendidas como mapa de saídas.  
Exemplo candidato: `orders.created` seguindo para fila de e-mail, fila de auditoria e stream de histórico.  
Fonte: F1, F2, F3  
Por que a prosa pode não bastar: a cardinalidade zero/uma/várias fica vaga sem ver as saídas.  
Risco de virar laboratório ou excesso: médio se detalhar consumers, filas ou stream; esses detalhes ficam fora.  
Como manter conceitual e mínimo: destinos são nomes de recursos, sem política, durability, consumer ou ack.  
Fronteira com nodes futuros: fila/consumer no node 06; tipos de exchange no node 04.

Conceito ou relação: destination type como queue, stream ou exchange.  
Tipo de demanda: forma e fronteira  
Primitiva visual escolhida: tabela curta de leitura  
Justificativa da primitiva: a pessoa precisa saber o que o campo aceita sem abrir cada tecnologia.  
Exemplo candidato: `queue`, `stream`, `exchange`.  
Fonte: F1, F4, F5  
Por que a prosa pode não bastar: o campo `destination_type` é uma classificação, e tabela comunica melhor.  
Risco de virar laboratório ou excesso: alto se aprofundar stream ou E2E.  
Como manter conceitual e mínimo: uma linha por tipo e uma frase de limite.  
Fronteira com nodes futuros: E2E em intermediário; filas e consumers no node 06.

## Riscos, Armadilhas e Erros Comuns

- Confusão: "routing key" e "binding key" são sempre a mesma coisa.  
  Base: F1, F2, F4.  
  Tratamento no HTML: mostrar que uma é enviada na publicação e a outra pertence à regra; quando os valores coincidem, a origem deles continua diferente.
- Confusão: exchange sem bindings guarda mensagens para enviar depois.  
  Base: F1, F2, F3 e matriz anti-repetição do roadmap.  
  Tratamento no HTML: usar estado de tabela vazia, sem abrir `mandatory` ou AE.
- Confusão: uma publicação sempre vai para uma única fila.  
  Base: F1, F2.  
  Tratamento no HTML: mapa com múltiplos destinos para a mesma routing key.
- Confusão: argumentos de binding são payload da mensagem.  
  Base: F1, F4.  
  Tratamento no HTML: chamar argumentos de parâmetros da regra, sem falar de payload.
- Confusão: destination exchange deve ser entendida agora como composição E2E.  
  Base: F1, F5.  
  Tratamento no HTML: mencionar como tipo de destino e deixar o aprofundamento para depois.
- Confusão: alguns tipos ignoram routing key, então a key não importa.  
  Base: F1, F2.  
  Tratamento no HTML: registrar que o tipo decide como a key participa e que os nomes dos tipos vêm no próximo node.

## Limites e Fora de Escopo

- Este node explica:
  - forma de um binding;
  - diferença entre routing key e binding key;
  - source exchange, destination e destination type;
  - zero, uma ou várias rotas;
  - exchange sem bindings como tabela de roteamento vazia;
  - argumentos de binding como parte da regra.
- Este node menciona apenas como fronteira:
  - destination exchange;
  - tipos de exchange que usam, ignoram ou interpretam a routing key de modos diferentes;
  - mensagens sem rota como ausência de destino inicial.
- Fica para outro node:
  - direct, fanout e topic em detalhe;
  - headers exchange e `x-match`;
  - consumers, acks, filas concorrentes;
  - `mandatory`, returned messages e alternate exchange;
  - E2E bindings em profundidade;
  - policies, permissões e governança.
- Não pertence a este roadmap neste momento:
  - laboratório de declaração de bindings;
  - comandos de `rabbitmqctl`, HTTP API ou clientes;
  - tuning operacional ou performance.

## Divergências, Versões e Notas Temporais

- O vocabulário AMQP 0-9-1 clássico fala principalmente de exchange e message queue. A documentação RabbitMQ 4.3 amplia a leitura prática para destination types como queue, stream e exchange. Decisão: usar a documentação atual do RabbitMQ para destination type, preservando AMQP 0-9-1 como base de modelo.
- A API HTTP usa o campo `routing_key` para bindings. Para evitar confusão didática, o HTML deve explicar que, no contexto do binding, esse valor funciona como key da regra, chamada no node de binding key.
- Mensagens sem rota têm comportamentos configuráveis. Decisão: o HTML pode dizer "não encontra destino inicial" e não deve entrar em retorno, confirmação ou alternate exchange.

## Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| Binding como regra de roteamento | F1, F2, F6 | Base central do node. |
| Routing key da publicação | F1, F2, F3, F6 | Usar como dado enviado pelo publisher. |
| Binding key como critério da regra | F1, F2, F4, F6 | Distinguir do campo de publicação. |
| Source, destination, destination type, arguments | F1, F4 | Shape do registro de topologia. |
| Zero, uma ou várias rotas | F1, F2 | Sem abrir tratamento de unroutable. |
| Queue, stream e exchange como destino | F1, F3, F4, F5 | E2E apenas como fronteira. |
| Exchange sem bindings como tabela vazia | F1, F2, F3 | Inferência explícita a partir do papel de bindings. |

## Lacunas Pesquisadas e Resolvidas

Lacuna: RabbitMQ atual reconhece destinos além de queue para bindings?  
Busca feita: documentação de exchanges e API HTTP do RabbitMQ.  
Fonte que resolveu: F1 e F4.  
Decisão: o HTML menciona queue, stream e exchange como destination types, mas só aprofunda queue e mantém exchange como fronteira.

Lacuna: Como registrar a diferença entre routing key da publicação e key do binding sem contrariar a API que usa `routing_key` no binding?  
Busca feita: documentação de exchanges, conceitos AMQP e API HTTP.  
Fonte que resolveu: F1, F2 e F4.  
Decisão: usar "routing key" para o valor enviado pelo publisher e "binding key" para o critério da regra; explicar que APIs podem nomear o campo da regra como `routing_key`.

Lacuna: O node pode afirmar que mensagem sem rota é descartada?  
Busca feita: AMQP concepts e publishers.  
Fonte que resolveu: F2 e F3.  
Decisão: no dump, registrar ausência de rota; no HTML, evitar detalhar descarte, `mandatory`, returns ou AE.

Lacuna: Destination exchange deve ser explicado agora?  
Busca feita: exchanges e E2E docs.  
Fonte que resolveu: F1 e F5.  
Decisão: mencionar como tipo de destino válido e apontar que a composição entre exchanges será aprofundada depois.

## Lacunas Remanescentes

Não há lacuna relevante que bloqueie o HTML. O limite principal é editorial: explicar o shape de binding com precisão sem invadir types, headers, unroutable e E2E.

## Ordem de Introdução Conceitual

Conceito: exchange com tabela vazia  
Necessidade: abrir a diferença entre exchange sem bindings e fila vazia.  
Explicação antes do nome: uma exchange recém-criada pode receber publicações, mas ainda não tem saída configurada.  
Nomeação: "tabela de roteamento vazia".  
Depende de: exchange como roteador herdada dos nodes 01 e 02.  
Pode usar depois para: introduzir binding como linha da tabela.  
Não entrar ainda em: mensagens retornadas, mandatory, AE.  
Visual possível: estado antes/depois.  
Fonte base: F1, F2, F3.

Conceito: binding  
Necessidade: nomear a regra que cria uma saída na exchange.  
Explicação antes do nome: a exchange precisa de uma regra que diga para onde uma publicação pode seguir.  
Nomeação: "binding".  
Depende de: tabela vazia e exchange como roteador.  
Pode usar depois para: source, destination, key da regra e múltiplas rotas.  
Não entrar ainda em: tipos específicos de exchange.  
Visual possível: linha da tabela de roteamento.  
Fonte base: F1, F2, F6.

Conceito: source exchange  
Necessidade: mostrar a direção da regra.  
Explicação antes do nome: a regra começa na exchange que está avaliando a publicação.  
Nomeação: "source exchange".  
Depende de: binding.  
Pode usar depois para: destination e E2E como fronteira.  
Não entrar ainda em: federation, upstream/downstream.  
Visual possível: mapa com exchange de origem.  
Fonte base: F1, F4, F5.

Conceito: destination e destination type  
Necessidade: mostrar para onde a regra aponta.  
Explicação antes do nome: a saída de uma regra aponta para um recurso de destino, e RabbitMQ classifica esse recurso por tipo.  
Nomeação: "destination" e "destination type".  
Depende de: binding e source.  
Pode usar depois para: queue, stream e exchange como destinos.  
Não entrar ainda em: consumers, streams em profundidade, E2E.  
Visual possível: tabela curta.  
Fonte base: F1, F3, F4, F5.

Conceito: routing key  
Necessidade: mostrar o dado que acompanha a publicação.  
Explicação antes do nome: a publicação pode carregar uma chave textual que ajuda a exchange a escolher saídas.  
Nomeação: "routing key".  
Depende de: publicação herdada e binding como regra.  
Pode usar depois para: comparar com binding key.  
Não entrar ainda em: topic wildcard ou headers.  
Visual possível: snippet conceitual de publicação.  
Fonte base: F1, F2, F3, F6.

Conceito: binding key  
Necessidade: separar a chave enviada da chave registrada na regra.  
Explicação antes do nome: a regra também pode ter uma chave própria, usada como critério.  
Nomeação: "binding key".  
Depende de: binding e routing key.  
Pode usar depois para: explicar coincidência de valores sem confusão de origem.  
Não entrar ainda em: match exato, wildcard, direct/topic.  
Visual possível: tabela publicação versus regra.  
Fonte base: F1, F2, F4, F6.

Conceito: binding arguments  
Necessidade: completar a forma do binding.  
Explicação antes do nome: algumas regras carregam parâmetros adicionais que o tipo de exchange pode ler.  
Nomeação: "binding arguments".  
Depende de: binding, destination e key da regra.  
Pode usar depois para: preparar headers exchange.  
Não entrar ainda em: `x-match`, headers e policies.  
Visual possível: snippet conceitual com `arguments = {}`.  
Fonte base: F1, F4.

Conceito: múltiplas rotas  
Necessidade: mostrar que cardinalidade não é fixa.  
Explicação antes do nome: a exchange avalia suas regras; mais de uma regra pode combinar com a mesma publicação.  
Nomeação: "zero, uma ou várias rotas".  
Depende de: binding, routing key e binding key.  
Pode usar depois para: explicar destino múltiplo.  
Não entrar ainda em: tipos específicos e consumers competindo.  
Visual possível: mapa de saídas.  
Fonte base: F1, F2.

## Insumos para o Ledger Editorial

Conceito: binding  
Tipo: termo  
Pode aparecer depois de: uma regra de saída da exchange ter sido descrita em linguagem comum.  
Explicação mínima antes do nome: "regra que conecta a exchange a um destino".  
Primeira nomeação permitida: primeira seção narrativa, depois da tabela vazia.  
Aliases e paráfrases: ligação, regra de roteamento, linha da tabela de roteamento.  
Pode ser usado depois para: source, destination, binding key, argumentos.  
Não usar para: mensagem, fila, consumidor, armazenamento.  
Pode aparecer em título/lead/tabela/visual/referência: título sim depois da abertura; lead sim; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: E2E aprofunda binding com destino exchange; types detalham como a regra é avaliada.  
Fonte base: F1, F2, F6.

Conceito: routing key  
Tipo: parâmetro  
Pode aparecer depois de: publicação com chave textual ter sido apresentada.  
Explicação mínima antes do nome: "valor que acompanha a publicação".  
Primeira nomeação permitida: lead e primeira seção, pois o node anterior já usou o termo; ainda assim explicar de novo no novo contexto.  
Aliases e paráfrases: chave de roteamento, chave da publicação.  
Pode ser usado depois para: contraste com binding key.  
Não usar para: critério da regra sem explicar a distinção.  
Pode aparecer em título/lead/tabela/visual/referência: sim em todos, com contexto.  
Fronteira com nodes futuros: não explicar wildcard nem tipos clássicos.  
Fonte base: F1, F2, F3, F6.

Conceito: binding key  
Tipo: parâmetro  
Pode aparecer depois de: binding ter sido nomeado e routing key ter sido separada como valor da publicação.  
Explicação mínima antes do nome: "chave registrada na regra".  
Primeira nomeação permitida: bloco de contraste publicação versus regra.  
Aliases e paráfrases: chave do binding, key da regra, critério da ligação.  
Pode ser usado depois para: explicar quando valores coincidem.  
Não usar para: key enviada pelo publisher.  
Pode aparecer em título/lead/tabela/visual/referência: título não antes da explicação; corpo/tabela/visual sim; referência sim.  
Fronteira com nodes futuros: match exato e patterns ficam para o próximo node.  
Fonte base: F1, F2, F4, F6.

Conceito: source exchange  
Tipo: papel  
Pode aparecer depois de: binding como relação direcional.  
Explicação mínima antes do nome: "exchange onde a regra começa".  
Primeira nomeação permitida: seção sobre forma do binding.  
Aliases e paráfrases: origem, exchange de origem.  
Pode ser usado depois para: destination.  
Não usar para: publisher ou broker.  
Pode aparecer em título/lead/tabela/visual/referência: corpo/tabela/visual sim; título com cautela; lead não necessário.  
Fronteira com nodes futuros: não usar upstream/downstream.  
Fonte base: F1, F4, F5.

Conceito: destination / destination type  
Tipo: papel  
Pode aparecer depois de: source exchange e binding terem sido apresentados.  
Explicação mínima antes do nome: "recurso para onde a regra aponta e sua classe".  
Primeira nomeação permitida: seção sobre forma do binding.  
Aliases e paráfrases: destino, tipo de destino, destination queue, destination exchange.  
Pode ser usado depois para: mapa de destinos.  
Não usar para: consumidor final ou serviço de negócio.  
Pode aparecer em título/lead/tabela/visual/referência: corpo/tabela/visual sim; lead não necessário.  
Fronteira com nodes futuros: streams e E2E não devem ser aprofundados.  
Fonte base: F1, F3, F4, F5.

Conceito: binding arguments  
Tipo: parâmetro  
Pode aparecer depois de: binding como registro de regra.  
Explicação mínima antes do nome: "parâmetros opcionais da regra".  
Primeira nomeação permitida: snippet conceitual da forma do binding.  
Aliases e paráfrases: argumentos, parâmetros da regra.  
Pode ser usado depois para: dizer que alguns tipos leem argumentos.  
Não usar para: payload, política, configuração global.  
Pode aparecer em título/lead/tabela/visual/referência: corpo/tabela sim; título/lead não necessário.  
Fronteira com nodes futuros: headers e `x-match` ficam no node 05.  
Fonte base: F1, F4.

Conceito: tabela de roteamento vazia  
Tipo: estado  
Pode aparecer depois de: exchange sem bindings ser descrita.  
Explicação mínima antes do nome: "sem regras de saída".  
Primeira nomeação permitida: abertura narrativa.  
Aliases e paráfrases: tabela sem linhas, sem saídas, sem bindings.  
Pode ser usado depois para: explicar zero rota.  
Não usar para: fila vazia ou buffer.  
Pode aparecer em título/lead/tabela/visual/referência: sim, quando preparado.  
Fronteira com nodes futuros: não abrir tratamento de unroutable.  
Fonte base: F1, F2, F3.

Conceitos que só podem aparecer no dump:
- `mandatory`: pertence a tratamento de mensagens sem rota no intermediário.
- alternate exchange / AE: pertence ao intermediário.
- returned message: pertence ao intermediário.
- publisher confirm: pertence ao intermediário.
- `x-match`: pertence ao node de headers.
- wildcard `*` e `#`: pertencem ao próximo node.

Títulos de fontes com vocabulário técnico:
- RabbitMQ - Exchanges: pode aparecer visível; termos já são herdados.
- RabbitMQ - AMQP 0-9-1 Model Explained: pode aparecer visível como fonte geral.
- RabbitMQ - Publishers: pode aparecer visível; "publisher" é pré-requisito herdado.
- RabbitMQ - HTTP API Reference: pode aparecer como "RabbitMQ - Referência da API HTTP"; não deve virar roteiro.
- RabbitMQ - Exchange-to-exchange bindings: não deve aparecer como título visível no HTML atual; se a fonte for citada, adaptar para "RabbitMQ - Bindings entre exchanges" apenas como fronteira ou deixar no dump.

## Candidatos de Narrativa para o HTML

Pergunta-motor possível:
- Quando uma exchange recebe uma publicação, de onde vem a decisão de quais destinos recebem a mensagem?
- O que existe dentro da "rota" entre uma exchange e uma fila?
- Por que uma exchange vazia não se comporta como uma fila vazia?

Situação de abertura possível:
- Uma equipe declara `orders.events`, publica `orders.created` e espera que e-mail e auditoria recebam a mensagem. A exchange existe, mas nenhuma saída foi declarada ainda.

Transformação acompanhada:
- A exchange começa como tabela sem linhas.
- Um binding cria a primeira saída.
- A publicação traz uma routing key.
- A exchange compara a publicação com suas regras conforme seu tipo.
- Mais de um binding pode apontar para destinos diferentes.

Narrativa dominante:
- Construção incremental/topológica.

Por que esta narrativa combina com o node:
- O centro do node é transformar uma exchange abstrata em uma tabela de roteamento legível. Construir a tabela linha por linha evita começar por definições soltas.

Exemplo condutor possível:
- `orders.events` recebe `orders.created`; bindings enviam a cópia para `orders.email`, `orders.audit` e, como fronteira, `orders.history` stream.

Momento de nomeação dos conceitos:
- Nomear "tabela de roteamento vazia" depois da exchange sem saídas.
- Nomear "binding" depois da primeira linha de saída.
- Nomear "routing key" quando a publicação carrega `orders.created`.
- Nomear "binding key" ao comparar valor da publicação com valor da regra.
- Nomear "destination type" ao ler queue, stream ou exchange como destinos.

Abstrações que precisam virar visual:
- Estado antes/depois de uma exchange sem bindings.
- Mapa de uma publicação encontrando múltiplas saídas.
- Registro mínimo de binding.

Contrastes realmente necessários:
- routing key da publicação versus binding key da regra.
- exchange sem bindings versus fila vazia.
- destination queue/stream/exchange sem aprofundar cada destino.

Riscos, limites e armadilhas que devem ficar no bastidor:
- `mandatory`, AE, returned message.
- Regras completas de direct/fanout/topic.
- Headers e `x-match`.
- E2E profundo.

Riscos de virar fórmula:
- Transformar o HTML em tabela de campos. Mitigação: abrir por situação concreta e usar tabelas só depois da explicação.

Risco de tom corretivo:
- Médio, porque há muitas confusões possíveis. Mitigação: construir o modelo da tabela de roteamento antes de usar frases negativas.

## Validação do Dump

- Contrato do roadmap extraído: sim.
- Matriz anti-repetição aplicada: sim.
- Fontes primárias priorizadas: sim.
- Afirmações importantes com fonte ou inferência declarada: sim.
- Conceitos essenciais com dependências explícitas: sim.
- Relações causais e estruturais claras: sim.
- Riscos, limites e divergências registrados: sim.
- Lacunas relevantes resolvidas ou declaradas: sim.
- Ordem de introdução conceitual existe: sim.
- Insumos para o ledger editorial existem: sim.
- Obrigações de concretização didática existem e registram demandas reais: sim.
- Conceitos classificados como permitidos, dump-only ou reservados: sim.
- Aliases, paráfrases e títulos de fontes registrados: sim.
- Candidatos de narrativa existem: sim.
- O dump não é outline do HTML: sim.
