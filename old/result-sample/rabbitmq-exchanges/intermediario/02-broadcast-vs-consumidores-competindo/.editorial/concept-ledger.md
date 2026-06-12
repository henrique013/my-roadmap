# Concept ledger

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Level: intermediario
- Node: Broadcast vs consumidores competindo
- Node ID: intermediario/02-broadcast-vs-consumidores-competindo
- Data: 2026-06-10
- Fonte principal: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/research-dump.md`

## Conceitos Permitidos no HTML

### Cópia por fila

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "cada fila guarda sua própria entrega"
- Primeira ocorrência permitida: depois da situação de e-mail, auditoria e analytics
- Explicação mínima exigida antes da primeira ocorrência: mostrar que uma publicação precisa ser processada por papéis independentes
- Aliases e paráfrases:
  - cópia por fila
  - cópia em cada fila
  - cópias independentes
  - uma entrega para cada fila
  - cada fila recebe sua própria cópia
- Termos relacionados que também exigem preparo:
  - broadcast
  - multicast
- Pode aparecer em:
  - título: sim
  - lead: sim, depois de preparação breve
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar múltiplas filas para papéis diferentes
  - contrastar com consumers equivalentes na mesma fila
- Usos proibidos:
  - sugerir cópia por consumer dentro da mesma fila
- Fronteira com nodes futuros: não usar para explicar Alternate Exchange, DLX ou confirms
- Fonte base: F1, F3, F4

### Broadcast

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar cópia por fila
- Explicação mínima exigida antes da primeira ocorrência: mostrar que mais de um serviço precisa processar o mesmo evento
- Aliases e paráfrases:
  - broadcast
  - distribuir para todos os interessados
  - todos os serviços recebem o evento
  - publicação para vários destinos
- Termos relacionados que também exigem preparo:
  - fanout
  - direct
  - topic
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - nomear a decisão de múltiplas filas
  - explicar que fanout é uma forma de roteamento para destinos ligados
- Usos proibidos:
  - usar broadcast como sinônimo de balanceamento
- Fronteira com nodes futuros: hash e exchanges especializadas ficam para node avançado
- Fonte base: F1, F3

### Consumidores competindo

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "workers equivalentes dividem entregas"
- Primeira ocorrência permitida: depois de explicar uma fila compartilhada por workers do mesmo papel
- Explicação mínima exigida antes da primeira ocorrência: mostrar que os workers fazem o mesmo trabalho lógico
- Aliases e paráfrases:
  - consumidores competindo
  - competing consumers
  - workers competindo
  - dividir trabalho na mesma fila
  - vários consumers na mesma fila
- Termos relacionados que também exigem preparo:
  - grupo de consumidores
  - prefetch
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar escala horizontal de instâncias equivalentes
  - contrastar com cópia por fila
- Usos proibidos:
  - afirmar que todos os consumers recebem a mesma mensagem
- Fronteira com nodes futuros: não discutir single active consumer nem ordenação profunda
- Fonte base: F2, F5, F7

### Grupo de consumidores

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "instâncias do mesmo serviço"
- Primeira ocorrência permitida: depois de explicar a fila compartilhada por workers equivalentes
- Explicação mínima exigida antes da primeira ocorrência: diferenciar serviço diferente de instância equivalente
- Aliases e paráfrases:
  - grupo de consumidores
  - grupo equivalente
  - instâncias equivalentes
  - workers do mesmo papel
  - consumers equivalentes
- Termos relacionados que também exigem preparo:
  - consumidores competindo
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - explicar por que várias instâncias podem compartilhar uma fila
- Usos proibidos:
  - tratar serviços diferentes como o mesmo grupo
- Fronteira com nodes futuros: governança de nomes e permissões fica em node posterior
- Fonte base: F2, F5

### Prefetch

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de preparar "entregas em andamento ainda não confirmadas"
- Explicação mínima exigida antes da primeira ocorrência: explicar que um consumer pode ter mensagens recebidas e ainda não confirmadas
- Aliases e paráfrases:
  - prefetch
  - `prefetch`
  - `prefetch_count`
  - janela de entregas
  - limite de entregas não confirmadas
- Termos relacionados que também exigem preparo:
  - entregas não confirmadas
  - acknowledgement
- Pode aparecer em:
  - título: sim, apenas depois de seção anterior preparar o mecanismo
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar distribuição observada entre consumers da mesma fila
- Usos proibidos:
  - recomendar valores
  - virar tutorial de `basic.qos`
  - definir topologia ou criar cópias
- Fronteira com nodes futuros: tuning, throughput e redelivery loops ficam fora
- Fonte base: F2, F6, F7

### Consumer capacity

- Tipo: métrica
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que a fila pode ou não entregar imediatamente para seus consumers
- Explicação mínima exigida antes da primeira ocorrência: mostrar que capacidade é sinal de entrega da fila, não regra de roteamento
- Aliases e paráfrases:
  - consumer capacity
  - capacidade de consumer
  - capacidade de consumo
  - capacidade da fila entregar
- Termos relacionados que também exigem preparo:
  - fila
  - consumers
  - prefetch
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar sinal operacional de capacidade de entrega
- Usos proibidos:
  - tratar como prova única de topologia correta
- Fronteira com nodes futuros: diagnóstico detalhado fica para node avançado
- Fonte base: F5

### Fanout

- Tipo: tipo de exchange
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como pré-requisito herdado
- Primeira ocorrência permitida: depois de explicar broadcast por filas
- Explicação mínima exigida antes da primeira ocorrência: lembrar que o tipo roteia para destinos ligados, sem reensinar tipos
- Aliases e paráfrases:
  - fanout
  - fanout exchange
- Termos relacionados que também exigem preparo:
  - broadcast
  - cópia por fila
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - mostrar que fanout copia para filas ligadas
- Usos proibidos:
  - reexplicar tipos clássicos em profundidade
  - chamar fanout de load balancing
- Fronteira com nodes futuros: tipos especializados ficam para node avançado
- Fonte base: F1, F3

### Direct e topic

- Tipo: tipo de exchange
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como pré-requisito herdado
- Primeira ocorrência permitida: depois de estabelecer que broadcast arquitetural depende de múltiplas filas compatíveis
- Explicação mínima exigida antes da primeira ocorrência: dizer que bindings compatíveis podem apontar para mais de uma fila
- Aliases e paráfrases:
  - direct
  - topic
  - direct exchange
  - topic exchange
  - multicast por direct/topic
- Termos relacionados que também exigem preparo:
  - binding
  - routing key
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: não
  - referências: sim
  - comentário final: não
- Usos permitidos:
  - nota curta para evitar reduzir broadcast a fanout
- Usos proibidos:
  - reensinar matching de direct/topic
- Fronteira com nodes futuros: diagnostics e tipos especializados não entram
- Fonte base: F1

## Conceitos Permitidos Só no Dump

### AMQP 0-9-1

- Motivo: versão e protocolo sustentam as fontes.
- Por que não deve aparecer no HTML: o node pode ensinar a decisão sem abrir camada de protocolo.
- Aliases bloqueados no HTML:
  - AMQP 0-9-1
  - protocolo AMQP
- Fonte base: F1, F6, F7

### `basic.qos`

- Motivo: fonte técnica de `prefetch`.
- Por que não deve aparecer no HTML: citar o método puxaria o texto para guia operacional.
- Aliases bloqueados no HTML:
  - basic.qos
  - Channel#basic_qos
  - `basic.qos`
- Fonte base: F2, F6, F7

### `basic.ack`

- Motivo: detalhe de acknowledgement.
- Por que não deve aparecer no HTML: a página só precisa de "confirmar entrega/processamento" como linguagem comum.
- Aliases bloqueados no HTML:
  - basic.ack
  - `basic.ack`
- Fonte base: F7

## Conceitos Reservados a Nodes Futuros

### Falha de rota inicial

- Node responsável: Unroutable, mandatory e Alternate Exchange
- Node ID responsável, quando existir: intermediario/03-unroutable-mandatory-e-alternate-exchange
- Menção permitida no HTML atual: handoff final curto sem termo técnico em inglês
- Aliases bloqueados:
  - publicação órfã
  - publicação sem destino
- Condição de exceção: somente no texto do link de próximo node em `.node-context`, se vindo do contrato

### Tratamento alternativo de rota

- Node responsável: Unroutable, mandatory e Alternate Exchange
- Node ID responsável, quando existir: intermediario/03-unroutable-mandatory-e-alternate-exchange
- Menção permitida no HTML atual: nenhuma fora do label do próximo node
- Aliases bloqueados:
  - retorno ao publisher
  - exchange alternativa
  - fallback de rota
- Condição de exceção: label do próximo node pode aparecer em `.node-context`

### Dead Letter Exchange

- Node responsável: Dead Letter Exchanges e retry conceitual
- Node ID responsável, quando existir: intermediario/04-dead-letter-exchanges-e-retry-conceitual
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - Dead Letter Exchange
  - DLX
  - dead-letter
  - retry
- Condição de exceção: nenhuma

### Policies, x-arguments e permissões

- Node responsável: Policies, x-arguments e permissões
- Node ID responsável, quando existir: intermediario/05-policies-x-arguments-e-permissoes
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - policies
  - policy
  - x-arguments
  - permissões
  - permissions
- Condição de exceção: nenhuma

### Publisher confirms

- Node responsável: Publisher confirms e confiabilidade
- Node ID responsável, quando existir: intermediario/07-publisher-confirms-e-confiabilidade
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - publisher confirms
  - confirm mode
  - confirms
- Condição de exceção: nenhuma

### Single active consumer

- Node responsável: fora do escopo deste roadmap intermediário atual
- Node ID responsável, quando existir:
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - single active consumer
  - consumidor ativo único
  - ordenação estrita
- Condição de exceção: nenhuma

### Hash exchange

- Node responsável: Tipos especializados e plugins
- Node ID responsável, quando existir: avancado/02-tipos-especializados-e-plugins
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - hash exchange
  - x-modulus-hash
  - consistent hashing
  - particionamento por hash
- Condição de exceção: nenhuma

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Exchanges, fanout, direct, topic | sim | Documentação oficial de exchanges |
| F2 | Work Queues | sim | Tutorial oficial de filas de trabalho |
| F3 | Publish/Subscribe | sim | Tutorial oficial de publicação para vários interessados |
| F4 | Queues | sim | Documentação oficial de filas |
| F5 | Consumers, Consumer Capacity | sim | Documentação oficial de consumidores e capacidade |
| F6 | Consumer Prefetch | sim, após preparar `prefetch` | Documentação oficial de prefetch |
| F7 | Consumer Acknowledgements and Publisher Confirms | parcialmente | Guia oficial de acknowledgements e prefetch |
