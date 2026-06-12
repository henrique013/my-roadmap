# Research dump - Filas, consumidores e entrega

## Metadados do Node

- Roadmap de origem: `rabbitmq-exchanges`
- Tema humano do roadmap: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: `basico`
- Node ID: `basico/06-filas-consumidores-e-entrega`
- Slug do node: `06-filas-consumidores-e-entrega`
- Label do node: Filas, consumidores e entrega
- Posição local: 6 de 6
- Node anterior no nível para incrementalidade: `basico/05-headers-e-metadados-de-roteamento` - Headers exchange e metadados de roteamento
- Próximo node no nível: nenhum; este node fecha o nível básico
- Node anterior na sequência global: `basico/05-headers-e-metadados-de-roteamento` - Headers exchange e metadados de roteamento
- Próximo node na sequência global: `intermediario/01-contrato-de-topologia-e-roteamento` - Contrato de topologia e roteamento
- Data da pesquisa: 2026-06-09
- Observações temporais: a documentação oficial consultada está na série RabbitMQ 4.3 em 2026-06-09. O recorte do node usa AMQP 0-9-1 e RabbitMQ 4.3. A noção central de fila, consumer e acknowledgement é estável, mas detalhes de prefetch, tipos de fila, transient queues, redelivery limits e publisher confirms são fronteiras de nodes posteriores ou de documentação operacional.

## Contrato Extraído do Roadmap

- Papel do node na corrente: fecha a base separando o que pertence à exchange do que pertence à fila e ao consumidor: armazenamento, entrega, concorrência e acknowledgement.
- Papel do nível no roadmap tri-level: estabilizar fundamentos, vocabulário indispensável e modelos mentais antes de tratar escolhas de topologia e decisões operacionais no intermediário.
- Pré-requisitos herdados:
  - Entender exchanges, bindings, routing keys e tipos clássicos.
  - Entender que exchanges roteiam e não armazenam como destino final.
  - Entender que uma publicação pode ser roteada para zero, uma ou várias filas conforme a topologia.
  - Entender que headers exchange, direct, fanout e topic já foram apresentados como variações da lógica de roteamento.
- O que o node introduz pela primeira vez:
  - Fila como armazenamento ordenado.
  - Consumer como subscription de entrega.
  - Acknowledgement de consumidor.
  - Competição entre consumidores da mesma fila.
- O que deve cobrir:
  - Explicar que filas armazenam mensagens prontas e entregues mas ainda não reconhecidas.
  - Mostrar que consumidores consomem de filas, não de exchanges.
  - Introduzir acknowledgements apenas como remoção segura da fila após processamento.
  - Diferenciar várias filas recebendo cópias de vários consumidores competindo dentro de uma fila.
- O que não deve cobrir:
  - Não aprofundar prefetch, retries, redelivery loops ou confirms.
  - Não discutir quorum queues ainda.
  - Não reabrir os tipos de exchange em detalhes.
- Perguntas do node:
  - Onde a mensagem fica se não houver consumidor online?
  - O que muda quando dois consumidores estão na mesma fila?
  - Por que broadcast exige múltiplas filas quando cada serviço precisa de sua própria cópia?
- Vocabulário conceitual:
  - ready message
  - delivered message
  - consumer
  - subscription
  - acknowledgement
  - competing consumers
- Exemplos e diagramas permitidos:
  - Cenário conceitual de uma fila `emails` com três workers competindo por mensagens.
  - Contraste visual entre uma fila com três consumers e três filas ligadas à mesma exchange.
- Armadilhas:
  - Achar que fanout para uma fila com três consumers entrega três cópias.
  - Confundir ack do consumidor com confirm do publisher.
  - Supor que exchange segura mensagem até o consumer aparecer.
- Critério de domínio: consegue explicar a diferença entre broadcast para filas e distribuição de carga entre consumidores da mesma fila.
- Handoff: a base está completa; o intermediário passa a tratar escolhas de topologia, falhas de roteamento e desenho operacional.
- Referências específicas herdadas do contrato:
  - F4: https://www.rabbitmq.com/docs/queues - definição oficial de filas e estados de mensagens.
  - F5: https://www.rabbitmq.com/docs/consumers - definição oficial de consumidores.
  - F6: https://www.rabbitmq.com/docs/confirms - base de acknowledgements e negative acknowledgements.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto no node 01:
  - Publisher publica em exchange.
  - Exchange roteia por bindings e não armazena mensagens como destino final.
  - Fila e consumer já foram citados como peças do fluxo, mas ainda não foram aprofundados.
- Conteúdo já coberto no node 02:
  - A aparente publicação direta em fila passa pela default exchange.
  - `exchange=""` não significa ausência de exchange.
- Conteúdo já coberto no node 03:
  - Binding é regra de roteamento entre exchange de origem e destino.
  - Routing key e binding key definem, conforme o tipo, quais destinos recebem a publicação.
  - Uma publicação pode chegar a zero, uma ou várias filas.
- Conteúdo já coberto no node 04:
  - Fanout envia uma cópia a cada destino ligado.
  - Direct e topic também podem chegar a mais de uma fila quando a topologia cria múltiplos matches.
  - O node atual pode usar fanout apenas como contraste curto, sem reexplicar tipos.
- Conteúdo já coberto no node 05:
  - Headers exchange roteia por atributos dos headers da mensagem.
  - Payload permanece opaco para o broker.
  - O node atual herda essa separação entre dado de roteamento e corpo da mensagem.
- Conteúdo que este node adiciona:
  - A fila é o ponto em que a mensagem fica acumulada para consumo.
  - Mensagem enfileirada pode estar pronta para entrega ou entregue e ainda não reconhecida.
  - Consumer é uma subscription registrada em uma fila.
  - Acknowledgement do consumidor permite ao broker tratar uma entrega como processada e futura candidata à remoção.
  - Vários consumers na mesma fila distribuem trabalho; várias filas ligadas à mesma publicação recebem cópias independentes.
- Conteúdo reservado a nodes futuros:
  - `intermediario/01-contrato-de-topologia-e-roteamento`: ownership de exchange, convenção de routing key e contrato publisher-topologia-consumer.
  - `intermediario/02-broadcast-vs-consumidores-competindo`: aprofundamento arquitetural de broadcast versus competição, incluindo prefetch e capacidade de consumer em cenários.
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: mensagem sem rota no momento da publicação.
  - `intermediario/04-dead-letter-exchanges-e-retry-conceitual`: saída posterior da fila por rejeição, TTL, limite ou dead-letter.
  - `intermediario/07-publisher-confirms-e-confiabilidade`: sinais do publisher, confirms e confiabilidade de publicação.
  - `avancado/03-quorum-queues-dlx-e-redelivery-limits`: quorum queues, delivery limit, redelivery e retries.
- Exemplos que não devem ser repetidos:
  - Não repetir a comparação detalhada direct/fanout/topic.
  - Não reutilizar o exemplo do node 05 com `tenant`, `format` e `priority`.
  - Não criar roteiro operacional com comandos, cliente de linguagem ou configuração.
- Definições tratadas como pré-requisito:
  - Exchange.
  - Binding.
  - Routing key.
  - Fanout como cópia por destino ligado.
  - Payload opaco.
- Termos que ainda precisam ser introduzidos neste node antes do uso visível:
  - fila como armazenamento ordenado;
  - mensagem pronta;
  - mensagem entregue sem reconhecimento;
  - consumer;
  - subscription;
  - acknowledgement;
  - consumers competindo.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/queues  
Tipo: documentação oficial  
Data consultada: 2026-06-09  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: define queue como coleção ordenada de mensagens, relaciona enfileirar e entregar, registra estados ready e delivered but not yet acknowledged e descreve métricas de fila.  
Tópicos cobertos: queue, FIFO, entrega para consumers, estados de mensagem, ordenação, métricas de ready e unacknowledged, limites de escopo sobre durabilidade.  
Limites da fonte: a página também cobre nomes de fila, argumentos, durabilidade, tipos de fila e recursos avançados; o HTML usa apenas o recorte necessário para separar armazenamento, entrega e estado.

ID: F2  
URL: https://www.rabbitmq.com/docs/consumers  
Tipo: documentação oficial  
Data consultada: 2026-06-09  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: define que consumers consomem de filas, que uma subscription faz RabbitMQ empurrar deliveries, e que entregas começam quando há mensagens prontas ou novas mensagens enfileiradas.  
Tópicos cobertos: consumer, subscription, queue como alvo de consumo, delivery, consumer tag, consumer capacity, diferença entre push e polling.  
Limites da fonte: detalhes de cancelamento, polling, prioridade de consumer, capacidade e prefetch ficam fora do HTML ou aparecem somente como fronteira conceitual.

ID: F3  
URL: https://www.rabbitmq.com/docs/confirms  
Tipo: documentação oficial  
Data consultada: 2026-06-09  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: ancora acknowledgements de consumidor e separa esse mecanismo de publisher confirms.  
Tópicos cobertos: consumer delivery acknowledgement, delivery tag, manual acknowledgement, noções de data safety, ortogonalidade entre acknowledgement de consumidor e confirmação do publisher.  
Limites da fonte: o node não aprofunda negative acknowledgements, requeue, prefetch ou publisher confirms; esses temas ficam para o intermediário.

ID: F4  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial  
Data consultada: 2026-06-09  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta o contraste entre exchange como roteador e fila como destino de armazenamento/entrega, além da afirmação de que fanout envia cópia a cada destino ligado.  
Tópicos cobertos: exchange, roteamento para filas, propósito de exchanges, fanout como cópia por fila/stream/exchange ligado.  
Limites da fonte: o HTML não reabre a comparação de tipos de exchange; usa a fonte apenas para posicionar a fronteira exchange versus fila.

ID: F5  
URL: https://www.rabbitmq.com/tutorials/amqp-concepts  
Tipo: guia oficial  
Data consultada: 2026-06-09  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3, modelo AMQP 0-9-1  
Motivo de uso: complementa o modelo AMQP: publishers publicam em exchanges, queues armazenam mensagens, consuming usa subscription por push, acknowledgements sinalizam recebimento/processamento e prefetch existe como fronteira para múltiplos consumers.  
Tópicos cobertos: modelo AMQP, queue, consumer, acknowledgement, prefetch em nível conceitual, atributos e payload.  
Limites da fonte: prefetch é mencionado apenas como fronteira para o próximo nível; o node atual não ensina tuning nem sequência operacional.

## Síntese por Fonte

F1 permite afirmar que uma queue em RabbitMQ é uma coleção ordenada de mensagens. A fonte também registra que mensagens são enfileiradas e desenfileiradas quando entregues a consumers, com semântica FIFO sujeita a exceções como prioridade, redelivery e múltiplos active consumers. Para este node, o ponto mais importante é o estado: uma mensagem enfileirada pode estar pronta para entrega ou entregue mas ainda sem acknowledgement do consumidor.

F2 sustenta que consumers consomem de filas. Uma aplicação se registra como consumer em uma fila, e RabbitMQ passa a empurrar deliveries para o handler fornecido pela aplicação. Se a fila já tiver mensagens prontas, as deliveries começam imediatamente; se estiver vazia, as próximas deliveries acontecem quando novas mensagens entrarem na fila. A mesma fonte fornece a noção de subscription e consumer tag, mas o HTML usa esses termos apenas na medida necessária para entender consumo a partir da fila.

F3 fornece a fronteira de segurança do acknowledgement: quando RabbitMQ entrega uma mensagem, ele precisa saber quando pode considerar essa entrega recebida e processada com sucesso. Acknowledgement de consumidor confirma a entrega ao node e permite que a mensagem entregue seja marcada para futura remoção. A fonte também deixa claro que acknowledgements de consumidor e publisher confirms resolvem problemas parecidos em lados diferentes do fluxo, mas são independentes. O HTML usa essa distinção apenas como fronteira, sem ensinar publisher confirms.

F4 mantém a separação global do roadmap: exchanges são entidades onde publishers publicam mensagens, e seu propósito é rotear mensagens para filas, streams ou outras exchanges. A página de exchanges também define fanout como envio de uma cópia a cada destino ligado, o que permite explicar por que "três consumers na mesma fila" não equivalem a "três filas recebendo cópias".

F5 reforça o modelo AMQP 0-9-1: queue armazena mensagens consumidas por aplicações; consumidores podem se inscrever para que o broker empurre mensagens; acknowledgement positivo informa que a aplicação recebeu e processou a mensagem; prefetch controla quantas mensagens podem ficar em trânsito antes de novos acknowledgements, mas esse detalhe deve ficar como fronteira para o intermediário.

## Afirmações Técnicas Importantes

Afirmação: uma fila em RabbitMQ é uma coleção ordenada de mensagens; mensagens são enfileiradas e entregues para consumers a partir dela.  
Base: F1  
Condição ou limite: a ordenação observada pode mudar em casos como prioridade, redelivery e múltiplos consumers; esses detalhes não são o foco do básico.  
Impacto didático: estabelece a fila como o ponto de armazenamento e entrega, não como regra de roteamento.

Afirmação: consumers consomem de filas; para consumir, precisa existir uma fila.  
Base: F2  
Condição ou limite: o node trata o fluxo push via subscription; polling por `basic.get` é desencorajado pela documentação e não pertence à narrativa principal.  
Impacto didático: corrige a fronteira sem abrir uma lista de erros: consumer não assina a exchange diretamente no modelo ensinado.

Afirmação: se uma fila está vazia no momento da inscrição, as entregas começam quando novas mensagens são enfileiradas; se já há mensagens prontas, a entrega pode começar imediatamente.  
Base: F2  
Condição ou limite: a existência de consumer online não é exigida para a fila acumular mensagens roteadas com sucesso, desde que a fila exista e a topologia aponte para ela.  
Impacto didático: responde onde a mensagem fica quando não há consumer online.

Afirmação: mensagens enfileiradas podem estar prontas para entrega ou entregues mas ainda sem acknowledgement.  
Base: F1  
Condição ou limite: a documentação apresenta esses estados para mensagens enfileiradas; o HTML usa a distinção conceitual, sem transformar em guia de métricas.  
Impacto didático: dá forma ao intervalo entre "está na fila" e "foi removida com segurança".

Afirmação: consumer acknowledgement confirma ao node que uma delivery foi recebida e processada com sucesso, permitindo marcar a mensagem entregue para futura remoção.  
Base: F3  
Condição ou limite: o node não cobre negative acknowledgements, requeue, redelivery loops nem prefetch.  
Impacto didático: introduz ack como mecanismo de segurança de remoção, não como sinal genérico de sucesso do sistema inteiro.

Afirmação: acknowledgements de consumidor e confirmações do lado do publisher são ortogonais.  
Base: F3  
Condição ou limite: o HTML deve mencionar isso apenas como fronteira curta, sem ensinar publisher confirms.  
Impacto didático: evita confundir "consumer terminou" com "broker aceitou publicação" e preserva o node intermediário de confiabilidade.

Afirmação: fanout envia uma cópia para cada destino ligado à exchange, não uma cópia para cada consumer que compartilha a mesma fila.  
Base: F4, inferência declarada a partir de F1 e F2  
Condição ou limite: "destino ligado" aqui é fila, stream ou exchange. O HTML usa fila para manter o recorte do roadmap.  
Impacto didático: separa broadcast para filas de distribuição de carga entre consumers competindo.

Afirmação: múltiplos consumers ativos na mesma fila dividem entregas; cada mensagem entregue sai como uma delivery para um consumer, e qualquer redelivery posterior pertence a detalhes fora do recorte básico.  
Base: F1, F2, F5  
Condição ou limite: a distribuição real pode ser afetada por prefetch, tempo de processamento, cancelamentos e redelivery; o intermediário aprofunda.  
Impacto didático: mostra a diferença entre escalar workers e criar cópias independentes para serviços diferentes.

## Conceitos Essenciais

Conceito: fila como armazenamento ordenado  
Explicação simples: lugar lógico onde mensagens roteadas com sucesso ficam acumuladas até serem entregues para consumers.  
Necessidade no node: é a peça que fecha o contraste com exchange, que roteia mas não guarda a mensagem para o consumer final.  
Relação com conceitos anteriores: usa exchanges e bindings como origem da entrada na fila.  
Relação com conceitos futuros: tipos de fila, durabilidade, quorum queues e limites de redelivery ficam para nodes posteriores.  
Riscos de confusão: tratar a fila como outro tipo de exchange ou como uma assinatura direta do consumer na exchange.  
Fonte base: F1, F4.

Conceito: mensagem pronta  
Explicação simples: mensagem que está na fila aguardando entrega.  
Necessidade no node: permite responder o que acontece quando não há consumer online ou quando os consumers estão ocupados.  
Relação com conceitos anteriores: depende de a mensagem ter sido roteada para uma fila.  
Relação com conceitos futuros: métricas de queue depth e capacidade ficam para observabilidade.  
Riscos de confusão: achar que a exchange mantém a mensagem aguardando consumer.  
Fonte base: F1, F2.

Conceito: mensagem entregue sem reconhecimento  
Explicação simples: mensagem que já foi enviada a um consumer, mas ainda não recebeu acknowledgement.  
Necessidade no node: mostra que entrega e remoção segura são momentos diferentes.  
Relação com conceitos anteriores: vem depois do roteamento e da fila.  
Relação com conceitos futuros: redelivery, requeue e DLX ficam fora.  
Riscos de confusão: concluir que "entregou" significa "pode apagar imediatamente" em todos os modos.  
Fonte base: F1, F3.

Conceito: consumer  
Explicação simples: aplicação ou parte de aplicação registrada para receber deliveries de uma fila.  
Necessidade no node: separa consumo de fila de publicação em exchange.  
Relação com conceitos anteriores: publishers publicam; consumers recebem de filas.  
Relação com conceitos futuros: consumer capacity, prefetch e tuning ficam para o intermediário.  
Riscos de confusão: tratar consumer como destino direto de binding.  
Fonte base: F2.

Conceito: subscription  
Explicação simples: registro do consumer em uma fila para que RabbitMQ empurre deliveries.  
Necessidade no node: explica o que "consumer está online" significa para a fila.  
Relação com conceitos anteriores: depende de fila existente.  
Relação com conceitos futuros: cancelamento de consumer e polling ficam fora.  
Riscos de confusão: usar a palavra "assinatura" como se fosse assinatura em exchange.  
Fonte base: F2.

Conceito: acknowledgement de consumidor  
Explicação simples: sinal do consumer para o broker dizendo que aquela delivery foi recebida e processada com sucesso.  
Necessidade no node: cria a fronteira entre entregar e remover com segurança.  
Relação com conceitos anteriores: acontece depois da fila entregar a mensagem.  
Relação com conceitos futuros: negative acknowledgement, requeue, redelivery, retry e publisher confirms ficam fora.  
Riscos de confusão: confundir com confirmação do lado do publisher ou com garantia de processamento exatamente uma vez.  
Fonte base: F3.

Conceito: consumers competindo  
Explicação simples: vários consumers registrados na mesma fila recebem mensagens diferentes da mesma sequência de trabalho.  
Necessidade no node: diferencia escalar workers de criar cópias independentes para serviços diferentes.  
Relação com conceitos anteriores: contrasta com fanout para várias filas.  
Relação com conceitos futuros: prefetch e consumer capacity explicam detalhes da distribuição observada no intermediário.  
Riscos de confusão: achar que cada consumer da mesma fila recebe uma cópia da mesma mensagem.  
Fonte base: F1, F2, F5.

## Relações Causais e Estruturais

- Exchange roteia; fila armazena e entrega. Condição: a mensagem precisa ter sido roteada com sucesso para a fila. Consequência: quando não há consumer online, a pergunta correta é sobre o estado da fila, não sobre a exchange.
- Fila com mensagem pronta e sem consumer online acumula trabalho. Condição: a fila existe e a mensagem foi enfileirada. Consequência: quando um consumer se registra, deliveries podem começar.
- Delivery não encerra sozinha o ciclo de segurança. Condição: modo com acknowledgement manual, que é o recorte conceitual do node. Consequência: a mensagem pode estar em estado entregue mas ainda sem acknowledgement.
- Acknowledgement de consumidor permite futura remoção da mensagem entregue. Condição: ack enviado no mesmo contexto de delivery conforme protocolo e biblioteca. Consequência: o broker passa a tratar aquela delivery como processada com sucesso.
- Uma fila com três workers distribui trabalho. Condição: os três consumers estão registrados na mesma fila. Consequência: cada mensagem é entregue a um deles, não copiada para todos.
- Três filas ligadas à mesma publicação criam cópias independentes. Condição: a exchange e seus bindings roteiam a publicação para três filas. Consequência: cada fila mantém seu próprio acúmulo, entrega e acknowledgement.

## Exemplos Técnicos Possíveis

Exemplo: fila `emails` com três workers.  
Mudança ou contraste mostrado: quando a fila tem mensagens `E1`, `E2`, `E3`, os workers recebem unidades diferentes de trabalho; adicionar worker aumenta capacidade de consumo, não cria cópia extra da mesma mensagem.  
Conceitos introduzidos: fila, consumer, subscription, consumers competindo, acknowledgement.  
Risco de escopo: pode virar tuning de prefetch ou throughput.  
Como manter conceitual: não mostrar comando, biblioteca ou configuração; usar apenas estados e setas.

Exemplo: exchange de pedidos ligada a três filas `email`, `audit` e `analytics`.  
Mudança ou contraste mostrado: a mesma publicação pode gerar uma cópia em cada fila; cada fila terá seu próprio consumer e seu próprio acknowledgement.  
Conceitos introduzidos: cópia por fila, broadcast para filas, independência de backlog por serviço.  
Risco de escopo: reabrir fanout/direct/topic.  
Como manter conceitual: usar "a topologia roteou para três filas" sem discutir tipo de exchange.

Exemplo: mensagem entregue a um worker mas ainda sem ack.  
Mudança ou contraste mostrado: a mensagem saiu da lista de prontas e entrou em um intervalo de entrega pendente; o ack fecha esse intervalo.  
Conceitos introduzidos: ready message, delivered but not acknowledged, acknowledgement.  
Risco de escopo: abrir negative acknowledgement, requeue e redelivery.  
Como manter conceitual: dizer apenas que esses detalhes existem fora do node, sem descrevê-los.

## Obrigações de Concretização Didática

Conceito ou relação: estados de uma mensagem dentro da fila.  
Tipo de demanda: estado | ordem  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: o leitor precisa ver a passagem "pronta para entrega" -> "entregue sem ack" -> "removível depois do ack"; prosa isolada tende a misturar entrega com remoção.  
Exemplo candidato: fila `emails` com mensagens prontas, delivery para worker e ack final.  
Fonte: F1, F3.  
Por que a prosa pode não bastar: os dois estados pertencem à fila, mas um já está em trânsito para o consumer.  
Risco de virar laboratório ou excesso: transformar em comando `basic.ack` ou fluxo de biblioteca.  
Como manter conceitual e mínimo: representar estados e consequência, sem sintaxe operacional.  
Fronteira com nodes futuros: negative ack, requeue, redelivery e prefetch ficam fora.

Conceito ou relação: uma fila com vários workers versus várias filas recebendo cópias.  
Tipo de demanda: contraste | topologia  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: é o contraste central do node e precisa ficar visível como diferença estrutural, não só como frase.  
Exemplo candidato: `emails` com três workers competindo versus `email`, `audit` e `analytics` como filas separadas.  
Fonte: F2, F4, inferência declarada a partir de F1.  
Por que a prosa pode não bastar: "três consumers" e "três filas" parecem parecidos quando descritos em texto corrido.  
Risco de virar laboratório ou excesso: discutir tipos de exchange, binding keys ou configuração de consumidor.  
Como manter conceitual e mínimo: desenhar apenas caixas e setas sem declarar tipo de exchange.  
Fronteira com nodes futuros: aprofundamento arquitetural de broadcast e prefetch fica em `intermediario/02-broadcast-vs-consumidores-competindo`.

Conceito ou relação: quem é responsável por cada trecho do fluxo.  
Tipo de demanda: fronteira  
Primitiva visual escolhida: tabela curta  
Justificativa da primitiva: consolidar depois da narrativa ajuda a separar exchange, fila, consumer e ack sem criar uma seção de checklist.  
Exemplo candidato: tabela "peça, pergunta que responde, limite".  
Fonte: F1, F2, F3, F4.  
Por que a prosa pode não bastar: a confusão principal do básico é atribuir responsabilidade à peça errada.  
Risco de virar laboratório ou excesso: listar muitos recursos operacionais.  
Como manter conceitual e mínimo: quatro linhas no máximo, sem comandos nem parâmetros.  
Fronteira com nodes futuros: contrato de topologia, falhas de rota e confiabilidade de publicação ficam fora.

## Riscos, Armadilhas e Erros Comuns

- Achar que fanout para uma fila com três consumers entrega três cópias. Base: F4 mais F2; fanout copia para destinos ligados, e consumer consome de fila.
- Confundir acknowledgement de consumidor com confirmação do lado do publisher. Base: F3; são mecanismos ortogonais e independentes.
- Supor que a exchange segura a mensagem até aparecer consumer. Base: F4 e F1; exchange roteia, fila armazena.
- Tratar "entregue" como "removido com segurança". Base: F1 e F3; existe estado entregue mas ainda sem acknowledgement.
- Antecipar prefetch e capacity no básico. Base: F1, F2, F5; esses detalhes existem, mas pertencem ao aprofundamento intermediário.
- Usar "broadcast" como sinônimo de "mais workers". Base: F4 e inferência declarada; broadcast para serviços independentes exige destinos independentes, normalmente filas distintas.

## Limites e Fora de Escopo

- Este node explica:
  - fila como armazenamento ordenado;
  - consumo a partir de fila;
  - diferença entre mensagem pronta e mensagem entregue sem ack;
  - acknowledgement de consumidor como remoção segura após processamento;
  - diferença entre cópia por fila e competição entre consumers da mesma fila.
- Este node pode mencionar como fronteira:
  - prefetch;
  - consumer capacity;
  - redelivery;
  - negative acknowledgement;
  - publisher-side signals;
  - DLX e retry.
- Este node não explica:
  - tuning de prefetch;
  - retries, requeue ou redelivery loop;
  - quorum queues;
  - publisher confirms;
  - mandatory, alternate exchange ou unroutable;
  - configuração por linguagem, comandos ou laboratório.
- Fora do roadmap:
  - tutorial de biblioteca cliente;
  - setup local de RabbitMQ;
  - guia de performance;
  - estratégia completa de confiabilidade ou exactly-once.

## Divergências, Versões e Notas Temporais

- RabbitMQ 4.3 documenta que transient non-durable non-exclusive classic queues estão depreciadas e desabilitadas por padrão a partir de 4.3.0, mas essa mudança é de operação/tipo de fila e não entra no HTML do node básico.
- A documentação atual de queues menciona streams como estrutura alternativa. O roadmap é sobre exchanges no modelo AMQP 0-9-1; streams aparecem apenas como limite fora do recorte do node.
- Prefetch aparece nas fontes como forma de limitar entregas pendentes e influenciar múltiplos consumers, mas o contrato do node impede aprofundamento aqui. O HTML pode dizer que a distribuição real tem detalhes posteriores, sem ensinar prefetch.
- O guia de confirms separa acknowledgements de consumer e publisher confirms. O HTML deve preparar acknowledgement do consumer e só marcar que sinais do publisher são outro trecho do fluxo.

## Ordem de Introdução Conceitual para o HTML

1. Abrir com uma mensagem de e-mail já roteada para uma fila, mas sem worker online.
2. Mostrar que, depois da exchange, a pergunta deixa de ser roteamento e vira armazenamento/entrega.
3. Nomear fila como coleção ordenada onde a mensagem pode ficar pronta para entrega.
4. Registrar consumer como aplicação inscrita em uma fila para receber deliveries.
5. Separar estado pronto de estado entregue mas ainda não reconhecido.
6. Nomear acknowledgement como sinal do consumer que fecha a entrega com segurança.
7. Voltar ao exemplo `emails` com três workers para mostrar competição por trabalho.
8. Contrastar com três filas independentes recebendo cópias da mesma publicação.
9. Consolidar responsabilidades em tabela curta.
10. Fechar o básico apontando para o intermediário, onde topologia e falhas de rota viram decisões.

## Insumos para `.editorial/concept-ledger.md`

- Conceitos permitidos no HTML:
  - fila;
  - mensagem pronta;
  - delivery;
  - consumer;
  - subscription;
  - acknowledgement;
  - consumers competindo;
  - cópia por fila;
  - broadcast para filas.
- Conceitos permitidos só no dump:
  - basic.get;
  - consumer tag;
  - channel QoS;
  - transient non-exclusive classic queue.
- Conceitos reservados a nodes futuros:
  - prefetch;
  - consumer capacity;
  - negative acknowledgement;
  - requeue;
  - redelivery;
  - retry;
  - dead-letter exchange;
  - quorum queue;
  - publisher confirm;
  - mandatory;
  - alternate exchange;
  - exactly-once.
- Títulos de fontes precisam ser adaptados no HTML:
  - "Consumer Acknowledgements and Publisher Confirms" deve aparecer como "Guia oficial de acknowledgements" para não introduzir publisher confirms no rodapé.
  - "AMQP 0-9-1 Model Explained" pode aparecer como "Guia oficial do modelo AMQP 0-9-1".

## Candidatos de Narrativa para o HTML

Narrativa candidata A: estado da mensagem depois do roteamento.  
Pergunta-motor: onde a mensagem fica e quando ela deixa de estar sob responsabilidade da fila?  
Força: alinha perfeitamente com fila, delivery e acknowledgement.  
Risco: pode ficar abstrata sem contraste entre uma e várias filas.  
Decisão: usar como narrativa dominante.

Narrativa candidata B: contraste entre broadcast e workers.  
Pergunta-motor: por que três workers não significam três cópias?  
Força: ataca a armadilha mais importante.  
Risco: vira correção cedo demais e invade o intermediário.  
Decisão: usar como segunda metade, depois que estado da fila e ack já estiverem preparados.

Narrativa candidata C: fronteira de responsabilidades.  
Pergunta-motor: qual peça responde qual pergunta no fluxo?  
Força: fecha o nível básico.  
Risco: virar tabela/checklist.  
Decisão: usar como consolidação curta, não como estrutura principal.

## Exemplo Condutor Escolhido

Exemplo principal: uma fila `emails` recebe mensagens já roteadas e tem três workers. A narrativa acompanha primeiro uma mensagem parada sem worker, depois uma delivery pendente de ack, e por fim a diferença entre três workers na mesma fila e três filas independentes (`email`, `audit`, `analytics`) recebendo cópias.

Por que este exemplo serve:

- é pequeno e conceitual;
- usa o vocabulário de fila/consumer sem depender de linguagem;
- mostra estado, ordem e contraste;
- não repete o exemplo de headers do node anterior;
- evita comandos e configuração.

## Situação de Abertura e Tom

- Situação de abertura: a topologia já roteou um evento para a fila `emails`, mas nenhum worker está online naquele instante.
- Transformação acompanhada: a mensagem passa de "roteada para uma fila" para "pronta", depois "entregue mas aguardando ack", e só então "removível".
- Momento de nomeação: "fila" pode aparecer cedo como conceito herdado, mas "mensagem pronta", "delivery", "consumer", "subscription" e "acknowledgement" devem vir depois da necessidade.
- Risco de tom corretivo: alto na parte de broadcast versus consumers. O HTML deve construir primeiro o modelo da fila e só depois contrastar.
- Necessidades reais de visualização:
  - estado da mensagem;
  - contraste entre uma fila com workers e múltiplas filas.
