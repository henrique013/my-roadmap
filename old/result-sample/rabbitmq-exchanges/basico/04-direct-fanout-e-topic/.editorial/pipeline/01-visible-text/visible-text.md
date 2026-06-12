# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Direct, fanout e topic |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Básico · 04 de 06 |
| 4 | strong | Básico · 04 de 06 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Direct, fanout e topic |
| 7 | p | Anterior: Bindings, routing key e destinos · Próximo: Headers exchange e metadados de roteamento |
| 8 | a | Bindings, routing key e destinos |
| 9 | a | Headers exchange e metadados de roteamento |
| 10 | h1 | Direct, fanout e topic |
| 11 | p.lead | O node anterior deixou a exchange com bindings legíveis. Agora a pergunta muda: quando uma publicação chega com uma routing key, a exchange deve comparar por igualdade, copiar para todos os destinos ou testar um padrão? |
| 12 | p.meta | Pesquisa consultada em 2026-06-08: documentação oficial RabbitMQ 4.3, tutoriais oficiais e especificação AMQP 0-9. |
| 13 | h2 | A diferença está na pergunta que a exchange faz |
| 14 | p | Imagine três publicações pequenas: orders.created , logs.error e audit.user.login . Todas chegam a uma exchange, e todas carregam uma routing key. O que muda entre direct, fanout e topic não é a existência da key; é a pergunta que a exchange faz aos seus bindings. |
| 15 | code | orders.created |
| 16 | code | logs.error |
| 17 | code | audit.user.login |
| 18 | div.content-grid.visual-block@aria-label | Três modos de decisão para uma exchange com bindings |
| 19 | span.tag.blue | Direct |
| 20 | h3 | Igualdade exata |
| 21 | p | A key da publicação é comparada com a key registrada no binding. Se os textos são iguais, aquele destino entra na rota. |
| 22 | span.tag | Fanout |
| 23 | h3 | Cópia ampla |
| 24 | p | A publicação segue para todos os destinos ligados. A routing key pode existir, mas não participa do filtro. |
| 25 | span.tag.purple | Topic |
| 26 | h3 | Padrão por partes |
| 27 | p | A key é lida como segmentos separados por ponto, e o binding registra um padrão que pode ter curingas. |
| 28 | p | Esse trio é suficiente para muita topologia cotidiana porque cobre três intenções diferentes: escolher uma etiqueta exata, enviar cópia ampla ou deixar a fila interessada em uma família de keys. |
| 29 | h2 | Direct resolve quando a etiqueta precisa bater |
| 30 | p | Quando a intenção é uma etiqueta exata, a exchange só precisa perguntar se a routing key da publicação é igual à binding key da regra. Esse é o papel da direct exchange. |
| 31 | div.routing-lab.visual-block@aria-label | Exemplo conceitual de direct exchange com uma publicação e duas filas alcançadas |
| 32 | span.tag.blue | Publicação |
| 33 | h3 | Key enviada |
| 34 | span.key-pill | orders.created |
| 35 | p | A key vem com a mensagem. Ela não escolhe fila por si só; ela será comparada com os bindings da exchange. |
| 36 | span.tag | Bindings |
| 37 | h3 | Regras registradas |
| 38 | strong | Fila de notificação |
| 39 | span | orders.created combina. |
| 40 | code | orders.created |
| 41 | strong | Fila de auditoria |
| 42 | span | orders.created combina. |
| 43 | code | orders.created |
| 44 | strong | Fila de cancelamento |
| 45 | span | orders.cancelled não combina. |
| 46 | code | orders.cancelled |
| 47 | span.tag | Consequência |
| 48 | h3 | Mais de uma saída |
| 49 | p | A palavra direct não limita a rota a uma fila. Se duas filas têm bindings com a mesma key, as duas recebem cópias da publicação. |
| 50 | p | Por isso direct é suficiente quando a decisão principal cabe em uma key completa: orders.created , invoice.paid , logs.error . Ele fica fraco quando a key precisa carregar mais de um eixo de escolha e cada destino quer uma fatia diferente desses eixos. |
| 51 | code | orders.created |
| 52 | code | invoice.paid |
| 53 | code | logs.error |
| 54 | h2 | Fanout resolve quando escolher não faz parte da intenção |
| 55 | p | Às vezes a publicação não precisa selecionar uma categoria. O objetivo é que todos os destinos ligados recebam uma cópia. Nesse caso, a fanout exchange transforma a lista de bindings em uma lista de saídas, sem usar a routing key para filtrar. |
| 56 | th | Situação |
| 57 | th | Leitura correta |
| 58 | th | Consequência |
| 59 | td | logs.error chega a uma fanout exchange |
| 60 | code | logs.error |
| 61 | td | A key pode estar presente, mas a exchange não a consulta. |
| 62 | td | Todas as filas ligadas recebem cópia. |
| 63 | td | Uma fila ligada grava histórico e outra atualiza tela |
| 64 | td | São destinos diferentes recebendo a mesma publicação. |
| 65 | td | Isso é broadcast por topologia, não disputa entre consumidores. |
| 66 | td | Uma fila queria apenas erros críticos |
| 67 | td | Fanout não expressa esse filtro. |
| 68 | td | A topologia precisa de outra regra de decisão. |
| 69 | p | O ponto de corte. Se todos os destinos ligados devem receber tudo, fanout é direto e legível. Se algum destino precisa escolher por categoria, fanout já não está respondendo à pergunta certa. |
| 70 | strong | O ponto de corte. |
| 71 | h2 | Topic entra quando a key vira uma frase curta |
| 72 | p | Quando uma key exata fica estreita demais, a exchange pode ler a routing key como segmentos separados por ponto. A topic exchange compara essa key com um routing pattern registrado no binding. |
| 73 | p | Antes de olhar os curingas, veja a forma: audit.user.login tem três segmentos. O primeiro sugere uma família, o segundo uma área, o terceiro uma ação. O binding pode fixar alguns segmentos e deixar outros variarem. |
| 74 | code | audit.user.login |
| 75 | div.topic-strip.visual-block@aria-label | Segmentos de uma routing key topic |
| 76 | strong | audit |
| 77 | p.small | Primeiro segmento. Pode representar a família de eventos que interessa a uma fila. |
| 78 | strong | user |
| 79 | p.small | Segundo segmento. Pode variar quando a fila aceita várias áreas dentro da mesma família. |
| 80 | strong | login |
| 81 | p.small | Terceiro segmento. Pode ser fixo quando a fila só quer uma ação específica. |
| 82 | pre.code-block@aria-label | Padrões topic mínimos para comparar com uma routing key |
| 83 | code | # routing key publicada audit.user.login # padrões registrados em bindings audit.*.login => combina com exatamente um segmento no meio audit.# => combina com zero ou mais segmentos depois de audit orders.# => não combina com audit.user.login |
| 84 | span.syntax-comment | # routing key publicada |
| 85 | span.syntax-value | audit.user.login |
| 86 | span.syntax-comment | # padrões registrados em bindings |
| 87 | span.syntax-key | audit.*.login |
| 88 | span.syntax-op | => |
| 89 | span.syntax-value | combina com exatamente um segmento no meio |
| 90 | span.syntax-key | audit.# |
| 91 | span.syntax-op | => |
| 92 | span.syntax-value | combina com zero ou mais segmentos depois de audit |
| 93 | span.syntax-key | orders.# |
| 94 | span.syntax-op | => |
| 95 | span.syntax-risk | não combina com audit.user.login |
| 96 | p | O asterisco * cobre exatamente um segmento. A cerquilha # cobre zero ou mais segmentos. Essa diferença pequena muda muito a amplitude da rota: audit.*.login é seletivo; audit.# pega uma família inteira; # sozinho fica amplo a ponto de se aproximar de fanout para aquele binding. |
| 97 | code | * |
| 98 | code | # |
| 99 | code | audit.*.login |
| 100 | code | audit.# |
| 101 | code | # |
| 102 | h2 | Como escolher sem decorar tipo por tipo |
| 103 | p | A escolha fica mais simples quando começa pela intenção da fila, não pelo nome da exchange. Pergunte qual leitura a fila precisa fazer sobre cada publicação. |
| 104 | th | Intenção de roteamento |
| 105 | th | Tipo que costuma expressar melhor |
| 106 | th | Leitura da key |
| 107 | th | Cuidado imediato |
| 108 | td | Receber apenas uma etiqueta exata, como orders.created . |
| 109 | code | orders.created |
| 110 | td | Direct |
| 111 | td | Comparar igualdade entre binding key e routing key. |
| 112 | td | Mais de uma fila pode usar a mesma key. |
| 113 | td | Receber tudo que passar por aquela exchange. |
| 114 | td | Fanout |
| 115 | td | Não usar routing key como filtro. |
| 116 | td | Não usar quando o destino precisa escolher por categoria. |
| 117 | td | Receber uma família de keys com partes variáveis. |
| 118 | td | Topic |
| 119 | td | Comparar segmentos e curingas. |
| 120 | td | # pode abrir demais a rota. |
| 121 | code | # |
| 122 | p | O risco do padrão amplo. Em topic, # é útil quando a fila aceita uma família inteira de keys. Ele é perigoso quando vira atalho para "qualquer coisa". Quanto mais amplo o padrão, menos a topologia comunica a intenção real de cada destino. |
| 123 | strong | O risco do padrão amplo. |
| 124 | code | # |
| 125 | p | Quando essa leitura está clara, direct, fanout e topic deixam de ser nomes para memorizar. Eles viram três respostas para a mesma pergunta: a publicação deve bater exatamente, ir para todos os destinos ligados ou combinar com um padrão por segmentos? |
| 126 | h2 | Referências |
| 127 | li.reference-item | F1 - documentação oficial RabbitMQ 4.3 Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 128 | a | F1 - documentação oficial RabbitMQ 4.3 |
| 129 | span.reference-note | Uso neste node: Define exchanges, tipos, bindings, exchange padrão, propriedades, E2E e alternate exchanges na documentação corrente. |
| 130 | li.reference-item | F2 - guia oficial RabbitMQ 4.3 Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
| 131 | a | F2 - guia oficial RabbitMQ 4.3 |
| 132 | span.reference-note | Uso neste node: Explica o modelo AMQP 0-9-1: publishers, exchanges, bindings, queues, consumers e os quatro tipos clássicos. |
