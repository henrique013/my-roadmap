# Research dump - Dead Letter Exchanges e retry conceitual

## Metadados do Node

- Roadmap de origem: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: intermediario
- `node_id`: `intermediario/04-dead-letter-exchanges-e-retry-conceitual`
- Slug do node: `04-dead-letter-exchanges-e-retry-conceitual`
- Label do node: Dead Letter Exchanges e retry conceitual
- Posição numérica local no nível: 04 de 07
- Node anterior e próximo do mesmo nível para incrementalidade: anterior `intermediario/03-unroutable-mandatory-e-alternate-exchange`; próximo `intermediario/05-policies-x-arguments-e-permissoes`
- Node anterior e próximo na sequência global do roadmap: anterior `intermediario/03-unroutable-mandatory-e-alternate-exchange`; próximo `intermediario/05-policies-x-arguments-e-permissoes`
- Data da pesquisa: 2026-06-10
- Observações temporais: documentação oficial consultada na série RabbitMQ 4.3. O recorte técnico é RabbitMQ 4.3 com AMQP 0-9-1 como vocabulário principal de acknowledgements de consumidor. A página de quorum queues em 4.3 tem mudanças relevantes sobre `delivery-count`, `acquired-count` e delayed retry; por isso esses pontos ficam como fronteira conceitual, não como aprofundamento.

## Contrato Extraído do Roadmap

- Papel do node na corrente: separa DLX de AE e mostra como filas republiquem mensagens para uma exchange normal em rejeição, TTL, limite ou delivery-limit.
- Papel do nível no roadmap tri-level: arquitetura, relações, decisões e trade-offs.
- Pré-requisitos herdados:
  - Entender `unroutable` e AE como falha de roteamento na entrada.
  - Entender que exchange roteia e fila armazena para entrega posterior.
  - Entender que o node anterior terminou antes da fila: a publicação não encontrou binding compatível.
- Introduz pela primeira vez:
  - Dead Letter Exchange.
  - Negative acknowledgement.
  - `requeue=false`.
  - TTL.
  - Queue length limit.
  - Delivery limit.
- Deve cobrir:
  - Definir DLX como exchange normal configurada em filas.
  - Listar os eventos que levam uma mensagem a dead-lettering.
  - Diferenciar falha de roteamento inicial de saída posterior da fila.
  - Explicar por que DLX é base de quarentena, análise e retry com atraso.
  - Registrar que policies são preferíveis a x-arguments rígidos para DLX quando aplicável.
- Não deve cobrir:
  - Não desenhar passo a passo de implementação.
  - Não aprofundar quorum queues e delivery-limit além da fronteira conceitual.
  - Não confundir DLX com fila morta; a exchange roteia para filas de destino.
- Perguntas do node:
  - Por que DLX não é um tipo especial de exchange?
  - Quais eventos fazem a mensagem sair da fila para dead-lettering?
  - Como `requeue=true` infinito difere de dead-lettering planejado?
- Vocabulário conceitual:
  - DLX.
  - dead-lettering.
  - `basic.nack`.
  - `basic.reject`.
  - TTL.
  - delivery-limit.
  - retry queue.
  - quarantine queue.
- Exemplos e diagramas permitidos:
  - Fluxo conceitual: fila principal -> DLX -> fila de análise ou espera -> exchange principal.
  - Cenário de mensagem inválida separada para fila de quarentena.
- Armadilhas:
  - Chamar DLX de fila.
  - Declarar DLX no papel e não garantir que a exchange destino exista.
  - Criar loops de retry sem limite ou observabilidade.
  - Usar `requeue=true` como substituto de política de retry.
- Critério de domínio: consegue explicar quando a mensagem é dead-lettered e como a DLX participa sem armazenar a mensagem por si mesma.
- Handoff: depois de DLX, o próximo node trata policies, x-arguments e permissões que governam essas configurações.
- Referências específicas do contrato:
  - F7 `https://www.rabbitmq.com/docs/dlx`: eventos e configuração de Dead Letter Exchanges.
  - F6 `https://www.rabbitmq.com/docs/confirms`: negative acknowledgements e requeue.
  - F12 `https://www.rabbitmq.com/docs/quorum-queues`: delivery-limit e dead-lettering em quorum queues.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto:
  - `basico/01-modelo-amqp-e-papel-da-exchange`: exchange roteia, não armazena como fila.
  - `basico/03-bindings-routing-key-e-destinos`: binding e routing key conectam exchange a destinos.
  - `basico/06-filas-consumidores-e-entrega`: fila é o ponto de acúmulo e entrega ao consumidor; acknowledgements existem como parte do fluxo de consumo.
  - `intermediario/01-contrato-de-topologia-e-roteamento`: producer publica contra contrato de topologia, não contra detalhes internos de consumidores.
  - `intermediario/02-broadcast-vs-consumidores-competindo`: múltiplas filas criam cópias independentes; múltiplos consumers na mesma fila competem pelo trabalho.
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: falha de roteamento inicial, `mandatory`, `basic.return` e AE.
- Conteúdo que pode ser reutilizado:
  - Exchange é roteador normal; a DLX herda esse conceito e não precisa redefinir exchange.
  - O contraste AE vs DLX pode ser usado uma vez: AE cuida de publicação que não achou rota; DLX cuida de mensagem que já estava em uma fila e saiu dela.
  - A ideia de rota alternativa pode ser reaproveitada, mas agora a origem do movimento é a fila, não a exchange inicial.
- Conteúdo reservado a nodes futuros:
  - `intermediario/05-policies-x-arguments-e-permissoes`: governança, precedência, permissões e alteração operacional de configurações via policies e argumentos opcionais.
  - `intermediario/07-publisher-confirms-e-confiabilidade`: publisher confirms em profundidade.
  - `avancado/01-diagnostico-de-roteamento-e-observabilidade`: diagnóstico operacional com métricas, sinais e investigação.
  - `avancado/03-quorum-queues-dlx-e-redelivery-limits`: at-least-once dead-lettering, detalhes de delivery-limit, delayed retry de quorum queues e garantias em cluster.
- Exemplos que não devem ser repetidos:
  - Não repetir o exemplo de migração de routing key do node anterior.
  - Não repetir tabela sobre descarte, retorno ao publisher e AE.
  - Não transformar retry em sequência de comandos, laboratório ou implementação cliente a cliente.
- Definições que podem ser tratadas como pré-requisito:
  - Exchange roteia conforme bindings.
  - Fila armazena mensagens prontas para entrega.
  - Consumer reconhece ou rejeita entregas.
  - AE já significa fallback de roteamento na entrada.
- Termos que ainda precisam ser introduzidos no HTML:
  - Dead Letter Exchange.
  - Dead-lettering.
  - Negative acknowledgement.
  - `requeue=false`.
  - TTL.
  - Queue length limit.
  - Delivery limit.
  - Retry queue.
  - Quarantine queue.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/dlx  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: base principal para DLX, eventos de dead-lettering, configuração por policy ou x-argument, routing key de dead-lettering, ciclo de dead-letter e efeitos sobre headers.  
Tópicos cobertos: mensagem dead-lettered, DLX como exchange normal, `dead-letter-exchange`, `dead-letter-routing-key`, eventos `rejected`, `expired`, `maxlen`, `delivery_limit`, segurança e `x-death`.  
Limites da fonte: detalha também segurança e headers; o HTML usa apenas o necessário para o modelo conceitual e deixa garantias avançadas para node futuro.

ID: F2  
URL: https://www.rabbitmq.com/docs/confirms  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta consumer acknowledgements, negative acknowledgements, `basic.reject`, `basic.nack`, diferença entre `requeue=true` e `requeue=false`, e risco de loops de redelivery.  
Tópicos cobertos: acknowledgement manual, negative acknowledgement, requeue, prefetch, publisher confirms.  
Limites da fonte: publisher confirms só aparecem como fronteira; node atual não aprofunda confiabilidade do publisher.

ID: F3  
URL: https://www.rabbitmq.com/docs/ttl  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta TTL de mensagem, TTL por fila, menor valor entre TTL por fila e por mensagem, relação entre expiração e dead-lettering, e ressalva de que expiração não é agendador preciso.  
Tópicos cobertos: `message-ttl`, `expiration`, per-message TTL, per-queue TTL, remoção de mensagens expiradas, race com entrega ao consumidor.  
Limites da fonte: não define estratégia de retry completa; o HTML usa TTL como peça conceitual de espera.

ID: F4  
URL: https://www.rabbitmq.com/docs/maxlength  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta queue length limit como evento que pode remover ou dead-letter mensagens e registra que mensagens unacknowledged não contam para o limite de ready messages.  
Tópicos cobertos: limite por quantidade ou bytes, policy recomendada, overflow, `drop-head`, `reject-publish`, `reject-publish-dlx`.  
Limites da fonte: o HTML menciona limite como causa de dead-lettering, sem virar aula de capacidade ou overflow.

ID: F5  
URL: https://www.rabbitmq.com/docs/policies  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta a recomendação curta de preferir policies para parâmetros que podem mudar em runtime, em vez de acoplar tudo em argumentos de declaração.  
Tópicos cobertos: policies como mecanismo declarativo por vhost, x-arguments, alteração de propriedades de grupos de queues e exchanges.  
Limites da fonte: detalhes de precedência, permissões, operator policies e governança ficam para o próximo node.

ID: F6  
URL: https://www.rabbitmq.com/docs/publishers  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta a fronteira com o node anterior: publicação sem rota, `mandatory`, `basic.return` e AE pertencem à entrada, não à saída posterior de uma fila.  
Tópicos cobertos: publicação em exchange, mensagens sem rota, `mandatory`, Alternate Exchange.  
Limites da fonte: usada como contraste, não como conteúdo principal.

ID: F7  
URL: https://www.rabbitmq.com/docs/ae  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta a diferença AE vs DLX: AE lida com mensagem que uma exchange não conseguiu rotear; DLX lida com mensagem que uma fila dead-lettered.  
Tópicos cobertos: Alternate Exchange, fallback para mensagens sem rota, configuração por policy ou argumento de exchange.  
Limites da fonte: só usada como fronteira herdada do node anterior.

ID: F8  
URL: https://www.rabbitmq.com/docs/quorum-queues  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta delivery-limit em quorum queues e a ressalva de RabbitMQ 4.3 sobre `delivery-count`, `acquired-count`, requeues e delayed retry.  
Tópicos cobertos: poison messages, delivery limit, `x-delivery-count`, `x-acquired-count`, repeatedly requeued deliveries, delayed retry.  
Limites da fonte: node atual não aprofunda quorum queues; usa delivery-limit como quarta causa de dead-lettering e deixa detalhes para node avançado.

ID: F9  
URL: https://www.rabbitmq.com/docs/reliability  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta a leitura conceitual de acknowledgements como transferência de responsabilidade, redelivery e idempotência de consumidores.  
Tópicos cobertos: responsabilidades de publisher, broker e consumer, acknowledgements, at-least-once, redelivery, idempotência.  
Limites da fonte: usada para orientar a narrativa de confiabilidade sem abrir publisher confirms em profundidade.

## Síntese por Fonte

- F1 permite afirmar que uma mensagem de uma fila pode ser dead-lettered quando é rejeitada ou nacked com `requeue=false`, quando expira por TTL, quando é removida por limite de fila ou quando excede delivery limit em quorum queue. A mesma fonte permite afirmar que DLX é exchange normal, configurada em uma fila, e que a mensagem dead-lettered é republicada para essa exchange.
- F2 permite afirmar que `basic.reject` e `basic.nack` são mecanismos de negative acknowledgement; com `requeue=true`, a entrega volta para a fila; com `requeue=false`, pode ser descartada ou dead-lettered se houver DLX.
- F3 permite afirmar que TTL pode existir por fila ou por mensagem, que o menor valor prevalece quando ambos aparecem, e que mensagens expiradas podem ser dead-lettered. A fonte também limita a leitura de TTL: mensagens expiradas podem só ser removidas ao chegar ao head da fila ou em eventos específicos.
- F4 permite afirmar que limite de comprimento ou bytes da fila pode provocar remoção ou dead-lettering, dependendo do comportamento de overflow configurado. O node não precisa ensinar overflow; basta registrar que limite de fila é uma causa legítima.
- F5 permite afirmar que policies existem para configurar propriedades de grupos de queues e exchanges que podem mudar em runtime; isso sustenta a recomendação de não cristalizar DLX e TTL em argumentos fixos quando policy for aplicável.
- F6 e F7 permitem afirmar a fronteira herdada: AE cuida de mensagem sem rota na exchange de entrada; DLX cuida de mensagem que saiu de uma fila depois de algum evento.
- F8 permite afirmar que delivery-limit é uma causa de dead-lettering em quorum queues e que RabbitMQ 4.3 alterou a contagem relevante para delivery limit. Essa fonte também mostra que retry com atraso em quorum queues existe, mas a página atual só registra a ideia de backoff como fronteira.
- F9 permite afirmar que acknowledgements carregam semântica de responsabilidade: a aplicação consumidora não deve ackar antes de assumir o processamento; redelivery é esperado em sistemas confiáveis e consumidores precisam lidar com duplicidade.

## Afirmações Técnicas Importantes

Afirmação: DLX não é um tipo especial de exchange; é uma exchange normal escolhida como destino de mensagens dead-lettered por uma fila.  
Base: F1; reforço conceitual por F6 e F7 para separar de AE.  
Condição ou limite: a exchange precisa existir quando a mensagem for dead-lettered; se o destino de DLX não puder aceitar a publicação, a segurança depende de detalhes avançados e do tipo de fila.  
Impacto didático: evita chamar DLX de fila morta e preserva o modelo já aprendido de exchange como roteador.

Afirmação: Dead-lettering acontece depois que a mensagem já entrou em uma fila, não quando a exchange inicial deixa de encontrar rota.  
Base: F1, F6, F7.  
Condição ou limite: uma mensagem dead-lettered será republicada para uma exchange; ainda assim a causa original está na fila.  
Impacto didático: estabelece a fronteira com o node anterior.

Afirmação: Rejeitar ou nackar uma entrega com `requeue=false` é uma causa de dead-lettering quando a fila tem DLX configurada.  
Base: F1, F2.  
Condição ou limite: sem DLX, a mensagem pode ser descartada; com `requeue=true`, ela volta para a fila em vez de seguir para DLX.  
Impacto didático: torna a decisão de consumer visível sem virar tutorial de código.

Afirmação: TTL vencido pode dead-letter uma mensagem; TTL por fila e TTL por mensagem podem coexistir, e o menor valor é escolhido.  
Base: F1, F3.  
Condição ou limite: TTL não deve ser tratado como scheduler preciso; mensagens expiradas podem ficar retidas até eventos de remoção, como chegar ao head da fila.  
Impacto didático: permite explicar retry com atraso sem prometer precisão temporal.

Afirmação: Queue length limit é uma causa de dead-lettering quando a fila excede limites configurados e o comportamento de overflow permite dead-letter.  
Base: F1, F4.  
Condição ou limite: o node não aprofunda `drop-head`, `reject-publish` ou `reject-publish-dlx`; eles ficam como detalhe operacional.  
Impacto didático: completa a lista de causas sem deslocar a narrativa para capacidade.

Afirmação: Delivery-limit em quorum queues pode dead-letter mensagens que ultrapassam o limite, mas os detalhes de contagem mudaram em RabbitMQ 4.3.  
Base: F1, F8.  
Condição ou limite: a documentação de quorum queues informa que, a partir de 4.3, o limite usa `delivery-count`, e certas requeues explícitas não contam para esse limite.  
Impacto didático: registra a causa sem transformar o node em aula avançada de quorum queues.

Afirmação: `requeue=true` repetido pode criar loop de redelivery sem progresso, enquanto retry planejado cria um caminho de espera, contagem e saída para análise.  
Base: F2, F8, F9; inferência declarada a partir de requeue, repeatedly requeued deliveries e confiabilidade de consumidores.  
Condição ou limite: a forma concreta de backoff varia por tipo de fila e configuração; este node fica no modelo conceitual.  
Impacto didático: separa "tentar de novo imediatamente" de "retry como política".

Afirmação: Um desenho comum de retry com atraso usa uma fila de espera com TTL e DLX de volta para a exchange principal.  
Base: F1, F3; inferência declarada a partir de TTL e dead-letter routing.  
Condição ou limite: não é tutorial de implementação; TTL não é relógio exato; o desenho precisa limite de tentativas e observabilidade.  
Impacto didático: dá forma mental para "retry queue" sem comandos.

Afirmação: Policies são preferíveis a x-arguments rígidos para DLX e TTL quando aplicável, porque podem ser alteradas em runtime e aplicadas a grupos de recursos.  
Base: F1, F5.  
Condição ou limite: o próximo node aprofunda precedência, permissões e governança; aqui entra apenas como recomendação de leitura.  
Impacto didático: evita que a pessoa associe DLX a código imutável de declaração.

Afirmação: Consumidores devem reconhecer mensagens apenas quando assumem responsabilidade pelo processamento; caso contrário, a decisão entre requeue, DLX e descarte precisa representar a consequência desejada.  
Base: F2, F9.  
Condição ou limite: idempotência e duplicidade aparecem como pano de fundo, não como seção principal do HTML.  
Impacto didático: conecta DLX à semântica de processamento, não só a topologia.

## Conceitos Essenciais

### Mensagem já dentro da fila

- Nome técnico: queued message.
- Explicação em linguagem simples: a exchange já encontrou um destino e a mensagem passou a pertencer a uma fila, aguardando entrega, reconhecimento ou outro evento.
- Por que é necessária: separa DLX de AE; DLX começa depois do roteamento inicial.
- Relação com conceitos anteriores: depende de fila, exchange, binding e entrega ao consumidor.
- Relação com conceitos futuros: prepara policies, permissões e diagnóstico de filas.
- Riscos de confusão: achar que DLX resolve publicação sem rota.
- Fonte base: F1, F6, F7.

### Dead Letter Exchange

- Nome técnico: Dead Letter Exchange.
- Explicação em linguagem simples: exchange normal para a qual uma fila republica mensagens que saíram dela por um motivo de dead-lettering.
- Por que é necessária: é o centro do node.
- Relação com conceitos anteriores: reutiliza exchange como roteador; não redefine tipos de exchange.
- Relação com conceitos futuros: sua configuração por policy, x-argument e permissões será governada no próximo node.
- Riscos de confusão: chamar DLX de fila; achar que DLX armazena.
- Fonte base: F1.

### Dead-lettering

- Nome técnico: dead-lettering.
- Explicação em linguagem simples: movimento em que uma mensagem sai de uma fila por uma condição definida e é republicada para a DLX.
- Por que é necessária: nomeia o evento que muda a mensagem de posição.
- Relação com conceitos anteriores: acontece depois da fila e do consumo.
- Relação com conceitos futuros: diagnóstico e garantias avançadas ficam para nodes posteriores.
- Riscos de confusão: tratar como falha genérica ou como descarte sempre definitivo.
- Fonte base: F1.

### Negative acknowledgement

- Nome técnico: negative acknowledgement.
- Explicação em linguagem simples: sinal do consumer ao broker de que a entrega não foi aceita como concluída.
- Por que é necessária: uma das causas de dead-lettering depende de rejeição ou nack com `requeue=false`.
- Relação com conceitos anteriores: consumer acknowledgement já é pré-requisito de fila e entrega.
- Relação com conceitos futuros: publisher confirms são outro mecanismo.
- Riscos de confusão: confundir nack de consumidor com nack de publisher confirm.
- Fonte base: F2, F9.

### `requeue=false` e `requeue=true`

- Nome técnico: `requeue` parameter.
- Explicação em linguagem simples: a escolha que diz se uma entrega rejeitada volta para a fila ou não.
- Por que é necessária: mostra a bifurcação entre loop imediato e saída para DLX.
- Relação com conceitos anteriores: fila e consumer.
- Relação com conceitos futuros: redelivery limits e delayed retry de quorum queues.
- Riscos de confusão: usar `requeue=true` como retry ilimitado.
- Fonte base: F2, F8.

### TTL

- Nome técnico: Time-to-Live.
- Explicação em linguagem simples: tempo máximo durante o qual uma mensagem pode permanecer na fila antes de expirar.
- Por que é necessária: permite explicar dead-lettering por expiração e retry com atraso.
- Relação com conceitos anteriores: fila como lugar de espera.
- Relação com conceitos futuros: configuração por policy e detalhes de queue TTL.
- Riscos de confusão: tratar TTL como timer exato ou scheduler.
- Fonte base: F3.

### Queue length limit

- Nome técnico: queue length limit.
- Explicação em linguagem simples: limite de quantidade ou bytes de mensagens prontas na fila.
- Por que é necessária: uma das causas de dead-lettering.
- Relação com conceitos anteriores: fila acumula mensagens.
- Relação com conceitos futuros: capacity planning e políticas operacionais não são foco.
- Riscos de confusão: achar que mensagens não reconhecidas contam igual para o limite de ready messages.
- Fonte base: F4.

### Delivery limit

- Nome técnico: delivery-limit.
- Explicação em linguagem simples: limite de tentativas em quorum queues depois do qual uma mensagem pode ser removida ou dead-lettered.
- Por que é necessária: completa a lista de causas do contrato.
- Relação com conceitos anteriores: redelivery e retry.
- Relação com conceitos futuros: node avançado de quorum queues e redelivery limits.
- Riscos de confusão: generalizar para todo tipo de fila ou ignorar mudança de RabbitMQ 4.3.
- Fonte base: F1, F8.

### Retry queue

- Nome técnico: retry queue.
- Explicação em linguagem simples: fila usada para segurar uma mensagem por algum tempo antes de uma nova tentativa.
- Por que é necessária: mostra DLX como base de retry com atraso.
- Relação com conceitos anteriores: fila e exchange.
- Relação com conceitos futuros: backoff, delayed retry nativo de quorum queues e políticas de tentativa ficam em níveis posteriores.
- Riscos de confusão: montar loop sem limite.
- Fonte base: F1, F3, F8.

### Quarantine queue

- Nome técnico: quarantine queue.
- Explicação em linguagem simples: fila de destino para mensagens que não devem voltar imediatamente ao fluxo principal e precisam de inspeção.
- Por que é necessária: mostra DLX como base de análise e isolamento.
- Relação com conceitos anteriores: fila como ponto de acúmulo.
- Relação com conceitos futuros: observabilidade e diagnóstico.
- Riscos de confusão: esconder mensagens indefinidamente sem dono operacional.
- Fonte base: F1, F9.

### Policy e x-arguments

- Nome técnico: policy, optional arguments, x-arguments.
- Explicação em linguagem simples: formas de aplicar parâmetros como DLX e TTL a filas; policy é alterável operacionalmente, argumento fixo nasce na declaração.
- Por que é necessária: o contrato exige registrar a preferência por policies quando aplicável.
- Relação com conceitos anteriores: configura a fila que dead-lettera.
- Relação com conceitos futuros: próximo node aprofunda governança, permissões e precedência.
- Riscos de confusão: antecipar todo o node seguinte.
- Fonte base: F1, F5.

## Relações Causais e Estruturais

- Relação: publicação roteada para uma fila -> mensagem passa a ser responsabilidade da fila até entrega, ack, rejeição, expiração ou limite.
  - Condição: a publicação encontrou ao menos um destino.
  - Base: F1, F2, F9.
- Relação: consumer rejeita ou nacks com `requeue=false` -> mensagem não volta para a fila principal -> DLX configurada recebe republicação.
  - Condição: fila tem DLX configurada; sem DLX, o destino pode ser descarte.
  - Base: F1, F2.
- Relação: consumer rejeita ou nacks com `requeue=true` -> mensagem volta para a fila -> pode ser entregue de novo.
  - Condição: posição da mensagem pode mudar; redelivery loops são possíveis se o motivo não se resolve.
  - Base: F2, F8.
- Relação: TTL vencido -> mensagem expira -> pode ser dead-lettered.
  - Condição: remoção de mensagens expiradas tem caveats; não é relógio exato.
  - Base: F1, F3.
- Relação: queue length limit excedido -> mensagem pode ser removida ou dead-lettered.
  - Condição: depende do overflow configurado; HTML só registra a causa geral.
  - Base: F1, F4.
- Relação: quorum queue com delivery-limit excedido -> mensagem pode ser removida ou dead-lettered.
  - Condição: RabbitMQ 4.3 usa `delivery-count`; detalhes são avançados.
  - Base: F1, F8.
- Relação: DLX -> exchange normal -> bindings da DLX decidem destino.
  - Condição: a DLX precisa existir e ter bindings adequados.
  - Base: F1.
- Relação: DLX para quarantine queue -> mensagem sai do fluxo principal para análise.
  - Condição: bom para erro definitivo, contrato inválido ou caso que exige inspeção.
  - Base: F1, F9; inferência declarada para estratégia conceitual.
- Relação: DLX para retry queue com TTL -> mensagem espera -> expira -> dead-lettera de volta para uma exchange de trabalho.
  - Condição: precisa limite de tentativas e observabilidade; TTL não é scheduler preciso.
  - Base: F1, F3, F8; inferência declarada.
- Relação: policy altera parâmetros de grupos de filas em runtime -> menor acoplamento que x-argument fixo.
  - Condição: quando a propriedade é controlável por policy.
  - Base: F1, F5.

## Exemplos Técnicos Possíveis

- Exemplo condutor escolhido: uma mensagem de pedido já entrou em `orders.work`, foi entregue a um consumer e falhou por causa transitória ou dado inválido.
  - Mudança de estado: na fila principal -> tentativa do consumer -> decisão de requeue ou saída -> DLX -> fila de quarentena ou fila de espera -> possível retorno ao fluxo principal.
  - Conceitos introduzidos: fila já recebida, negative acknowledgement, `requeue`, DLX, dead-lettering, quarantine queue, retry queue, TTL.
  - Risco de escopo: virar código de consumer ou tutorial de configuração.
  - Controle: usar nomes conceituais e snippets não executáveis, sem comandos.
- Exemplo de quarentena: mensagem com formato inválido sai da fila principal e segue para uma fila de análise.
  - Mudança de estado: processamento não pode concluir; mensagem não deve voltar imediatamente.
  - Conceitos: DLX, quarantine queue.
  - Risco: virar observabilidade avançada.
  - Controle: não abrir métricas, dashboards ou `x-death` no HTML.
- Exemplo de retry com espera: falha transitória em serviço externo usa fila de espera com TTL antes de voltar à exchange principal.
  - Mudança de estado: saída planejada, espera, reentrada.
  - Conceitos: retry queue, TTL, dead-lettering por expiração.
  - Risco: transformar TTL em scheduler preciso.
  - Controle: incluir ressalva de que TTL é mecanismo de expiração, não agenda exata.

## Obrigações de Concretização Didática

Conceito ou relação: diferença entre AE e DLX.  
Tipo de demanda: fronteira.  
Primitiva visual escolhida: componente HTML/CSS com dois painéis de estado.  
Justificativa da primitiva: a pessoa precisa ver que AE nasce na exchange de entrada e DLX nasce depois da fila; só prosa tende a misturar os nomes.  
Exemplo candidato: publicação sem rota no node anterior versus mensagem já em `orders.work` que sai da fila.  
Fonte: F1, F6, F7.  
Por que a prosa pode não bastar: os dois mecanismos terminam em exchanges e podem parecer equivalentes.  
Risco de virar laboratório ou excesso: baixo; manter como contraste visual curto.  
Como manter conceitual e mínimo: sem comandos e sem repetir a tabela do node anterior.  
Fronteira com nodes futuros: não abrir diagnóstico de AE/DLX.

Conceito ou relação: causas de dead-lettering.  
Tipo de demanda: ordem e lista de condições.  
Primitiva visual escolhida: componente HTML/CSS de fluxo com quatro gatilhos convergindo para DLX.  
Justificativa da primitiva: a lista de eventos é central e precisa mostrar que causas diferentes convergem no mesmo mecanismo de saída.  
Exemplo candidato: rejeição com `requeue=false`, TTL vencido, queue length limit, delivery-limit de quorum queue.  
Fonte: F1, F2, F3, F4, F8.  
Por que a prosa pode não bastar: sem visual, a DLX pode parecer uma causa, não o destino configurado.  
Risco de virar laboratório ou excesso: médio se incluir parâmetros demais.  
Como manter conceitual e mínimo: sem valores, sem comandos, sem keys completas além de termos já introduzidos.  
Fronteira com nodes futuros: delivery-limit fica como causa, não como mecânica avançada.

Conceito ou relação: `requeue=true` versus dead-lettering planejado.  
Tipo de demanda: contraste e risco.  
Primitiva visual escolhida: tabela curta depois de prosa preparatória.  
Justificativa da primitiva: o contraste é de consequência operacional e cabe melhor como matriz de leitura após o conceito.  
Exemplo candidato: falha transitória que volta imediatamente sem pausa versus fila de espera com TTL.  
Fonte: F2, F8, F9.  
Por que a prosa pode não bastar: a diferença entre "tentar de novo" e "planejar retry" é fácil de perder.  
Risco de virar laboratório ou excesso: médio se listar receita de backoff.  
Como manter conceitual e mínimo: não dar algoritmo de tentativa; falar de limite, espera e observabilidade.
Fronteira com nodes futuros: delayed retry e redelivery limits avançados ficam para quorum queues.

Conceito ou relação: recorte mínimo de configuração de DLX.  
Tipo de demanda: forma.  
Primitiva visual escolhida: snippet conceitual não executável com highlight semântico.  
Justificativa da primitiva: o leitor precisa ver que a configuração fica na fila e aponta para uma exchange, mas não precisa executar nada.  
Exemplo candidato: `fila_principal.dead_letter_exchange = pedidos.dlx`.  
Fonte: F1, F5.  
Por que a prosa pode não bastar: sem forma mínima, DLX pode ser imaginada como fila ou atributo da exchange principal.  
Risco de virar laboratório ou excesso: alto se usar comandos RabbitMQ.  
Como manter conceitual e mínimo: usar placeholders, sem `rabbitmqctl`, sem client library, sem sequência operacional.  
Fronteira com nodes futuros: mencionar que policies são preferíveis, mas não explicar precedência ou permissões.

Conceito ou relação: retry com atraso via fila de espera.  
Tipo de demanda: ordem temporal.  
Primitiva visual escolhida: componente HTML/CSS de etapas conectadas.  
Justificativa da primitiva: a pessoa precisa ver o retorno ao fluxo principal depois da espera.  
Exemplo candidato: fila principal -> DLX -> retry queue com TTL -> exchange principal.  
Fonte: F1, F3, F8.  
Por que a prosa pode não bastar: retry com DLX envolve duas passagens por exchanges e uma espera em fila.  
Risco de virar laboratório ou excesso: alto se detalhar múltiplas filas de backoff.  
Como manter conceitual e mínimo: uma única fila de espera, sem comandos, com ressalva sobre TTL.  
Fronteira com nodes futuros: delayed retry nativo e estratégia de backoff ficam fora.

## Riscos, Armadilhas e Erros Comuns

- Chamar DLX de fila morta.
  - Base: F1.
  - Correção conceitual: DLX é exchange; a fila de quarentena ou DLQ é destino roteado pela DLX.
- Usar `requeue=true` indefinidamente.
  - Base: F2, F8.
  - Correção conceitual: requeue imediato devolve ao mesmo circuito; retry planejado cria espera, limite e saída para análise.
- Achar que TTL é scheduler exato.
  - Base: F3.
  - Correção conceitual: TTL é expiração; remoção e dead-lettering têm caveats.
- Declarar DLX mas não garantir que a exchange exista ou tenha bindings.
  - Base: F1.
  - Correção conceitual: dead-lettering é republicação para uma exchange; roteamento ainda depende da topologia.
- Generalizar delivery-limit para todas as filas.
  - Base: F1, F8.
  - Correção conceitual: delivery-limit citado no contrato se refere a quorum queues.
- Usar x-arguments rígidos para algo que precisa mudar em produção.
  - Base: F1, F5.
  - Correção conceitual: policies são preferíveis quando aplicáveis; governança detalhada fica no próximo node.

## Limites e Fora de Escopo

- Este node explica:
  - O momento em que uma mensagem já em fila sai dela por dead-lettering.
  - DLX como exchange normal configurada na fila.
  - As causas principais: reject/nack com `requeue=false`, TTL, queue length limit e delivery-limit de quorum queue.
  - A diferença entre requeue imediato e retry planejado.
  - Quarentena e retry queue como destinos conceituais.
  - Preferência breve por policies sobre x-arguments rígidos quando aplicável.
- Este node apenas menciona como fronteira:
  - Delivery-limit em quorum queues.
  - Delayed retry de RabbitMQ 4.3 em quorum queues.
  - At-least-once dead-lettering e segurança em cluster.
  - `x-death` e headers de auditoria.
- Fica para outro node:
  - Policies, x-arguments, operator policies, permissões e precedência: `intermediario/05-policies-x-arguments-e-permissoes`.
  - Publisher confirms em profundidade: `intermediario/07-publisher-confirms-e-confiabilidade`.
  - Diagnóstico de AE/DLX com métricas: `avancado/01-diagnostico-de-roteamento-e-observabilidade`.
  - Quorum queues, redelivery limits, delayed retry e garantias avançadas: `avancado/03-quorum-queues-dlx-e-redelivery-limits`.
- Não pertence ao roadmap neste node:
  - Tutorial completo de código cliente.
  - Sequência de comandos RabbitMQ.
  - Projeto de retry com múltiplos backoffs e observabilidade completa.
  - Escolha de framework ou biblioteca de consumer.

## Divergências, Versões e Notas Temporais

- As páginas consultadas mostram a série RabbitMQ 4.3 como versão corrente em 2026-06-10.
- RabbitMQ 4.3 é relevante para quorum queues: a documentação informa que delivery-limit é baseado em `delivery-count` e introduz distinção com `x-acquired-count`; isso impede simplificar "todo nack aumenta delivery count".
- A documentação de TTL ressalta que a remoção de mensagens expiradas pode depender de posição na fila ou eventos, então o HTML não deve apresentar TTL como agenda exata.
- A documentação de DLX recomenda contra x-arguments rígidos para DLX quando policies podem resolver, porque argumentos fixos exigem mudança de aplicação e redeclaração/deleção da fila para alteração.
- O plugin histórico de delayed message exchange não é necessário para este node; para evitar desvio e fonte secundária, o HTML não depende dele.

## Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| DLX como exchange normal | F1 | Conceito central do node. |
| Eventos de dead-lettering | F1, F2, F3, F4, F8 | Quatro causas principais, com delivery-limit restrito a quorum queues. |
| `basic.reject`, `basic.nack`, `requeue` | F2, F9 | Usado para separar requeue imediato de saída para DLX. |
| TTL e retry com espera | F1, F3 | TTL sustenta espera, mas não deve virar scheduler exato. |
| Queue length limit | F1, F4 | Causa de dead-lettering sem detalhar overflow. |
| Delivery-limit | F1, F8 | Fronteira conceitual, sem aprofundar quorum queues. |
| Policies versus x-arguments | F1, F5 | Recomendação curta; próximo node aprofunda. |
| AE versus DLX | F1, F6, F7 | Fronteira com node anterior. |
| Confiabilidade e responsabilidade de consumer | F2, F9 | Contexto para ack/nack e idempotência. |

## Ordem de Introdução Conceitual para o HTML

1. Situação: a mensagem já entrou na fila principal.
2. Diferença com o node anterior: não é publicação sem rota nem AE.
3. Consumer não conclui e precisa decidir entre devolver à fila ou deixar a mensagem sair.
4. Negative acknowledgement e `requeue`.
5. `requeue=false` como caminho para dead-lettering.
6. DLX como exchange normal configurada na fila.
7. Outros gatilhos de dead-lettering: TTL, queue length limit, delivery-limit.
8. Quarantine queue e retry queue como destinos possíveis.
9. Retry com atraso e ressalva de TTL.
10. Policies versus x-arguments como recomendação curta.
11. Handoff para o próximo node.

## Insumos para o Ledger Editorial

- Termos permitidos no HTML com preparação: Dead Letter Exchange, DLX, dead-lettering, negative acknowledgement, `basic.nack`, `basic.reject`, `requeue=false`, `requeue=true`, TTL, queue length limit, delivery-limit, retry queue, quarantine queue, policies, x-arguments.
- Termos permitidos só no dump ou apenas como fronteira curta: `x-death`, at-least-once dead-lettering, delayed retry nativo de quorum queues, `x-delivery-count`, `x-acquired-count`, `reject-publish-dlx`, overflow detalhado.
- Termos reservados: operator policies, permissões de usuário para DLX, precedence de policy vs argumento, publisher confirms em profundidade, observabilidade operacional de DLQ.
- Títulos de fontes com termos carregados devem ser adaptados no rodapé do HTML para não introduzir conceitos não preparados.

## Candidatos de Narrativa para o HTML

- Narrativa dominante escolhida: processo com contraste de fronteira. A página acompanha uma mensagem que já chegou à fila, falha no consumo e tem sua saída decidida por requeue, DLX, TTL ou limite.
- Pergunta-motor: quando uma mensagem já está na fila e não deve simplesmente voltar para o mesmo ponto, que caminho técnico permite isolá-la, esperar ou tentar de novo sem confundir isso com falha de rota inicial?
- Situação de abertura: uma mensagem de pedido chegou à fila de trabalho, mas o consumer não consegue concluir; isso não é mais AE, porque a exchange já encontrou a rota.
- Transformação acompanhada: fila principal -> tentativa de consumo -> decisão de requeue ou dead-lettering -> DLX -> fila de quarentena ou fila de espera -> possível retorno ao fluxo principal.
- Exemplo condutor: `orders.work`, `orders.dlx`, fila de quarentena e fila de espera com TTL, sempre como nomes conceituais, não comandos.
- Momento de nomeação:
  - DLX só depois de mostrar a mensagem saindo da fila.
  - `requeue` só depois de mostrar a decisão do consumer.
  - TTL só depois de mostrar a necessidade de espera.
  - Policies só depois de apresentar DLX como configuração da fila.
- Risco de tom corretivo: alto, porque o node contém muitos "não confundir". O HTML deve construir o fluxo positivo antes de corrigir DLX vs fila morta ou requeue infinito.
