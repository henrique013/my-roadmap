# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Contrato de topologia e roteamento |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Intermediário · 01 de 07 |
| 4 | strong | Intermediário · 01 de 07 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Contrato de topologia e roteamento |
| 7 | p | Anterior: Filas, consumidores e entrega · Próximo: Broadcast vs consumidores competindo |
| 8 | a | Filas, consumidores e entrega |
| 9 | h1 | Contrato de topologia e roteamento |
| 10 | p.lead | Quando um serviço publica um acontecimento, ele precisa saber onde entregar a intenção de publicação, mas não deveria carregar no código a lista de filas que existem hoje. |
| 11 | p.meta | Pesquisa: documentação oficial RabbitMQ 4.3 e especificação AMQP 0-9-1 consultadas em 2026-06-09. |
| 12 | h2 | O producer conhece a porta, não os corredores |
| 13 | p | Imagine uma API de pedidos publicando que um pedido foi criado. No primeiro desenho, só o faturamento precisa reagir. Depois, auditoria e notificações também passam a precisar desse mesmo acontecimento. Se a API publica usando o nome da fila do faturamento, cada novo destino tende a virar mudança no producer. |
| 14 | p | O modelo de exchange evita esse encaixe apertado. A API publica em uma exchange conhecida e envia uma routing key com significado de domínio, como orders.created . A partir daí, bindings decidem quais filas recebem a mensagem. Esse conjunto estável, exchange alvo mais significado da routing key, é o contrato de publicação. |
| 15 | code | orders.created |
| 16 | strong | Ideia central: |
| 17 | h2 | Quem conhece quem na topologia |
| 18 | p | A primeira leitura útil é separar a parte pública da parte interna. A exchange e a routing key precisam fazer sentido para quem publica. As filas precisam fazer sentido para quem consome. O binding é a costura entre essas duas responsabilidades. |
| 19 | div.topology.visual-block@aria-label | Topologia conceitual de publicação em pedidos |
| 20 | span.tag | Producer |
| 21 | strong | orders-api |
| 22 | code | orders-api |
| 23 | p | Conhece a exchange orders.events e publica a intenção orders.created . |
| 24 | code | orders.events |
| 25 | code | orders.created |
| 26 | span.tag | Contrato |
| 27 | strong | orders.events |
| 28 | code | orders.events |
| 29 | p | Recebe publicações de pedidos e aplica bindings. A convenção de routing key diz qual acontecimento está sendo anunciado. |
| 30 | span.tag | Destinos internos |
| 31 | strong | Filas consumidoras |
| 32 | span.route-label | orders.created |
| 33 | code | orders.created |
| 34 | span | billing.orders-created |
| 35 | code | billing.orders-created |
| 36 | span.route-label | orders.* |
| 37 | code | orders.* |
| 38 | span | audit.orders-events |
| 39 | code | audit.orders-events |
| 40 | span.route-label | orders.created |
| 41 | code | orders.created |
| 42 | span | email.order-notifications |
| 43 | code | email.order-notifications |
| 44 | p | Nesse desenho, a fila billing.orders-created pode ser estável para o serviço de faturamento, mas não precisa virar vocabulário público da API de pedidos. O que a API promete é publicar o acontecimento em orders.events com uma key combinada. |
| 45 | code | billing.orders-created |
| 46 | code | orders.events |
| 47 | h2 | A routing key vira linguagem compartilhada |
| 48 | p | Uma routing key é tecnicamente uma string enviada na publicação. No contrato de topologia, ela também vira linguagem compartilhada. orders.created fala sobre um acontecimento; billing.orders-created fala sobre uma fila de um serviço. A diferença muda quem fica acoplado a quem. |
| 49 | code | orders.created |
| 50 | code | billing.orders-created |
| 51 | th | Forma |
| 52 | th | O que ela expõe |
| 53 | th | Consequência |
| 54 | td | orders.created |
| 55 | code | orders.created |
| 56 | td | Um acontecimento do domínio de pedidos. |
| 57 | td | Novos consumidores podem entrar por binding sem alterar a publicação original. |
| 58 | td | billing.orders-created |
| 59 | code | billing.orders-created |
| 60 | td | Um destino interno ligado ao faturamento. |
| 61 | td | O producer passa a carregar detalhe de consumo e a mudança de fila vira mudança pública. |
| 62 | p | A convenção de routing key precisa ser pequena o bastante para ser lembrada e rígida o bastante para proteger compatibilidade. Quando a key começa a codificar nome de fila, tecnologia do consumidor ou uma regra temporária de deploy, ela deixa de ser uma intenção de publicação e vira dependência interna. |
| 63 | h2 | A topologia pode mudar atrás do contrato |
| 64 | p | O valor prático aparece quando um consumidor novo entra. Antes, a publicação orders.created chegava só ao faturamento. Depois, auditoria precisa observar pedidos criados e cancelados. Se a exchange e a convenção continuam as mesmas, a mudança fica na topologia: uma nova fila e um novo binding. |
| 65 | code | orders.created |
| 66 | div.state-grid.visual-block@aria-label | Mudança de topologia sem alterar o producer |
| 67 | span.tag | Antes |
| 68 | p | orders-api publica em orders.events com orders.created . |
| 69 | code | orders-api |
| 70 | code | orders.events |
| 71 | code | orders.created |
| 72 | p | O binding existente envia a mensagem para billing.orders-created . |
| 73 | code | billing.orders-created |
| 74 | span.tag | Depois |
| 75 | p | orders-api continua publicando do mesmo jeito. |
| 76 | code | orders-api |
| 77 | p | A topologia adiciona audit.orders-events ligada ao padrão orders.* . |
| 78 | code | audit.orders-events |
| 79 | code | orders.* |
| 80 | p | O producer não ficou ignorante sobre o domínio: ele ainda escolhe a exchange e a key correta. O que ele não sabe é a lista atual de filas consumidoras. Essa é a fronteira publisher-topology-consumer em ação. |
| 81 | h2 | O recorte da exchange muda a responsabilidade |
| 82 | p | RabbitMQ não impõe uma convenção única para nomes de exchanges. O modelo dá peças; o desenho do contrato vem da aplicação. Por isso, escolher o recorte da exchange é escolher onde a responsabilidade semântica vai morar. |
| 83 | th | Recorte |
| 84 | th | Quando faz sentido |
| 85 | th | Cuidado principal |
| 86 | td | Por domínio |
| 87 | td | orders.events reúne acontecimentos de pedidos e deixa a routing key carregar o evento específico. |
| 88 | code | orders.events |
| 89 | td | O domínio precisa ter owner claro para evoluir keys sem quebrar publishers e consumers. |
| 90 | td | Por evento |
| 91 | td | orders.created como exchange separa fortemente um acontecimento muito central. |
| 92 | code | orders.created |
| 93 | td | Exchanges demais podem espalhar ownership e tornar a topologia difícil de revisar. |
| 94 | td | Por severidade |
| 95 | td | logs.severity combina quando a categoria operacional é a intenção de roteamento. |
| 96 | code | logs.severity |
| 97 | td | Não serve bem quando a decisão real é de domínio, como pedido criado ou pagamento recusado. |
| 98 | td | Por tenant |
| 99 | td | tenant-a.events pode isolar vocabulário por cliente em cenários que realmente pedem essa separação. |
| 100 | code | tenant-a.events |
| 101 | td | A cardinalidade cresce rápido; o tenant não deve substituir uma convenção de domínio quando o evento é o mesmo. |
| 102 | p | Ownership de exchange, aqui, não é discussão administrativa pesada. É a pergunta simples: quem pode dizer que orders.events continua significando a mesma coisa quando uma equipe quer mudar nomes, padrões ou destinos? |
| 103 | code | orders.events |
| 104 | h2 | O contrato aparece nas relações, não nos comandos |
| 105 | p | Como exchanges, filas e bindings são peças explícitas da topologia, é possível enxergar o contrato sem transformar a explicação em configuração. A forma mínima da relação é simples: uma exchange estável recebe a publicação; filas internas representam interesses de consumo; bindings unem os dois lados. |
| 106 | div.content-grid.visual-block@aria-label | Relações que materializam o contrato de topologia |
| 107 | span.tag | Exchange pública |
| 108 | p | orders.events é o ponto que o producer conhece. |
| 109 | code | orders.events |
| 110 | span.tag | Filas internas |
| 111 | p | billing.orders-created e audit.orders-events pertencem aos consumidores. |
| 112 | code | billing.orders-created |
| 113 | code | audit.orders-events |
| 114 | span.tag | Bindings |
| 115 | p | As regras conectam orders.created ou orders.* aos destinos que precisam da cópia. |
| 116 | code | orders.created |
| 117 | code | orders.* |
| 118 | p | A leitura importante é que a publicação continua apontando para orders.events . O que cresce é a tabela de bindings. Quando essa separação fica clara, a evolução de consumidores deixa de empurrar detalhes internos para o producer. |
| 119 | code | orders.events |
| 120 | h2 | Quando a key ficou pública demais |
| 121 | p | Depois que o modelo positivo está montado, a armadilha fica fácil de reconhecer: a routing key ficou pública demais quando ela revela o destino interno em vez da intenção de publicação. O sinal não é o tamanho da string; é a razão pela qual ela mudaria. |
| 122 | span.tag | Boa mudança |
| 123 | p | Adicionar audit.orders-events porque uma nova leitura precisa do mesmo acontecimento. |
| 124 | code | audit.orders-events |
| 125 | span.tag | Mudança suspeita |
| 126 | p | Renomear a key pública só porque a fila de um serviço mudou de nome. |
| 127 | span.tag | Pergunta útil |
| 128 | p | Esta key descreve o que aconteceu ou descreve quem consome agora? |
| 129 | p | O contrato de topologia não elimina mudanças incompatíveis. Ele torna visível onde elas acontecem e quem precisa coordená-las. Esse é o ponto em que uma exchange deixa de ser apenas mecanismo de roteamento e passa a ser uma fronteira de arquitetura. |
| 130 | h2 | A próxima decisão é sobre cópia e competição |
| 131 | p | Com o contrato estável, ainda falta decidir como os consumidores se organizam atrás dele. Uma fila por serviço muda o significado de receber cópias; vários consumers na mesma fila mudam a forma de dividir trabalho. Essa diferença é o próximo passo da corrente. |
| 132 | h2 | Referências |
| 133 | li.reference-item | Documentação oficial de exchanges Uso neste node: base para exchange como ponto de publicação, bindings e roteamento. |
| 134 | a | Documentação oficial de exchanges |
| 135 | span.reference-note | Uso neste node: base para exchange como ponto de publicação, bindings e roteamento. |
| 136 | li.reference-item | Guia oficial de publishers Uso neste node: sustenta a posição do producer no fluxo AMQP 0-9-1. |
| 137 | a | Guia oficial de publishers |
| 138 | span.reference-note | Uso neste node: sustenta a posição do producer no fluxo AMQP 0-9-1. |
| 139 | li.reference-item | Guia oficial do modelo AMQP 0-9-1 Uso neste node: reforça que aplicações definem entidades e esquemas de roteamento. |
| 140 | a | Guia oficial do modelo AMQP 0-9-1 |
| 141 | span.reference-note | Uso neste node: reforça que aplicações definem entidades e esquemas de roteamento. |
| 142 | li.reference-item | Documentação oficial de filas Uso neste node: apoia a separação entre fila consumidora e contrato público. |
| 143 | a | Documentação oficial de filas |
| 144 | span.reference-note | Uso neste node: apoia a separação entre fila consumidora e contrato público. |
| 145 | li.reference-item | Especificação AMQP 0-9-1 Uso neste node: base normativa para exchange, routing key e filas no modelo AMQP. |
| 146 | a | Especificação AMQP 0-9-1 |
| 147 | span.reference-note | Uso neste node: base normativa para exchange, routing key e filas no modelo AMQP. |
