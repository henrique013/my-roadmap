# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Filas, consumidores e entrega |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Básico · 06 de 06 |
| 4 | strong | Básico · 06 de 06 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Filas, consumidores e entrega |
| 7 | p | Anterior: Headers exchange e metadados de roteamento · Próximo: Contrato de topologia e roteamento |
| 8 | a | Headers exchange e metadados de roteamento |
| 9 | h1 | Filas, consumidores e entrega |
| 10 | p.lead | Depois que a exchange decidiu para qual fila uma publicação deve ir, começa outro trecho do fluxo: a mensagem precisa esperar, ser entregue a um consumer e só então sair da fila com segurança. |
| 11 | p.meta | Pesquisa: documentação oficial RabbitMQ 4.3 consultada em 2026-06-09. |
| 12 | h2 | Depois do roteamento, a pergunta muda |
| 13 | p | Imagine que a topologia já roteou uma mensagem para a fila emails . A exchange fez a parte dela: aplicou as regras de roteamento e colocou a mensagem no destino encontrado. Se nenhum worker de e-mail estiver online naquele instante, a mensagem não volta para a exchange nem fica esperando em um lugar abstrato entre as peças. |
| 14 | code | emails |
| 15 | p | Ela fica na fila. A fila é a coleção ordenada que guarda mensagens até que alguma aplicação registrada para consumir daquela fila possa recebê-las. Por isso, a pergunta depois do roteamento deixa de ser "qual binding combina?" e passa a ser "qual é o estado dessa mensagem dentro da fila?". |
| 16 | strong | Fronteira principal: |
| 17 | h2 | A fila mantém trabalho em estados diferentes |
| 18 | p | Enquanto não há worker disponível, a mensagem está pronta para entrega. Quando um consumer se registra na fila, RabbitMQ pode enviar essa mensagem para ele. Esse envio é uma delivery: a mensagem já saiu da lista de prontas, mas ainda não significa que o processamento terminou. |
| 19 | p | O ponto delicado é esse intervalo. A fila precisa distinguir uma mensagem apenas esperando de uma mensagem que já foi entregue a um consumer e ainda aguarda reconhecimento. O acknowledgement é o sinal do consumer dizendo ao broker que aquela delivery foi recebida e processada com sucesso. Só depois disso a mensagem entregue pode ser marcada para remoção futura. |
| 20 | div.state-flow.visual-block@aria-label | Estados conceituais de uma mensagem na fila |
| 21 | span.tag.blue | 1. Pronta |
| 22 | strong | Está na fila emails |
| 23 | code | emails |
| 24 | p | A mensagem foi roteada com sucesso e aguarda algum consumer disponível. |
| 25 | span.tag | 2. Entregue |
| 26 | strong | Foi enviada para um worker |
| 27 | p | A delivery está em processamento e ainda não recebeu acknowledgement. |
| 28 | span.tag | 3. Reconhecida |
| 29 | strong | O consumer confirmou a delivery |
| 30 | p | O broker pode tratar aquela entrega como concluída e remover a mensagem no momento adequado. |
| 31 | p | Essa separação evita uma leitura apressada: entregar não é o mesmo que encerrar. O ack pertence ao lado do consumer e protege a remoção da mensagem depois do processamento. Outros sinais do lado de quem publicou existem em outro ponto do fluxo e não dizem que um consumer processou a mensagem. |
| 32 | h2 | Consumer é inscrição em uma fila |
| 33 | p | Um consumer é a aplicação, processo ou worker registrado para receber mensagens de uma fila. A inscrição acontece na fila, não na exchange. Depois que esse registro existe, RabbitMQ passa a empurrar deliveries para o handler do consumer quando há mensagens disponíveis. |
| 34 | p | No exemplo emails , três workers podem se registrar na mesma fila. Isso não cria três cópias da mesma mensagem. Cria três candidatos para receber trabalhos diferentes daquela fila. A fila continua sendo uma sequência de mensagens; os workers dividem essa sequência. |
| 35 | code | emails |
| 36 | div.queue-contrast.visual-block@aria-label | Contraste entre workers na mesma fila e filas independentes |
| 37 | span.tag.blue | Uma fila, vários workers |
| 38 | strong.queue-title | Fila emails |
| 39 | code | emails |
| 40 | p | Mensagens: E1, E2, E3 |
| 41 | div.workers@aria-label | Workers competindo pela mesma fila |
| 42 | p.small | Cada worker recebe parte do trabalho. Uma mensagem não vira três cópias por existir três consumers. |
| 43 | span.tag | Várias filas, cópias independentes |
| 44 | strong.route-label | Publicação roteada |
| 45 | p | Um evento pode chegar a mais de uma fila quando a topologia assim define. |
| 46 | strong | Fila email |
| 47 | code | email |
| 48 | p | Cópia para envio de mensagens. |
| 49 | strong | Fila audit |
| 50 | code | audit |
| 51 | p | Cópia para registro de auditoria. |
| 52 | strong | Fila analytics |
| 53 | code | analytics |
| 54 | p | Cópia para leitura analítica. |
| 55 | p | Essa é a diferença que fecha o nível básico. Quando três serviços precisam processar o mesmo evento de forma independente, eles precisam de filas independentes recebendo cópias. Quando três workers só querem dividir o mesmo trabalho, eles ficam na mesma fila e competem pelas deliveries. |
| 56 | h2 | A responsabilidade de cada peça fica menor |
| 57 | p | Com filas e consumers no lugar certo, a topologia fica mais fácil de ler. A exchange não precisa saber quantos workers estão online. A fila não precisa reinterpretar a routing key. O consumer não decide para quais outros destinos a publicação deveria ter ido. Cada peça responde a uma pergunta menor. |
| 58 | th | Peça |
| 59 | th | Pergunta que responde |
| 60 | th | Limite útil neste node |
| 61 | td | Exchange |
| 62 | td | Para quais destinos a publicação deve ser roteada? |
| 63 | td | Não segura mensagem esperando worker. |
| 64 | td | Fila |
| 65 | td | Quais mensagens estão aguardando ou foram entregues sem ack? |
| 66 | td | Não representa um serviço inteiro quando vários serviços precisam de cópias próprias. |
| 67 | td | Consumer |
| 68 | td | Qual aplicação recebe uma delivery daquela fila? |
| 69 | td | Não assina a exchange diretamente no modelo trabalhado aqui. |
| 70 | td | Acknowledgement |
| 71 | td | Quando uma delivery pode ser considerada processada pelo consumer? |
| 72 | td | Não prova que a publicação foi aceita nem resolve confiabilidade de ponta a ponta. |
| 73 | div.legend@aria-label | Resumo conceitual de fila, consumer e cópia por fila |
| 74 | strong | Sem consumer online |
| 75 | span | A mensagem fica pronta na fila, desde que tenha sido roteada para ela. |
| 76 | strong | Com consumers na mesma fila |
| 77 | span | As deliveries são distribuídas como trabalho compartilhado. |
| 78 | strong | Com filas separadas |
| 79 | span | Cada fila guarda sua própria cópia e seu próprio ritmo de consumo. |
| 80 | h2 | O básico fecha quando a cópia tem endereço claro |
| 81 | p | Ao sair deste ponto, a leitura importante é simples: uma publicação vira cópia por fila, não por consumer. Depois que a cópia entra em uma fila, a conversa passa a ser entrega, processamento e ack. Essa base permite que o próximo nível trate contratos de topologia e decisões de desenho sem voltar a misturar roteamento, armazenamento e consumo. |
| 82 | h2 | Referências |
| 83 | li.reference-item | Documentação oficial de filas Uso neste node: define fila como coleção ordenada e registra estados de mensagens prontas ou entregues sem acknowledgement. |
| 84 | a | Documentação oficial de filas |
| 85 | span.reference-note | Uso neste node: define fila como coleção ordenada e registra estados de mensagens prontas ou entregues sem acknowledgement. |
| 86 | li.reference-item | Documentação oficial de consumers Uso neste node: sustenta que consumers se registram em filas e recebem deliveries a partir delas. |
| 87 | a | Documentação oficial de consumers |
| 88 | span.reference-note | Uso neste node: sustenta que consumers se registram em filas e recebem deliveries a partir delas. |
| 89 | li.reference-item | Guia oficial de acknowledgements Uso neste node: explica o reconhecimento de delivery pelo consumer e sua função na remoção segura. |
| 90 | a | Guia oficial de acknowledgements |
| 91 | span.reference-note | Uso neste node: explica o reconhecimento de delivery pelo consumer e sua função na remoção segura. |
| 92 | li.reference-item | Documentação oficial de exchanges Uso neste node: sustenta a fronteira entre roteamento por exchange e cópia para destinos ligados. |
| 93 | a | Documentação oficial de exchanges |
| 94 | span.reference-note | Uso neste node: sustenta a fronteira entre roteamento por exchange e cópia para destinos ligados. |
| 95 | li.reference-item | Guia oficial do modelo AMQP 0-9-1 Uso neste node: complementa o modelo de fila, consumer, subscription e acknowledgement no fluxo AMQP. |
| 96 | a | Guia oficial do modelo AMQP 0-9-1 |
| 97 | span.reference-note | Uso neste node: complementa o modelo de fila, consumer, subscription e acknowledgement no fluxo AMQP. |
