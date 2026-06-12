# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Bindings, routing key e destinos |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Básico · 03 de 06 |
| 4 | strong | Básico · 03 de 06 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Bindings, routing key e destinos |
| 7 | p | Anterior: Exchange padrão e publicação direta aparente · Próximo: Direct, fanout e topic |
| 8 | a | Exchange padrão e publicação direta aparente |
| 9 | a | Direct, fanout e topic |
| 10 | h1 | Bindings, routing key e destinos |
| 11 | p.lead | Uma exchange pode existir, receber uma publicação com orders.created e ainda assim não ter para onde mandar a mensagem. A diferença entre "existe" e "roteia" está nas regras ligadas a ela. |
| 12 | code | orders.created |
| 13 | p.meta | Pesquisa consultada em 2026-06-08: documentação oficial RabbitMQ 4.3 e especificação AMQP 0-9-1. |
| 14 | h2 | Uma exchange sem saídas ainda não tem rota |
| 15 | p | O node anterior mostrou a conveniência da exchange padrão. Agora a situação muda: imagine uma exchange de domínio chamada orders.events . Ela foi criada para receber eventos de pedido, mas ainda não há nenhuma regra dizendo quais destinos devem receber cada publicação. |
| 16 | code | orders.events |
| 17 | p | Nesse estado, a exchange não virou uma fila vazia. Uma fila vazia pode estar pronta para armazenar mensagens futuras. Uma exchange sem regras é uma tabela de roteamento vazia: ela tem entrada, mas não tem linhas de saída. |
| 18 | div.state-grid.visual-block@aria-label | Estado de uma exchange antes e depois de criar bindings |
| 19 | span.tag.warn | Antes |
| 20 | h3 | orders.events sem regras |
| 21 | code | orders.events |
| 22 | p | A publicação chega à exchange, mas a tabela não tem linha que aponte para um destino. |
| 23 | span.tag | Depois |
| 24 | h3 | orders.events com regras |
| 25 | code | orders.events |
| 26 | p | Cada linha liga a exchange a um destino e informa quando a publicação pode seguir por aquela saída. |
| 27 | p | A linha que cria uma saída é um binding . Ele não é a mensagem e não é o consumidor. É a regra de topologia que parte de uma exchange e aponta para um destino. |
| 28 | strong | binding |
| 29 | h2 | A publicação traz uma key; a regra também tem a sua |
| 30 | p | Quando o publisher envia uma mensagem para orders.events , ele pode carregar uma routing key . No exemplo condutor, a key da publicação é orders.created . Ela descreve o evento que entrou na exchange naquele momento. |
| 31 | code | orders.events |
| 32 | strong | routing key |
| 33 | code | orders.created |
| 34 | p | O binding, por sua vez, é criado antes da publicação. Ele também pode ter uma key registrada como critério da regra. Para separar as duas origens, este node chama essa key da regra de binding key . |
| 35 | strong | binding key |
| 36 | pre.code-block.language-text@aria-label | Comparação conceitual entre a key da publicação e a key da regra |
| 37 | code | # dado que acompanha a publicação publish.exchange = "orders.events" publish.routing_key = "orders.created" # dado registrado na regra da topologia binding.source = "orders.events" binding.destination = "orders.email" binding.binding_key = "orders.created" binding.arguments = {} |
| 38 | span.syntax-comment | # dado que acompanha a publicação |
| 39 | span.syntax-key | publish.exchange |
| 40 | span.syntax-op | = |
| 41 | span.syntax-value | "orders.events" |
| 42 | span.syntax-key | publish.routing_key |
| 43 | span.syntax-op | = |
| 44 | span.syntax-value | "orders.created" |
| 45 | span.syntax-comment | # dado registrado na regra da topologia |
| 46 | span.syntax-key | binding.source |
| 47 | span.syntax-op | = |
| 48 | span.syntax-value | "orders.events" |
| 49 | span.syntax-key | binding.destination |
| 50 | span.syntax-op | = |
| 51 | span.syntax-value | "orders.email" |
| 52 | span.syntax-key | binding.binding_key |
| 53 | span.syntax-op | = |
| 54 | span.syntax-value | "orders.created" |
| 55 | span.syntax-key | binding.arguments |
| 56 | span.syntax-op | = |
| 57 | span.syntax-value | {} |
| 58 | p | Os valores podem ser iguais, como no recorte acima, mas eles não vêm do mesmo lugar. A routing key nasce na publicação. A binding key vive na regra. Essa separação é o que permite olhar para uma topologia e prever o caminho da mensagem sem misturar o que o publisher informou com o que o broker já tinha configurado. |
| 59 | th | Peça |
| 60 | th | Quem define |
| 61 | th | Leitura correta |
| 62 | td | routing_key da publicação |
| 63 | code | routing_key |
| 64 | td | Publisher, no momento do envio |
| 65 | td | Valor que acompanha uma mensagem específica. |
| 66 | td | binding_key da regra |
| 67 | code | binding_key |
| 68 | td | Topologia, antes da publicação |
| 69 | td | Critério registrado para uma saída da exchange. |
| 70 | td | arguments do binding |
| 71 | code | arguments |
| 72 | td | Topologia, junto da regra |
| 73 | td | Parâmetros opcionais que certos tipos de exchange podem ler. |
| 74 | h2 | A mesma key pode encontrar mais de uma saída |
| 75 | p | Com as regras no lugar, a exchange avalia suas linhas. Uma publicação com orders.created pode encontrar uma saída, várias saídas ou nenhuma saída inicial. A cardinalidade não está na mensagem; ela aparece da combinação entre publicação, bindings e tipo de exchange. |
| 76 | code | orders.created |
| 77 | div.route-map.visual-block@aria-label | Mapa de uma exchange com bindings e destinos diferentes |
| 78 | span.tag.blue | Publicação |
| 79 | h3 | orders.events |
| 80 | code | orders.events |
| 81 | p | Recebe uma mensagem com a routing key orders.created . |
| 82 | code | orders.created |
| 83 | span.tag | Bindings |
| 84 | h3 | Linhas avaliadas |
| 85 | strong | binding key: orders.created |
| 86 | code | orders.created |
| 87 | span | Destino: orders.email |
| 88 | code | orders.email |
| 89 | strong | binding key: orders.created |
| 90 | code | orders.created |
| 91 | span | Destino: orders.audit |
| 92 | code | orders.audit |
| 93 | strong | binding key: orders.created |
| 94 | code | orders.created |
| 95 | span | Destino: orders.history |
| 96 | code | orders.history |
| 97 | span.tag | Destinos |
| 98 | h3 | Saídas alcançadas |
| 99 | span.kind | destination type: queue |
| 100 | strong | orders.email |
| 101 | code | orders.email |
| 102 | span.kind | destination type: queue |
| 103 | strong | orders.audit |
| 104 | code | orders.audit |
| 105 | span.kind | destination type: stream |
| 106 | strong | orders.history |
| 107 | code | orders.history |
| 108 | p | Esse mapa mostra três saídas para a mesma publicação. Se só uma linha combinasse, haveria uma rota. Se nenhuma linha combinasse, a exchange não encontraria destino inicial. O tratamento operacional dessa falta de saída fica para outro ponto do roadmap; aqui o importante é reconhecer o estado da tabela. |
| 109 | h2 | O binding tem origem, destino e tipo de destino |
| 110 | p | Ler um binding como seta é útil, mas incompleto. A regra tem uma exchange de origem, um destino, uma classificação do destino e, quando necessário, argumentos. Esses campos ajudam a distinguir "de onde a regra parte" de "para onde ela aponta". |
| 111 | th | Campo conceitual |
| 112 | th | O que ele responde |
| 113 | th | Exemplo no node |
| 114 | td | source exchange |
| 115 | td | Qual exchange avalia esta regra? |
| 116 | td | orders.events |
| 117 | code | orders.events |
| 118 | td | destination |
| 119 | td | Para qual recurso a rota aponta? |
| 120 | td | orders.email |
| 121 | code | orders.email |
| 122 | td | destination type |
| 123 | td | Que tipo de recurso é o destino? |
| 124 | td | queue , stream ou exchange |
| 125 | code | queue |
| 126 | code | stream |
| 127 | code | exchange |
| 128 | td | binding key |
| 129 | td | Qual critério textual está registrado na regra? |
| 130 | td | orders.created |
| 131 | code | orders.created |
| 132 | td | binding arguments |
| 133 | td | Há parâmetros adicionais da regra? |
| 134 | td | {} quando não há parâmetro extra |
| 135 | code | {} |
| 136 | p | O destino mais comum para começar a leitura é uma fila, porque ela torna visível onde a mensagem fica depois do roteamento. RabbitMQ também permite stream como destino e, em topologias mais compostas, outra exchange como destino. Esta página só precisa abrir esse vocabulário; o aprofundamento dessa forma de destino será tratado depois. |
| 137 | p | Fronteira do node. O tipo da exchange decide como routing key, binding key e argumentos participam da avaliação. O próximo node dá nome aos tipos principais e compara suas regras. Aqui, a pergunta é anterior: quais peças existem para que qualquer regra possa ser lida? |
| 138 | strong | Fronteira do node. |
| 139 | h2 | Como ler uma topologia pequena |
| 140 | p | Quando você olha para uma exchange, leia primeiro se há bindings. Depois, leia de onde cada binding parte, para onde aponta e qual critério ele registra. Só então compare com a publicação. |
| 141 | span.tag.blue | 1 |
| 142 | p | Entrada |
| 143 | strong | Entrada |
| 144 | p | Qual exchange recebeu a publicação e qual routing key veio junto? |
| 145 | span.tag | 2 |
| 146 | p | Regras |
| 147 | strong | Regras |
| 148 | p | Quais bindings existem a partir dessa source exchange? |
| 149 | span.tag | 3 |
| 150 | p | Saídas |
| 151 | strong | Saídas |
| 152 | p | Quais destinations são alcançados pelas regras que combinam? |
| 153 | p | Se essa leitura fica clara, a exchange deixa de ser uma caixa mágica. Ela vira uma tabela de regras: uma publicação entra, a exchange avalia seus bindings e os destinos alcançados recebem cópias conforme a topologia. |
| 154 | h2 | Referências |
| 155 | li.reference-item | F1 - documentação oficial RabbitMQ 4.3 Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 156 | a | F1 - documentação oficial RabbitMQ 4.3 |
| 157 | span.reference-note | Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 158 | li.reference-item | F2 - guia oficial RabbitMQ 4.3 Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
| 159 | a | F2 - guia oficial RabbitMQ 4.3 |
| 160 | span.reference-note | Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
