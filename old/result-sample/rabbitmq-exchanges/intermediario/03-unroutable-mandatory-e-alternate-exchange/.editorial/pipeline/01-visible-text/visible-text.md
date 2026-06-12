# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Quando a exchange não encontra caminho |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Intermediário · 03 de 07 |
| 4 | strong | Intermediário · 03 de 07 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Unroutable, mandatory e Alternate Exchange |
| 7 | p | Anterior: Broadcast vs consumidores competindo · Próximo: Dead Letter Exchanges e retry conceitual |
| 8 | a | Broadcast vs consumidores competindo |
| 9 | h1 | Quando a exchange não encontra caminho |
| 10 | p.lead | Uma publicação pode chegar à exchange certa e ainda assim não entrar em nenhuma fila. Esse ponto do fluxo decide se a mensagem some, volta para o publisher ou segue para uma rota alternativa. |
| 11 | h2 | A key nova ainda não tem destino |
| 12 | p | Imagine uma migração pequena: o producer de pedidos deixou de publicar `orders.created.v1` e passou a publicar `orders.created.v2`. A exchange existe, o nome dela está correto e a aplicação conseguiu enviar a publicação. O problema é mais estreito: a topologia ainda só tem binding para a key antiga. |
| 13 | p | Nesse instante, a exchange tenta aplicar a regra de routing que já vinha dos nodes anteriores. Ela olha para a routing key, compara com os bindings existentes e não encontra um destino compatível. A publicação está sem rota: chegou ao ponto de roteamento, mas não encontrou fila, stream ou outra exchange para receber a mensagem. |
| 14 | h2 | Três caminhos depois da tentativa de roteamento |
| 15 | p | Depois que a exchange não encontra destino, o desenho pode escolher entre silêncio, sinal ao publisher ou fallback de topologia. Os três caminhos partem do mesmo ponto, mas carregam responsabilidades diferentes. |
| 16 | div.visual-block@aria-label | Três caminhos de uma publicação sem rota |
| 17 | span.tag | Tentativa inicial |
| 18 | strong | Exchange de pedidos |
| 19 | p | Recebe `orders.created.v2` e não encontra binding compatível para essa routing key. |
| 20 | span.tag.warn | Sem pedido de retorno |
| 21 | span.branch-title | A publicação é descartada |
| 22 | p | Com `mandatory=false` e sem rota alternativa, o broker não devolve a mensagem ao publisher. O sinal precisa vir de métricas ou observação posterior. |
| 23 | span.tag.blue | Pedido de retorno |
| 24 | span.branch-title | A publicação volta ao publisher |
| 25 | p | Com `mandatory=true`, o broker retorna a mensagem sem rota. A aplicação publicadora precisa ter lógica de retorno para registrar, compensar ou corrigir o envio. |
| 26 | span.tag | Rota alternativa |
| 27 | span.branch-title | A publicação segue para uma AE |
| 28 | p | Com uma Alternate Exchange configurada, a exchange principal repassa a publicação para outra exchange, que tenta roteá-la por sua própria topologia. |
| 29 | p | O primeiro caminho é perigoso quando a equipe espera descobrir o problema pela aplicação. O segundo transforma a falha de rota em sinal para o publisher. O terceiro mantém a mensagem dentro de uma topologia de fallback, útil quando a arquitetura quer capturar publicações órfãs em vez de apenas avisar quem publicou. |
| 30 | h2 | O retorno só existe se alguém pediu para ouvir |
| 31 | p | O parâmetro `mandatory` pertence à publicação. Ele não muda o tipo da exchange nem cria uma fila. Ele apenas diz: se esta publicação não puder ser roteada, devolva a mensagem ao lado que publicou. |
| 32 | p | Em AMQP 0-9-1, esse retorno aparece como `basic.return`. A mensagem volta com informação suficiente para a aplicação entender qual exchange e qual routing key estavam envolvidas. Mas esse sinal só vira comportamento útil se o publisher tiver um handler de retorno. Sem essa lógica, a falha pode continuar invisível para o domínio, mesmo com a flag ligada. |
| 33 | pre.code-block.language-conf@aria-label | Recorte conceitual de publicação com retorno |
| 34 | code | # recorte conceitual, não executável publicacao.exchange = orders.events publicacao.routing_key = orders.created.v2 publicacao.mandatory = true publisher.on_return = registrar_e_corrigir_rota |
| 35 | span.syntax-comment | # recorte conceitual, não executável |
| 36 | span.syntax-key | publicacao.exchange |
| 37 | span.syntax-op | = |
| 38 | span.syntax-value | orders.events |
| 39 | span.syntax-key | publicacao.routing_key |
| 40 | span.syntax-op | = |
| 41 | span.syntax-value | orders.created.v2 |
| 42 | span.syntax-key | publicacao.mandatory |
| 43 | span.syntax-op | = |
| 44 | span.syntax-value | true |
| 45 | span.syntax-key | publisher.on_return |
| 46 | span.syntax-op | = |
| 47 | span.syntax-value | registrar_e_corrigir_rota |
| 48 | p | Esse recorte mostra a posição do mecanismo: o publisher pediu um retorno para aquela publicação. Ele ainda não sabe se um consumer processou a mensagem, nem recebeu prova de trabalho concluído. Ele recebeu um sinal de que a exchange não encontrou rota. |
| 49 | h2 | A rota alternativa pertence à exchange |
| 50 | p | Quando a intenção não é apenas avisar o publisher, mas preservar a publicação em um caminho controlado, a topologia pode configurar uma Alternate Exchange. A AE é uma exchange comum escolhida como destino alternativo para publicações que a exchange principal não conseguiu rotear. |
| 51 | p | No exemplo da migração, a exchange `orders.events` pode ter uma AE ligada a uma fila de órfãs. As mensagens com `orders.created.v2` que ainda não encontram binding na rota principal seguem para essa área de fallback. A equipe pode observar a fila, ajustar bindings e enxergar o período de transição sem perder silenciosamente as publicações. |
| 52 | pre.code-block.language-conf@aria-label | Recorte conceitual de exchange com fallback |
| 53 | code | # recorte conceitual, não executável exchange.principal = orders.events exchange.principal.alternate-exchange = orders.unrouted exchange.fallback = orders.unrouted fila.de_inspecao <- orders.unrouted |
| 54 | span.syntax-comment | # recorte conceitual, não executável |
| 55 | span.syntax-key | exchange.principal |
| 56 | span.syntax-op | = |
| 57 | span.syntax-value | orders.events |
| 58 | span.syntax-key | exchange.principal.alternate-exchange |
| 59 | span.syntax-op | = |
| 60 | span.syntax-value | orders.unrouted |
| 61 | span.syntax-key | exchange.fallback |
| 62 | span.syntax-op | = |
| 63 | span.syntax-value | orders.unrouted |
| 64 | span.syntax-key | fila.de_inspecao |
| 65 | span.syntax-op | <- |
| 66 | span.syntax-value | orders.unrouted |
| 67 | p | A diferença em relação ao retorno é estrutural. `mandatory` conversa com o publisher. A AE conversa com a topologia. Quando a mensagem é roteada pela AE, ela continua sendo uma mensagem roteada para o propósito de `mandatory`, porque encontrou um caminho alternativo. |
| 68 | h2 | Escolher sinal, fallback ou os dois |
| 69 | p | A decisão não precisa ser binária. Em muitos desenhos, `mandatory` ajuda a aplicação publicadora a saber que algo saiu do contrato esperado, enquanto a AE captura a publicação para análise ou tratamento genérico. O ponto é não confundir o papel de cada mecanismo. |
| 70 | th | Mecanismo |
| 71 | th | Quem recebe o sinal |
| 72 | th | O que acontece com a mensagem |
| 73 | th | Risco se for mal lido |
| 74 | td | `mandatory=true` |
| 75 | td | Publisher |
| 76 | td | Sem rota, a mensagem é retornada ao lado que publicou. |
| 77 | td | Tratar retorno como prova de processamento ou esquecer o handler de retorno. |
| 78 | td | Alternate Exchange |
| 79 | td | Topologia de fallback |
| 80 | td | Sem rota na exchange principal, a mensagem é republicada para a AE. |
| 81 | td | Transformar fallback em lixeira invisível e esconder quebra de contrato. |
| 82 | td | Sem `mandatory` e sem AE |
| 83 | td | Ninguém diretamente |
| 84 | td | A publicação sem rota pode ser descartada. |
| 85 | td | Descobrir tarde que uma key nova nunca chegou a nenhuma fila. |
| 86 | p | Quando a rota principal é parte de um contrato de domínio, o fallback precisa ser observável. Uma AE que captura tudo sem alerta pode parecer proteção, mas também pode mascarar uma topologia quebrada. |
| 87 | h2 | O limite está antes da fila |
| 88 | p | Este node termina no momento em que a exchange decidiu o destino inicial da publicação. Se a mensagem entrou em uma fila e depois saiu por rejeição, expiração, limite ou tentativa posterior, a história mudou de lugar: agora o problema está depois do roteamento inicial. |
| 89 | div.state-grid@aria-label | Fronteira entre falha de rota inicial e evento em fila já roteada |
| 90 | span.tag | Neste node |
| 91 | strong | A exchange não achou destino |
| 92 | p | A publicação ainda não chegou a uma fila. O desenho decide entre descarte, retorno ao publisher ou roteamento para AE. |
| 93 | span.tag.warn | Próximo passo |
| 94 | strong | A mensagem já estava em uma fila |
| 95 | p | Rejeição, expiração e retry pertencem ao momento posterior, quando uma fila já recebeu a mensagem e outro mecanismo passa a decidir a saída. |
| 96 | h2 | A pergunta certa fica no ponto de roteamento |
| 97 | p | Quando uma publicação não aparece em nenhuma fila, a primeira pergunta não é quantos consumers estão online. A pergunta é se a exchange recebeu uma routing key que algum binding reconhece. |
| 98 | p | Se a resposta for não, há três leituras estáveis: sem pedido de retorno e sem fallback, a mensagem pode sumir do caminho; com `mandatory`, o publisher pode ser avisado; com AE, a topologia ganha uma rota alternativa. Dominar este node é saber em qual desses pontos a arquitetura escolheu colocar o sinal. |
| 99 | h2 | Referências |
| 100 | li.reference-item | Documentação de publishers Uso neste node: sustenta mensagens sem rota, `mandatory`, retorno ao publisher e métricas de publicações sem rota. |
| 101 | a | Documentação de publishers |
| 102 | span.reference-note | Uso neste node: sustenta mensagens sem rota, `mandatory`, retorno ao publisher e métricas de publicações sem rota. |
| 103 | li.reference-item | Documentação de Alternate Exchanges Uso neste node: sustenta AE como fallback de roteamento e a relação entre AE e `mandatory`. |
| 104 | a | Documentação de Alternate Exchanges |
| 105 | span.reference-note | Uso neste node: sustenta AE como fallback de roteamento e a relação entre AE e `mandatory`. |
| 106 | li.reference-item | Documentação de exchanges Uso neste node: sustenta exchange como ponto de publicação e roteamento por bindings. |
| 107 | a | Documentação de exchanges |
| 108 | span.reference-note | Uso neste node: sustenta exchange como ponto de publicação e roteamento por bindings. |
| 109 | li.reference-item | Referência AMQP 0-9-1 Uso neste node: sustenta a semântica de `basic.publish`, `mandatory` e `basic.return`. |
| 110 | a | Referência AMQP 0-9-1 |
| 111 | span.reference-note | Uso neste node: sustenta a semântica de `basic.publish`, `mandatory` e `basic.return`. |
| 112 | li.reference-item | Documentação sobre acknowledgements e confirmações Uso neste node: sustenta a fronteira entre retorno de rota, confirmação do publisher e processamento pelo consumidor. |
| 113 | a | Documentação sobre acknowledgements e confirmações |
| 114 | span.reference-note | Uso neste node: sustenta a fronteira entre retorno de rota, confirmação do publisher e processamento pelo consumidor. |
