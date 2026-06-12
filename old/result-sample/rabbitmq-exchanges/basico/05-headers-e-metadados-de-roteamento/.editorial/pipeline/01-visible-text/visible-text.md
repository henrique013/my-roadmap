# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Headers exchange e metadados de roteamento |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Básico · 05 de 06 |
| 4 | strong | Básico · 05 de 06 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Headers exchange e metadados de roteamento |
| 7 | p | Anterior: Direct, fanout e topic · Próximo: Filas, consumidores e entrega |
| 8 | a | Direct, fanout e topic |
| 9 | h1 | Headers exchange e metadados de roteamento |
| 10 | p.lead | Depois de direct, fanout e topic, aparece um caso em que a pergunta de roteamento não cabe bem em uma routing key textual: a mensagem precisa ser selecionada por atributos independentes. |
| 11 | p.meta | Pesquisa consultada em 2026-06-08: documentação oficial RabbitMQ 4.3, guia oficial AMQP 0-9-1 e especificação AMQP 0-9-1. |
| 12 | h2 | Quando uma key vira uma frase artificial |
| 13 | p | Imagine uma publicação de relatório. A rota depende de três critérios: tenant=acme , format=pdf e priority=high . É possível espremer tudo em uma key como acme.pdf.high , mas essa string mistura três eixos que não formam uma hierarquia natural. |
| 14 | code | tenant=acme |
| 15 | code | format=pdf |
| 16 | code | priority=high |
| 17 | code | acme.pdf.high |
| 18 | p | A mensagem AMQP também carrega um mapa de metadados separado do corpo. Esses metadados são os message headers. A headers exchange existe para ler esse mapa, comparar seus pares nome/valor com a regra do binding e decidir a rota sem depender da routing key. |
| 19 | div.message-map.visual-block@aria-label | Fronteira entre routing key, headers da mensagem e payload |
| 20 | span.tag.blue | Campo herdado |
| 21 | h3 | Routing key |
| 22 | p | Pode acompanhar a publicação, mas a headers exchange não usa esse campo para filtrar a mensagem. |
| 23 | span.tag | Metadados |
| 24 | h3 | Headers da mensagem |
| 25 | strong | tenant |
| 26 | span | acme |
| 27 | strong | format |
| 28 | span | pdf |
| 29 | strong | priority |
| 30 | span | high |
| 31 | span.tag.warn | Fora da decisão |
| 32 | h3 | Payload |
| 33 | p | O corpo segue junto, mas permanece opaco para a exchange. A rota não depende de abrir JSON, XML ou binário. |
| 34 | p | O ponto importante é que a exchange continua sendo roteador. A lógica não saiu para o consumidor nem passou a ler o conteúdo do corpo; ela mudou o dado de entrada da decisão: de key textual para headers da mensagem. |
| 35 | h2 | A regra fica no binding |
| 36 | p | Uma headers exchange não olha para qualquer header solto e decide sozinha. A ligação entre exchange e destino registra argumentos do binding. Esses argumentos dizem quais pares nome/valor devem combinar com os headers da mensagem. |
| 37 | div.match-flow.visual-block@aria-label | Comparacao entre argumentos do binding e headers da mensagem |
| 38 | span.tag.blue | Binding |
| 39 | h3 | Regra registrada |
| 40 | strong | tenant |
| 41 | span | acme |
| 42 | strong | format |
| 43 | span | pdf |
| 44 | strong | priority |
| 45 | span | high |
| 46 | span.tag | Mensagem |
| 47 | h3 | Headers recebidos |
| 48 | strong | tenant |
| 49 | span | acme |
| 50 | strong | format |
| 51 | span | pdf |
| 52 | strong | priority |
| 53 | span | high |
| 54 | span.tag | Resultado |
| 55 | h3 | Combina |
| 56 | p | Quando os pares exigidos batem com os headers relevantes, aquele destino entra na rota. |
| 57 | p | Se a mensagem viesse com format=csv , o par format=pdf deixaria de bater. A pergunta seguinte é inevitável: com três critérios, a exchange deve exigir todos ou aceitar que apenas um deles combine? |
| 58 | code | format=csv |
| 59 | code | format=pdf |
| 60 | h2 | O papel de x-match |
| 61 | code | x-match |
| 62 | p | Quando existe mais de um critério no binding, falta uma regra de combinação. O argumento especial x-match resolve essa ambiguidade: ele diz se a lista deve ser lida como "todos precisam bater" ou "qualquer um que bater já basta". |
| 63 | code | x-match |
| 64 | th | Valor de x-match |
| 65 | code | x-match |
| 66 | th | Como ler |
| 67 | th | Consequencia conceitual |
| 68 | td | all |
| 69 | code | all |
| 70 | td | Todos os pares relevantes do binding precisam combinar com os headers da mensagem. |
| 71 | td | Regra mais restritiva; boa quando a fila precisa exatamente daquele conjunto de atributos. |
| 72 | td | any |
| 73 | code | any |
| 74 | td | Um par relevante que combine já e suficiente. |
| 75 | td | Regra mais permissiva; a fila recebe mensagens que satisfazem ao menos um critério registrado. |
| 76 | td | all-with-x |
| 77 | code | all-with-x |
| 78 | td | Como all , mas também considera headers iniciados por x- na avaliacao. |
| 79 | code | all |
| 80 | code | x- |
| 81 | td | Variante documentada no RabbitMQ atual para incluir esses headers no match. |
| 82 | td | any-with-x |
| 83 | code | any-with-x |
| 84 | td | Como any , mas também considera headers iniciados por x- na avaliacao. |
| 85 | code | any |
| 86 | code | x- |
| 87 | td | Variante permissiva que inclui headers x- quando eles fazem parte da regra. |
| 88 | code | x- |
| 89 | pre.code-block@aria-label | Exemplo conceitual de argumentos de binding para headers exchange |
| 90 | code | # argumentos conceituais do binding x-match : all tenant : acme format : pdf priority : high |
| 91 | span.syntax-comment | # argumentos conceituais do binding |
| 92 | span.syntax-key | x-match |
| 93 | span.syntax-op | : |
| 94 | span.syntax-value | all |
| 95 | span.syntax-key | tenant |
| 96 | span.syntax-op | : |
| 97 | span.syntax-value | acme |
| 98 | span.syntax-key | format |
| 99 | span.syntax-op | : |
| 100 | span.syntax-value | pdf |
| 101 | span.syntax-key | priority |
| 102 | span.syntax-op | : |
| 103 | span.syntax-value | high |
| 104 | p | Esse trecho não é um comando. Ele apenas mostra a forma da regra: x-match pertence ao binding, enquanto tenant , format e priority são os critérios que a exchange compara com os headers da mensagem. |
| 105 | code | x-match |
| 106 | code | tenant |
| 107 | code | format |
| 108 | code | priority |
| 109 | h2 | Headers não substitui topic automaticamente |
| 110 | p | O node anterior mostrou que topic e bom quando uma routing key tem partes hierárquicas legíveis. Headers ficam mais claros quando a decisão depende de atributos independentes. A escolha deve preservar legibilidade da topologia. |
| 111 | div.compare-grid.visual-block@aria-label | Comparacao conceitual entre topic e headers |
| 112 | span.tag.purple | Topic |
| 113 | h3 | Quando a key tem forma de caminho |
| 114 | p | audit.user.login e legivel como familia, área e acao. O binding pode fixar partes e usar padroes sem criar vários campos paralelos. |
| 115 | code | audit.user.login |
| 116 | span.tag | Headers |
| 117 | h3 | Quando os critérios são eixos separados |
| 118 | p | tenant=acme , format=pdf e priority=high não precisam virar uma frase única. Cada atributo pode ser comparado pelo próprio nome. |
| 119 | code | tenant=acme |
| 120 | code | format=pdf |
| 121 | code | priority=high |
| 122 | th | Se a regra parece... |
| 123 | th | Modelo mais legivel |
| 124 | th | Cuidado imediato |
| 125 | td | Uma hierarquia textual curta, como audit.user.login . |
| 126 | code | audit.user.login |
| 127 | td | Topic tende a ser mais simples. |
| 128 | td | Não trocar por headers só para evitar pensar na convenção da key. |
| 129 | td | Um conjunto de atributos independentes, como tenant, formato e prioridade. |
| 130 | td | Headers tende a expressar melhor a decisão. |
| 131 | td | Manter poucos atributos com significado claro. |
| 132 | td | Um critério que exige ler o corpo da mensagem. |
| 133 | td | Não é decisão de headers exchange. |
| 134 | td | O payload continua opaco para o broker no roteamento. |
| 135 | p | Fronteira pratica. Headers são poderosos, mas headers mal padronizados tornam a topologia difícil de auditar. Também evite colocar dado sensível em header só porque ele facilita uma rota. |
| 136 | strong | Fronteira pratica. |
| 137 | h2 | O que precisa ficar claro ao sair deste node |
| 138 | p | Headers exchange completa os tipos básicos porque muda a pergunta de roteamento: em vez de comparar uma key textual ou um padrão, a exchange compara pares nome/valor de metadados. A regra continua no binding, x-match controla a combinação dos critérios, e o corpo da mensagem não entra na decisão. |
| 139 | code | x-match |
| 140 | p | Com os tipos clássicos cobertos, o próximo node separa definitivamente o que acontece depois da rota: fila, consumidor e entrega. |
| 141 | h2 | Referências |
| 142 | li.reference-item | F1 - documentação oficial RabbitMQ 4.3 Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 143 | a | F1 - documentação oficial RabbitMQ 4.3 |
| 144 | span.reference-note | Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 145 | li.reference-item | F2 - guia oficial RabbitMQ 4.3 Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
| 146 | a | F2 - guia oficial RabbitMQ 4.3 |
| 147 | span.reference-note | Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
