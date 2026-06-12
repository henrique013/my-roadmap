# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Quando a mensagem sai da fila |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Intermediário · 04 de 07 |
| 4 | strong | Intermediário · 04 de 07 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Dead Letter Exchanges e retry conceitual |
| 7 | p | Anterior: Unroutable, mandatory e Alternate Exchange · Próximo: Policies, x-arguments e permissões |
| 8 | a | Unroutable, mandatory e Alternate Exchange |
| 9 | h1 | Quando a mensagem sai da fila |
| 10 | p.lead | No node anterior, a mensagem ainda não tinha encontrado uma rota de entrada. Aqui a situação mudou: ela já chegou a uma fila, foi entregue ou ficou aguardando, e algum evento precisa tirá-la desse lugar sem transformar retry em repetição sem fim. |
| 11 | h2 | A fronteira muda depois que a fila recebeu a mensagem |
| 12 | p | Imagine uma mensagem de pedido em uma fila de trabalho. A exchange já fez seu papel: encontrou um binding, colocou a mensagem no destino certo e agora a fila controla a entrega para consumidores. Se o processamento falha nesse ponto, a pergunta técnica não é mais "por que a exchange não achou caminho?". A pergunta passa a ser "o que a fila deve fazer com uma mensagem que não pode continuar como se nada tivesse acontecido?". |
| 13 | p | Essa diferença protege a separação entre Alternate Exchange e Dead Letter Exchange. A AE aparece antes da fila, quando a exchange principal não consegue rotear uma publicação. A DLX aparece depois da fila, quando a mensagem já estava sob responsabilidade da fila e sai por uma condição específica. |
| 14 | div.visual-block@aria-label | Fronteira entre Alternate Exchange e Dead Letter Exchange |
| 15 | span.tag.warn | Antes da fila |
| 16 | strong | Falha de rota inicial |
| 17 | p | A exchange não encontra binding compatível. A saída possível é descarte, retorno ao publisher ou Alternate Exchange. |
| 18 | span.tag.blue | Depois da fila |
| 19 | strong | Saída posterior da fila |
| 20 | p | A mensagem já está em uma fila. Rejeição, expiração ou limite podem levar a fila a republicar a mensagem para uma DLX. |
| 21 | h2 | O consumer decide entre devolver e deixar sair |
| 22 | p | Quando um consumer recebe uma entrega, ele só deveria reconhecer positivamente depois de assumir o processamento. Se não consegue fazer isso, ele pode enviar um negative acknowledgement. Nesse ponto, o parâmetro `requeue` carrega uma decisão importante: voltar a mensagem para a mesma fila ou deixar que ela siga para outro destino configurado. |
| 23 | p | Com `requeue=true`, a mensagem volta para a fila e pode ser entregue de novo. Isso faz sentido quando outra instância pode processá-la agora, mas vira problema quando a causa continua presente. Com `requeue=false`, a mensagem não volta para a mesma fila; se a fila tiver uma Dead Letter Exchange configurada, o broker a republica para essa exchange. Esse movimento é o dead-lettering. |
| 24 | th | Decisão do consumer |
| 25 | th | Movimento imediato |
| 26 | th | Leitura conceitual |
| 27 | td | `basic.nack` ou `basic.reject` com `requeue=true` |
| 28 | td | A mensagem volta para a fila. |
| 29 | td | É uma nova tentativa rápida, não uma estratégia completa de retry. |
| 30 | td | `basic.nack` ou `basic.reject` com `requeue=false` |
| 31 | td | A mensagem sai da fila; com DLX configurada, é republicada para ela. |
| 32 | td | A fila decidiu que a mensagem precisa de outro caminho. |
| 33 | h2 | A DLX é exchange normal, apontada pela fila |
| 34 | p | O nome Dead Letter Exchange pode sugerir um mecanismo especial, mas a peça continua sendo uma exchange comum. O que muda é quem a usa: uma fila aponta para essa exchange como destino das mensagens que saem por dead-lettering. Depois da republicação, a DLX roteia por bindings como qualquer outra exchange. |
| 35 | pre.code-block.language-conf@aria-label | Recorte conceitual de fila apontando para uma DLX |
| 36 | code | # recorte conceitual, não executável fila_principal = orders.work fila_principal.dead_letter_exchange = orders.dlx dlx_exchange = orders.dlx destino_pos_saida = fila_de_quarentena_ou_espera |
| 37 | span.syntax-comment | # recorte conceitual, não executável |
| 38 | span.syntax-key | fila_principal |
| 39 | span.syntax-op | = |
| 40 | span.syntax-value | orders.work |
| 41 | span.syntax-key | fila_principal.dead_letter_exchange |
| 42 | span.syntax-op | = |
| 43 | span.syntax-value | orders.dlx |
| 44 | span.syntax-key | dlx_exchange |
| 45 | span.syntax-op | = |
| 46 | span.syntax-value | orders.dlx |
| 47 | span.syntax-key | destino_pos_saida |
| 48 | span.syntax-op | = |
| 49 | span.syntax-value | fila_de_quarentena_ou_espera |
| 50 | p | O recorte mostra a posição do mecanismo sem transformar isso em passo de configuração. A fila principal não vira DLX. A fila de quarentena também não é DLX. A DLX é a exchange que recebe a republicação e decide, pelos seus bindings, para onde a mensagem vai. |
| 51 | h2 | Quatro gatilhos levam ao mesmo ponto de saída |
| 52 | p | Rejeição do consumer é só um dos caminhos. A documentação de RabbitMQ lista outras condições que também podem levar a mensagem a ser dead-lettered. Elas têm causas diferentes, mas convergem no mesmo modelo: a fila tem uma mensagem que precisa sair e, se houver DLX, a republica para essa exchange. |
| 53 | div.visual-block@aria-label | Gatilhos de dead-lettering em RabbitMQ |
| 54 | span.tag.blue | Consumer |
| 55 | strong | Rejeição sem retorno |
| 56 | p | `basic.reject` ou `basic.nack` com `requeue=false` tira a mensagem da fila. |
| 57 | span.tag | Tempo |
| 58 | strong | TTL expirado |
| 59 | p | A mensagem ultrapassa seu tempo de vida e pode ser dead-lettered por expiração. |
| 60 | span.tag | Capacidade |
| 61 | strong | Limite de fila |
| 62 | p | Quando a fila excede limite de tamanho ou quantidade, mensagens podem sair por política de overflow. |
| 63 | span.tag.warn | Quorum queues |
| 64 | strong | Delivery limit |
| 65 | p | Em quorum queues, uma mensagem que excede o limite de entregas pode ser removida ou dead-lettered. |
| 66 | p | A lista é importante porque evita reduzir DLX a "erro do consumer". A fila pode dead-letter mensagens por uma decisão explícita do consumo, por expiração, por limite de acúmulo ou por uma proteção de tipo de fila. Em todos os casos, a DLX continua sendo o destino de republicação, não a causa em si. |
| 67 | h2 | Quarentena e espera são destinos diferentes |
| 68 | p | Depois que a DLX recebe a mensagem, a topologia precisa declarar uma intenção. Uma mensagem inválida pode ir para uma fila de quarentena, onde fica separada para análise. Uma falha transitória pode ir para uma retry queue, que segura a mensagem por algum tempo antes de uma nova tentativa. Os dois destinos usam DLX, mas respondem a problemas diferentes. |
| 69 | div.visual-block@aria-label | Destinos conceituais depois da DLX |
| 70 | span.tag | Isolar |
| 71 | strong | Quarantine queue |
| 72 | p | Boa para mensagem inválida, contrato inesperado ou caso que exige inspeção antes de voltar ao fluxo. |
| 73 | span.tag | Esperar |
| 74 | strong | Retry queue |
| 75 | p | Boa para falha transitória, desde que exista limite de tentativas e visibilidade do que está acumulando. |
| 76 | span.tag.risk | Evitar |
| 77 | strong | Loop sem dono |
| 78 | p | Ruim quando a mensagem circula entre filas sem critério de parada, sem atraso real ou sem sinal operacional. |
| 79 | h2 | Retry com atraso muda o ritmo da falha |
| 80 | p | Um retry conceitual precisa de mais do que "tentar de novo". Ele precisa reduzir pressão, dar tempo para uma dependência voltar e decidir quando parar. Um desenho básico com DLX e TTL usa uma fila de espera: a mensagem sai da fila principal, entra na fila de retry, expira depois do tempo configurado e volta para uma exchange de trabalho. |
| 81 | div.visual-block@aria-label | Fluxo conceitual de retry com atraso usando DLX e TTL |
| 82 | span.tag.blue | 1 |
| 83 | span.step-title | Fila principal |
| 84 | p | A mensagem está pronta para consumo e foi entregue a um consumer. |
| 85 | span.tag.blue | 2 |
| 86 | span.step-title | Saída planejada |
| 87 | p | O consumer rejeita sem recolocar imediatamente na mesma fila. |
| 88 | span.tag | 3 |
| 89 | span.step-title | DLX |
| 90 | p | A fila republica a mensagem para uma exchange de dead-letter. |
| 91 | span.tag | 4 |
| 92 | span.step-title | Fila de espera |
| 93 | p | A mensagem permanece em uma retry queue até o TTL expirar. |
| 94 | span.tag | 5 |
| 95 | span.step-title | Nova tentativa |
| 96 | p | Ao expirar, a mensagem pode ser roteada de volta ao fluxo de trabalho. |
| 97 | p | TTL ajuda a criar espera, mas não deve ser lido como agenda precisa. A documentação de RabbitMQ descreve caveats de expiração, incluindo situações em que mensagens expiradas só são removidas quando chegam ao início da fila ou quando outro evento força a avaliação. Para este node, a ideia importante é o ritmo: retry planejado desacelera a repetição e cria um lugar observável entre uma tentativa e outra. |
| 98 | h2 | O desenho precisa de um ponto de parada |
| 99 | p | A DLX não decide sozinha se a mensagem merece nova tentativa ou isolamento. Essa decisão vem do desenho da topologia e da leitura do consumer. Um erro transitório pode usar uma fila de espera; um erro definitivo deveria sair para quarentena; uma mensagem que já tentou demais precisa parar de pressionar a fila principal. |
| 100 | span.tag.risk | Requeue imediato |
| 101 | strong | Mesma causa, mesma fila |
| 102 | p | A mensagem volta rápido, encontra o mesmo problema e pode consumir capacidade sem progresso. |
| 103 | span.tag | Retry planejado |
| 104 | strong | Espera antes de tentar |
| 105 | p | A mensagem sai do circuito quente, aguarda e retorna com uma chance mais real de sucesso. |
| 106 | span.tag | Quarentena |
| 107 | strong | Sem retorno automático |
| 108 | p | A mensagem fica separada quando a próxima tentativa só repetiria uma falha conhecida. |
| 109 | p | Esse ponto de parada é o que torna retry diferente de repetição. Sem limite, cada volta parece uma ação, mas a arquitetura não aprende nada. Com uma saída explícita para análise, a mensagem deixa de competir com trabalho saudável. |
| 110 | h2 | Configuração rígida vira dívida operacional |
| 111 | p | Como DLX, TTL e limites são parâmetros de filas, a forma de aplicá-los importa. A documentação de RabbitMQ recomenda policies quando aplicável, porque elas permitem mudar parâmetros de grupos de filas em runtime. Colocar tudo como x-arguments fixos na declaração acopla a decisão ao código e torna mudanças de produção mais pesadas. |
| 112 | p | Este node só precisa dessa leitura: DLX é uma configuração de fila que aponta para uma exchange normal, e configurações desse tipo costumam precisar de governança. O próximo node aprofunda como policies, x-arguments e permissões definem quem pode mudar esses parâmetros e quais efeitos essa escolha traz. |
| 113 | h2 | A mensagem mudou de jurisdição |
| 114 | p | Quando uma mensagem não encontra rota, o problema pertence à exchange de entrada. Quando ela já está em uma fila e sai por rejeição, expiração ou limite, o problema pertence à fila e à política de saída desenhada para ela. |
| 115 | p | Dominar DLX é enxergar essa mudança de jurisdição: a fila decide que a mensagem não deve continuar no mesmo lugar, a DLX roteia a republicação, e a arquitetura escolhe se o próximo destino é análise, espera ou parada definitiva. |
| 116 | h2 | Referências |
| 117 | li.reference-item | Documentação de Dead Letter Exchanges Uso neste node: sustenta DLX como exchange normal, eventos de dead-lettering e recomendação contra x-arguments rígidos. |
| 118 | a | Documentação de Dead Letter Exchanges |
| 119 | span.reference-note | Uso neste node: sustenta DLX como exchange normal, eventos de dead-lettering e recomendação contra x-arguments rígidos. |
| 120 | li.reference-item | Documentação sobre acknowledgements de consumidor Uso neste node: sustenta `basic.nack`, `basic.reject`, `requeue` e a diferença entre voltar para a fila ou sair dela. |
| 121 | a | Documentação sobre acknowledgements de consumidor |
| 122 | span.reference-note | Uso neste node: sustenta `basic.nack`, `basic.reject`, `requeue` e a diferença entre voltar para a fila ou sair dela. |
| 123 | li.reference-item | Documentação de TTL e expiração Uso neste node: sustenta expiração de mensagens, relação com DLX e limites de precisão do TTL. |
| 124 | a | Documentação de TTL e expiração |
| 125 | span.reference-note | Uso neste node: sustenta expiração de mensagens, relação com DLX e limites de precisão do TTL. |
| 126 | li.reference-item | Documentação de limite de fila Uso neste node: sustenta queue length limit como causa de remoção ou dead-lettering. |
| 127 | a | Documentação de limite de fila |
| 128 | span.reference-note | Uso neste node: sustenta queue length limit como causa de remoção ou dead-lettering. |
| 129 | li.reference-item | Documentação de policies Uso neste node: sustenta a preferência por policies quando parâmetros de filas precisam mudar operacionalmente. |
| 130 | a | Documentação de policies |
| 131 | span.reference-note | Uso neste node: sustenta a preferência por policies quando parâmetros de filas precisam mudar operacionalmente. |
| 132 | li.reference-item | Documentação de publishers Uso neste node: sustenta a fronteira com publicações sem rota e Alternate Exchange. |
| 133 | a | Documentação de publishers |
| 134 | span.reference-note | Uso neste node: sustenta a fronteira com publicações sem rota e Alternate Exchange. |
| 135 | li.reference-item | Documentação de quorum queues Uso neste node: sustenta delivery limit como causa específica, sem aprofundar o comportamento avançado. |
| 136 | a | Documentação de quorum queues |
| 137 | span.reference-note | Uso neste node: sustenta delivery limit como causa específica, sem aprofundar o comportamento avançado. |
| 138 | li.reference-item | Guia de confiabilidade Uso neste node: sustenta a leitura de acknowledgements como transferência de responsabilidade e a necessidade de lidar com redelivery. |
| 139 | a | Guia de confiabilidade |
| 140 | span.reference-note | Uso neste node: sustenta a leitura de acknowledgements como transferência de responsabilidade e a necessidade de lidar com redelivery. |
