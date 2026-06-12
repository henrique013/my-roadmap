# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Modelo AMQP e papel da exchange |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Básico · 01 de 06 |
| 4 | strong | Básico · 01 de 06 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Modelo AMQP e papel da exchange |
| 7 | p | Anterior: início do roadmap · Próximo: Exchange padrão e publicação direta aparente |
| 8 | a | Exchange padrão e publicação direta aparente |
| 9 | h1 | Modelo AMQP e papel da exchange |
| 10 | p.lead | Uma aplicação publica uma mensagem no RabbitMQ para que outras partes do sistema reajam depois. O ponto decisivo do modelo AMQP 0-9-1 é que essa publicação entra em uma exchange, e a exchange decide quais filas podem receber a mensagem. |
| 11 | p.meta | Pesquisa consultada em 2026-06-08: documentação oficial RabbitMQ 4.3 e especificação AMQP 0-9-1. |
| 12 | h2 | Antes do nome, a necessidade |
| 13 | p | Imagine uma aplicação de pedidos publicando o fato pedido.criado . Faturamento talvez precise criar uma cobrança; notificação talvez precise avisar o cliente. Se a aplicação de pedidos tivesse que conhecer cada aplicação consumidora, ela carregaria uma lista de destinos que muda com o tempo. |
| 14 | code | pedido.criado |
| 15 | p | O broker RabbitMQ coloca uma peça entre quem publica e as filas que receberão mensagens. Essa peça é a exchange : o ponto de publicação que recebe a mensagem e faz roteamento para filas conforme as ligações configuradas. |
| 16 | strong | exchange |
| 17 | strong | Modelo mental: |
| 18 | h2 | O caminho que a mensagem percorre |
| 19 | p | O fluxo fica mais simples quando cada parte tem uma responsabilidade única. O publisher inicia a publicação. A exchange decide o caminho. O binding é a ligação que coloca uma fila ao alcance da exchange. A fila mantém a mensagem até a entrega. O consumer aparece no fim, ligado à fila. |
| 20 | div.path-diagram.visual-block@aria-label | Caminho conceitual de uma mensagem no modelo AMQP 0-9-1 |
| 21 | span.tag.blue | 1 |
| 22 | strong | Publisher |
| 23 | span | Aplicação de pedidos publica pedido.criado no broker. |
| 24 | code | pedido.criado |
| 25 | span.tag | 2 |
| 26 | strong | Exchange |
| 27 | span | Recebe a publicação e aplica roteamento. Ela não é a fila da mensagem. |
| 28 | span.tag | 3 |
| 29 | strong | Bindings |
| 30 | span | Ligações configuradas indicam quais filas estão ao alcance dessa exchange. |
| 31 | span.route-label | Fila de faturamento |
| 32 | p | Recebe uma cópia para o fluxo de cobrança. |
| 33 | strong | Consumer de faturamento |
| 34 | p | Processa a mensagem a partir da fila. |
| 35 | span.route-label | Fila de notificação |
| 36 | p | Recebe outra cópia para o aviso ao cliente. |
| 37 | strong | Consumer de notificação |
| 38 | p | Também processa a partir da sua fila. |
| 39 | p | O desenho evita uma leitura enganosa: o consumer não se registra na exchange como destino final. Ele recebe da fila. A exchange participa antes, no momento em que o broker decide para quais filas a publicação deve seguir. |
| 40 | h2 | Roteamento não é armazenamento |
| 41 | p | A diferença mais importante deste node é a fronteira entre rotear e armazenar . A exchange existe para decidir o caminho da mensagem. A fila existe para guardar mensagens que já foram roteadas e entregá-las aos consumers. |
| 42 | strong | rotear |
| 43 | strong | armazenar |
| 44 | div.responsibility-map.visual-block@aria-label | Responsabilidades de exchange, fila e consumer |
| 45 | span.tag | Exchange |
| 46 | p | Responsabilidade: roteamento. |
| 47 | strong | Responsabilidade: |
| 48 | p | Ela recebe a publicação e avalia as ligações existentes para alcançar filas. |
| 49 | span.tag.blue | Fila |
| 50 | p | Responsabilidade: armazenamento e entrega. |
| 51 | strong | Responsabilidade: |
| 52 | p | Ela mantém a mensagem até que um consumer a receba. |
| 53 | span.tag | Consumer |
| 54 | p | Responsabilidade: processamento. |
| 55 | strong | Responsabilidade: |
| 56 | p | Ele trabalha a partir de uma fila, não a partir da exchange. |
| 57 | p | Quando alguém diz que uma exchange "tem mensagens esperando", o modelo mental já saiu do trilho. O que pode ficar esperando no recorte básico é a mensagem em uma fila. A exchange pode até não encontrar nenhuma fila aplicável, mas isso não a transforma em armazenamento. |
| 58 | h2 | Uma publicação, três resultados possíveis |
| 59 | p | Publicar em uma exchange não significa escolher exatamente uma fila. O resultado depende das ligações que existem naquele momento. Para o exemplo do pedido, pense em três estados possíveis da topologia: |
| 60 | div.result-grid.visual-block@aria-label | Resultados possíveis de uma publicação em uma exchange |
| 61 | span.tag.warn | Zero filas |
| 62 | p | Nenhuma ligação aplicável alcança uma fila. A exchange não guarda a mensagem para tentar de novo como se fosse uma fila. |
| 63 | span.tag.blue | Uma fila |
| 64 | p | A publicação alcança uma fila, que passa a manter a mensagem para um consumer daquela fila. |
| 65 | span.tag | Várias filas |
| 66 | p | Mais de uma fila é alcançada. Cada fila recebe uma cópia independente para seu próprio fluxo. |
| 67 | p | Essa é a razão de a exchange existir como peça própria: o produtor publica um fato uma vez, e o broker usa a topologia para decidir o alcance dessa publicação. A aplicação de pedidos não precisa saber se hoje só faturamento escuta, se amanhã notificação também escuta, ou se nenhuma fila foi ligada ainda. |
| 68 | h2 | Como ler a topologia sem misturar papéis |
| 69 | p | Ao olhar para um desenho de RabbitMQ, leia da esquerda para a direita e pergunte qual responsabilidade aparece em cada ponto. Se a pergunta é "quem publica?", você está falando do publisher. Se é "onde a decisão de caminho acontece?", é a exchange. Se é "onde a mensagem fica até alguém receber?", é a fila. Se é "quem processa?", é o consumer. |
| 70 | th | Pergunta que você faz |
| 71 | th | Peça do modelo |
| 72 | th | Resposta segura neste node |
| 73 | td | Quem colocou a mensagem no broker? |
| 74 | td | publisher ou producer |
| 75 | code | publisher |
| 76 | code | producer |
| 77 | td | A aplicação que publica o fato. |
| 78 | td | Onde a publicação entra para ser direcionada? |
| 79 | td | exchange |
| 80 | code | exchange |
| 81 | td | No ponto de roteamento do broker. |
| 82 | td | Que relação permite uma fila ser alcançada? |
| 83 | td | binding |
| 84 | code | binding |
| 85 | td | Uma ligação configurada entre exchange e fila. |
| 86 | td | Onde a mensagem fica até a entrega? |
| 87 | td | queue / fila |
| 88 | code | queue |
| 89 | td | Na fila que recebeu a mensagem roteada. |
| 90 | td | Quem recebe para processar? |
| 91 | td | consumer |
| 92 | code | consumer |
| 93 | td | A aplicação consumidora ligada à fila. |
| 94 | p | Esse vocabulário já é suficiente para desenhar o fluxo básico de uma mensagem. O próximo passo é entender o caso que parece quebrar essa regra: a exchange padrão, que cria a aparência de publicação direta em fila sem abandonar o modelo de exchanges. |
| 95 | h2 | Referências |
| 96 | li.reference-item | F1 - documentação oficial RabbitMQ 4.3 Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 97 | a | F1 - documentação oficial RabbitMQ 4.3 |
| 98 | span.reference-note | Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 99 | li.reference-item | F2 - guia oficial RabbitMQ 4.3 Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
| 100 | a | F2 - guia oficial RabbitMQ 4.3 |
| 101 | span.reference-note | Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
| 102 | li.reference-item | F16 - especificação AMQP 0-9-1 Uso neste node: Fonte primária do protocolo AMQP 0-9-1 para o papel de exchanges, queues e routing keys. |
| 103 | a | F16 - especificação AMQP 0-9-1 |
| 104 | span.reference-note | Uso neste node: Fonte primária do protocolo AMQP 0-9-1 para o papel de exchanges, queues e routing keys. |
