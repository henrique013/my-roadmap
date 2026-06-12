# Concept ledger

## Metadados

- Roadmap: rabbitmq-exchanges
- Level: basico
- Node: Filas, consumidores e entrega
- Node ID: basico/06-filas-consumidores-e-entrega
- Data: 2026-06-09
- Fonte principal: research-dump.md, fontes F1-F5

## Conceitos Permitidos no HTML

### Fila

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como conceito herdado dos nodes anteriores
- Primeira ocorrência permitida: contexto inicial e lead
- Explicação mínima exigida antes da primeira ocorrência: não exige definição longa; o node deve rapidamente estabilizar que é onde mensagens roteadas ficam acumuladas para entrega
- Aliases e paráfrases:
  - fila
  - queue
  - coleção ordenada
  - lugar de acúmulo
- Termos relacionados que também exigem preparo:
  - mensagem pronta
  - entrega
  - consumer
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - ponto de armazenamento e entrega depois do roteamento
  - unidade que possui seu próprio backlog
- Usos proibidos:
  - tratar fila como exchange
  - sugerir que fila decide rota da publicação
- Fronteira com nodes futuros: tipos de fila, durabilidade e quorum queues ficam fora
- Fonte base: F1, F4

### Mensagem pronta

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "mensagem esperando entrega"
- Primeira ocorrência permitida: depois que a fila foi situada como lugar de acúmulo
- Explicação mínima exigida antes da primeira ocorrência: mostrar uma mensagem enfileirada sem worker online
- Aliases e paráfrases:
  - mensagem pronta
  - pronta para entrega
  - ready message
  - esperando entrega
- Termos relacionados que também exigem preparo:
  - mensagem entregue sem reconhecimento
  - delivery
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - estado de mensagem que ainda aguarda consumer disponível
- Usos proibidos:
  - usar como métrica operacional detalhada
- Fronteira com nodes futuros: queue depth e observabilidade ficam fora
- Fonte base: F1, F2

### Delivery

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "entrega"
- Primeira ocorrência permitida: depois de mostrar a fila entregando a mensagem a um worker
- Explicação mínima exigida antes da primeira ocorrência: explicar que o broker envia uma mensagem da fila para um consumer registrado
- Aliases e paráfrases:
  - delivery
  - entrega
  - mensagem entregue
  - enviada ao consumer
- Termos relacionados que também exigem preparo:
  - acknowledgement
  - mensagem entregue sem reconhecimento
- Pode aparecer em:
  - título: não
  - lead: sim, como entrega
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - unidade de entrega da fila para o consumer
- Usos proibidos:
  - tratar delivery como confirmação de publicação
- Fronteira com nodes futuros: delivery tags, cancelamento e prefetch ficam fora
- Fonte base: F2, F3

### Consumer

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "worker" quando o exemplo já prepara o papel
- Primeira ocorrência permitida: depois que a fila existe na narrativa
- Explicação mínima exigida antes da primeira ocorrência: mostrar que é a aplicação ou worker registrado para receber mensagens da fila
- Aliases e paráfrases:
  - consumer
  - consumidor
  - worker
  - aplicação consumidora
- Termos relacionados que também exigem preparo:
  - subscription
  - acknowledgement
  - consumers competindo
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - aplicação registrada para receber deliveries de uma fila
- Usos proibidos:
  - dizer que consumer assina exchange diretamente
- Fronteira com nodes futuros: consumer capacity, prefetch e tuning ficam para o intermediário
- Fonte base: F2

### Subscription

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "registro na fila"
- Primeira ocorrência permitida: depois de apresentar consumer
- Explicação mínima exigida antes da primeira ocorrência: explicar que o consumer se registra em uma fila para receber entregas
- Aliases e paráfrases:
  - subscription
  - inscrição
  - registro do consumer
  - consumer registrado
- Termos relacionados que também exigem preparo:
  - delivery
  - consumer tag
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: não
- Usos permitidos:
  - registro do consumer em uma fila
- Usos proibidos:
  - assinatura em exchange
- Fronteira com nodes futuros: cancelamento, consumer tag e polling ficam fora
- Fonte base: F2

### Acknowledgement

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "reconhecimento" depois que a entrega pendente foi explicada
- Primeira ocorrência permitida: depois de distinguir mensagem entregue de mensagem removida
- Explicação mínima exigida antes da primeira ocorrência: mostrar que o broker precisa saber quando a delivery foi processada com sucesso
- Aliases e paráfrases:
  - acknowledgement
  - ack
  - reconhecimento
  - reconhecer a entrega
  - sinal do consumer
- Termos relacionados que também exigem preparo:
  - mensagem entregue sem reconhecimento
  - remoção segura
- Pode aparecer em:
  - título: não
  - lead: sim, como "ack" apenas se já houver contexto suficiente
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - confirmação do consumer de que uma delivery foi recebida e processada
  - fronteira entre entrega e remoção segura
- Usos proibidos:
  - tratar como sinal de sucesso do publisher
  - prometer exactly-once
- Fronteira com nodes futuros: negative ack, requeue, retry e publisher confirms ficam fora
- Fonte base: F3

### Consumers competindo

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "workers dividindo trabalho"
- Primeira ocorrência permitida: depois de explicar consumer e fila
- Explicação mínima exigida antes da primeira ocorrência: mostrar vários consumers registrados na mesma fila
- Aliases e paráfrases:
  - consumers competindo
  - competing consumers
  - workers dividindo trabalho
  - consumidores da mesma fila
  - distribuição de trabalho
- Termos relacionados que também exigem preparo:
  - cópia por fila
  - broadcast para filas
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - explicar escala de processamento em uma fila
- Usos proibidos:
  - sugerir que todos recebem a mesma mensagem
- Fronteira com nodes futuros: prefetch e consumer capacity ficam para o node intermediário
- Fonte base: F1, F2, F5

### Cópia por fila

- Tipo: relação estrutural
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "cada fila recebe sua própria cópia"
- Primeira ocorrência permitida: depois de lembrar que exchange roteia para destinos ligados
- Explicação mínima exigida antes da primeira ocorrência: mostrar múltiplas filas como destinos independentes
- Aliases e paráfrases:
  - cópia por fila
  - cópias independentes
  - cada fila recebe uma cópia
  - destino independente
- Termos relacionados que também exigem preparo:
  - broadcast
  - fanout
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - diferenciar fila independente de worker concorrente
- Usos proibidos:
  - reabrir tipos de exchange em detalhes
- Fronteira com nodes futuros: arquitetura de broadcast fica para o intermediário
- Fonte base: F4, inferência a partir de F1 e F2

### Broadcast para filas

- Tipo: relação estrutural
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, se o visual já mostrou múltiplas filas independentes
- Primeira ocorrência permitida: segunda metade do HTML
- Explicação mínima exigida antes da primeira ocorrência: mostrar que múltiplas filas são destinos separados
- Aliases e paráfrases:
  - broadcast
  - broadcast para filas
  - distribuir cópias para filas
- Termos relacionados que também exigem preparo:
  - fanout
  - cópia por fila
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - contraste com consumers competindo
- Usos proibidos:
  - tratar broadcast como sinônimo de mais workers
- Fronteira com nodes futuros: aprofundamento de topologia e prefetch fica em `intermediario/02`
- Fonte base: F4

## Conceitos Permitidos Só no Dump

### basic.get

- Motivo: aparece nas fontes como mecanismo de polling desencorajado.
- Por que não deve aparecer no HTML: desviaria para API operacional.
- Aliases bloqueados no HTML:
  - basic.get
  - pull API
  - polling
- Fonte base: F2

### Consumer tag

- Motivo: detalhe de identificação da subscription.
- Por que não deve aparecer no HTML: não é necessário para o modelo mental básico.
- Aliases bloqueados no HTML:
  - consumer tag
  - identificador de subscription
- Fonte base: F2

### Channel QoS

- Motivo: base de prefetch e limite de entregas pendentes.
- Por que não deve aparecer no HTML: anteciparia tuning e decisão intermediária.
- Aliases bloqueados no HTML:
  - channel QoS
  - QoS
- Fonte base: F1, F5

## Conceitos Reservados a Nodes Futuros

### Prefetch

- Node responsável: Broadcast vs consumidores competindo
- Node ID responsável: intermediario/02-broadcast-vs-consumidores-competindo
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - prefetch
  - prefetch count
  - limite de entregas pendentes
- Condição de exceção: nenhuma no HTML final

### Consumer capacity

- Node responsável: Broadcast vs consumidores competindo
- Node ID responsável: intermediario/02-broadcast-vs-consumidores-competindo
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - consumer capacity
  - capacidade do consumer
- Condição de exceção: nenhuma no HTML final

### Negative acknowledgement, requeue, redelivery e retry

- Node responsável: Dead-letter exchanges e retry conceitual; Quorum queues, DLX e limites de redelivery
- Node ID responsável, quando existir: intermediario/04-dead-letter-exchanges-e-retry-conceitual; avancado/03-quorum-queues-dlx-e-redelivery-limits
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - negative acknowledgement
  - nack
  - rejeição
  - requeue
  - redelivery
  - retry
  - redelivery loop
- Condição de exceção: nenhuma no HTML final

### Dead-letter exchange

- Node responsável: Dead-letter exchanges e retry conceitual
- Node ID responsável: intermediario/04-dead-letter-exchanges-e-retry-conceitual
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - dead-letter
  - DLX
  - dead-letter exchange
- Condição de exceção: nenhuma no HTML final

### Quorum queue

- Node responsável: Quorum queues, DLX e limites de redelivery
- Node ID responsável: avancado/03-quorum-queues-dlx-e-redelivery-limits
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - quorum queue
  - quorum queues
  - fila quorum
- Condição de exceção: nenhuma no HTML final

### Publisher confirm

- Node responsável: Publisher confirms e confiabilidade
- Node ID responsável: intermediario/07-publisher-confirms-e-confiabilidade
- Menção permitida no HTML atual: curta como fronteira sem usar o termo canônico
- Aliases bloqueados:
  - publisher confirm
  - publisher confirms
  - confirm do publisher
  - confirmação do publisher
- Condição de exceção: o HTML pode dizer apenas que "sinais do publisher" pertencem a outro ponto do fluxo

### Mandatory e alternate exchange

- Node responsável: Unroutable, mandatory e alternate exchange
- Node ID responsável: intermediario/03-unroutable-mandatory-e-alternate-exchange
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - mandatory
  - alternate exchange
  - AE
  - unroutable
- Condição de exceção: nenhuma no HTML final

### Exactly-once

- Node responsável: fora do escopo deste node; confiabilidade posterior trata limites realistas
- Node ID responsável, quando existir: intermediario/07-publisher-confirms-e-confiabilidade
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - exactly-once
  - exatamente uma vez
- Condição de exceção: nenhuma no HTML final

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| Queues | queue | sim | Documentação oficial de filas |
| Consumers | consumers | sim | Documentação oficial de consumers |
| Consumer Acknowledgements and Publisher Confirms | publisher confirms | sim, adaptado | Guia oficial de acknowledgements |
| Exchanges | exchange, fanout | sim | Documentação oficial de exchanges |
| AMQP 0-9-1 Model Explained | AMQP 0-9-1 | sim | Guia oficial do modelo AMQP 0-9-1 |
