# Concept ledger

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Level: `basico`
- Node: `01-modelo-amqp-e-papel-da-exchange`
- Node ID: `basico/01-modelo-amqp-e-papel-da-exchange`
- Data: 2026-06-08
- Fonte principal: `research-dump.md`

## Conceitos Permitidos no HTML

### Mensagem

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum
- Primeira ocorrência permitida: abertura, ao falar da necessidade de enviar um evento ou fato.
- Explicação mínima exigida antes da primeira ocorrência: contexto de comunicação assíncrona entre aplicações.
- Aliases e paráfrases:
  - mensagem
  - mensagens
  - evento
  - fato publicado
  - conteúdo publicado
- Termos relacionados que também exigem preparo:
  - cópia da mensagem
  - publicação
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Objeto que atravessa publisher, exchange, fila e consumer.
  - Unidade que pode gerar cópias em filas diferentes.
- Usos proibidos:
  - Descrever propriedades, headers, persistência ou formato de payload.
- Fronteira com nodes futuros: propriedades e headers ficam para nodes posteriores.
- Fonte base: F2

### Publisher / Producer

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "aplicação que publica".
- Primeira ocorrência permitida: depois de mostrar que uma aplicação precisa enviar uma mensagem ao broker.
- Explicação mínima exigida antes da primeira ocorrência: é a aplicação que inicia a publicação.
- Aliases e paráfrases:
  - publisher
  - producer
  - produtor
  - aplicação produtora
  - aplicação publicadora
  - quem publica
- Termos relacionados que também exigem preparo:
  - publicação
  - broker
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Origem da mensagem no fluxo.
  - Contraste com consumer.
- Usos proibidos:
  - Publisher confirms, garantia de publicação ou tratamento de retorno.
- Fronteira com nodes futuros: confiabilidade do publisher fica no intermediário.
- Fonte base: F2, F3

### Broker

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como RabbitMQ em linguagem comum.
- Primeira ocorrência permitida: depois de mostrar que há um serviço intermediário entre aplicações.
- Explicação mínima exigida antes da primeira ocorrência: serviço que hospeda as peças da topologia e recebe publicações.
- Aliases e paráfrases:
  - broker
  - broker RabbitMQ
  - RabbitMQ
  - serviço intermediário
  - servidor RabbitMQ
- Termos relacionados que também exigem preparo:
  - exchange
  - fila
  - binding
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Local lógico onde exchange, fila e binding existem.
- Usos proibidos:
  - Vhost, cluster, permissões, gestão operacional.
- Fronteira com nodes futuros: governança e permissões ficam para intermediário/avançado.
- Fonte base: F2

### Exchange

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, apenas depois de a necessidade de roteamento estar clara.
- Primeira ocorrência permitida: lead ou primeira seção, após explicar que o produtor não deve escolher consumidores diretamente.
- Explicação mínima exigida antes da primeira ocorrência: ponto de publicação que decide para quais filas a mensagem pode seguir.
- Aliases e paráfrases:
  - exchange
  - exchanges
  - entidade de roteamento
  - ponto de publicação
  - ponto de roteamento
  - roteador
  - roteador do broker
- Termos relacionados que também exigem preparo:
  - roteamento
  - binding
  - fila
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Entidade onde publishers publicam.
  - Mecanismo que roteia para filas conforme regras.
  - Fronteira conceitual contra armazenamento.
- Usos proibidos:
  - Tratar como fila.
  - Tratar como local de assinatura de consumidores.
  - Explicar tipos específicos.
- Fronteira com nodes futuros: default exchange no node 02; direct/fanout/topic no node 04; headers no node 05.
- Fonte base: F1, F2, F3

### Roteamento

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "decidir o caminho".
- Primeira ocorrência permitida: junto da primeira explicação de exchange.
- Explicação mínima exigida antes da primeira ocorrência: a mensagem entra em uma peça que decide quais filas podem recebê-la.
- Aliases e paráfrases:
  - roteamento
  - rotear
  - direcionar
  - encaminhar conforme regras
  - decidir o caminho
  - escolher destinos
- Termos relacionados que também exigem preparo:
  - exchange
  - binding
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Resultado principal da exchange.
  - Contraste com armazenamento.
- Usos proibidos:
  - Explicar chave da publicação ou algoritmos por tipo de exchange.
- Fronteira com nodes futuros: vocabulário de chaves fica no node 03.
- Fonte base: F1, F2

### Binding

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "ligação configurada".
- Primeira ocorrência permitida: depois de exchange e fila terem sido apresentadas.
- Explicação mínima exigida antes da primeira ocorrência: ligação que cria uma regra entre exchange e fila.
- Aliases e paráfrases:
  - binding
  - bindings
  - ligação
  - ligações
  - ligação configurada
  - regra de ligação
  - regra de roteamento
  - regra existente
- Termos relacionados que também exigem preparo:
  - exchange
  - fila
  - roteamento
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Relação entre exchange e fila.
  - Regra mínima para explicar zero, uma ou várias filas.
- Usos proibidos:
  - Diferenciar key enviada pela publicação e key configurada no binding.
  - Entrar em argumentos, source/destination ou E2E.
- Fronteira com nodes futuros: node 03 aprofunda binding e chaves.
- Fonte base: F1, F2, F3

### Queue / Fila

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "lugar que guarda mensagens" depois de roteamento.
- Primeira ocorrência permitida: depois de exchange ou na área de contexto, porque o node precisa contrastar papéis.
- Explicação mínima exigida antes da primeira ocorrência: estrutura que recebe mensagens roteadas e as mantém para entrega.
- Aliases e paráfrases:
  - queue
  - queues
  - fila
  - filas
  - fila de mensagens
  - destino de armazenamento
  - estrutura de armazenamento
- Termos relacionados que também exigem preparo:
  - armazenamento
  - consumer
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Armazenamento e ponto de entrega para consumers.
  - Destino alcançado pela exchange.
- Usos proibidos:
  - Detalhar ordering avançado, concorrência, ack, prefetch ou tipos de fila.
- Fronteira com nodes futuros: node 06 aprofunda fila, consumer e entrega.
- Fonte base: F3, F4

### Armazenamento

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "guardar".
- Primeira ocorrência permitida: quando a mensagem chega à fila.
- Explicação mínima exigida antes da primeira ocorrência: a mensagem precisa ficar em uma estrutura até poder ser entregue.
- Aliases e paráfrases:
  - armazenamento
  - armazenar
  - guardar
  - segurar
  - manter até entrega
  - ficar esperando na fila
- Termos relacionados que também exigem preparo:
  - fila
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
  - Contraste com roteamento.
  - Responsabilidade da fila.
- Usos proibidos:
  - Associar armazenamento à exchange.
- Fronteira com nodes futuros: durabilidade e persistência ficam fora.
- Fonte base: F3, F4

### Consumer / Consumidor

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "aplicação que recebe da fila".
- Primeira ocorrência permitida: depois de fila.
- Explicação mínima exigida antes da primeira ocorrência: aplicação ou assinatura que recebe mensagens a partir de uma fila.
- Aliases e paráfrases:
  - consumer
  - consumers
  - consumidor
  - consumidores
  - aplicação consumidora
  - quem processa
  - quem recebe da fila
- Termos relacionados que também exigem preparo:
  - fila
  - entrega
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Fim do fluxo a partir de uma fila.
  - Contraste com publisher.
- Usos proibidos:
  - Explicar acknowledgements, polling, single active consumer ou concorrência.
- Fronteira com nodes futuros: node 06 aprofunda entrega e consumidores.
- Fonte base: F2, F3, F5

### Cópia da mensagem

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, depois de múltiplas filas serem apresentadas.
- Primeira ocorrência permitida: seção que mostra uma publicação alcançando duas filas.
- Explicação mínima exigida antes da primeira ocorrência: quando mais de uma fila é alcançada, cada fila recebe sua própria instância para consumo independente.
- Aliases e paráfrases:
  - cópia
  - cópias
  - cópias independentes
  - cópia da mensagem
  - message copy
  - uma instância em cada fila
- Termos relacionados que também exigem preparo:
  - mensagem
  - fila
  - binding
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Explicar que uma publicação pode alimentar mais de uma fila.
- Usos proibidos:
  - Chamar isso de fanout ou broadcast.
  - Comparar com vários consumidores na mesma fila.
- Fronteira com nodes futuros: fanout e competing consumers ficam depois.
- Fonte base: F2

### AMQP 0-9-1

- Tipo: sigla
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, porque é o contrato do roadmap e do título.
- Primeira ocorrência permitida: contexto, título ou lead.
- Explicação mínima exigida antes da primeira ocorrência: protocolo usado pelo recorte do roadmap.
- Aliases e paráfrases:
  - AMQP 0-9-1
  - modelo AMQP
  - protocolo AMQP 0-9-1
- Termos relacionados que também exigem preparo:
  - broker
  - exchange
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Delimitar o modelo conceitual.
- Usos proibidos:
  - Comparar com AMQP 1.0, MQTT ou STOMP.
- Fronteira com nodes futuros: protocolos alternativos ficam fora do roadmap.
- Fonte base: F2, F3

### Exchange padrão

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, somente como label de vizinho ou handoff.
- Primeira ocorrência permitida: contexto de posição do próximo node ou fechamento curto.
- Explicação mínima exigida antes da primeira ocorrência: nenhuma explicação neste node; é apenas orientação de sequência.
- Aliases e paráfrases:
  - Exchange padrão
  - exchange padrão
- Termos relacionados que também exigem preparo:
  - publicação direta aparente
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim, apenas no handoff
  - tabela: não
  - visual/aria-label: não
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - Texto do contexto `Próximo`.
  - Handoff final para o próximo node.
- Usos proibidos:
  - Explicar nome vazio, `amq.default`, binding automático ou publicação direta aparente.
- Fronteira com nodes futuros: node 02 é responsável.
- Fonte base: contrato do roadmap

## Conceitos Permitidos Só no Dump

### routing key

- Motivo: pertence à explicação detalhada de bindings e destinos.
- Por que não deve aparecer no HTML: vazaria vocabulário do node 03 antes da base estar estabilizada.
- Aliases bloqueados no HTML:
  - routing key
  - chave de roteamento
  - chave da publicação
  - routing-key
- Fonte base: contrato do roadmap

### binding key

- Motivo: pertence ao node 03.
- Por que não deve aparecer no HTML: exigiria explicar a diferença entre key publicada e key configurada.
- Aliases bloqueados no HTML:
  - binding key
  - chave do binding
  - chave de binding
- Fonte base: contrato do roadmap

### mandatory

- Motivo: pertence a mensagens sem rota e tratamento pelo publisher.
- Por que não deve aparecer no HTML: levaria ao intermediário.
- Aliases bloqueados no HTML:
  - mandatory
  - mandatory flag
  - flag mandatory
- Fonte base: contrato do roadmap

### acknowledgement

- Motivo: pertence a entrega e remoção segura da fila em node posterior.
- Por que não deve aparecer no HTML: este node só separa papéis, sem detalhar confirmação de consumidor.
- Aliases bloqueados no HTML:
  - acknowledgement
  - acknowledgements
  - confirmação do consumidor
  - confirmação de consumidor
- Fonte base: contrato do roadmap

### publisher confirms

- Motivo: pertence à confiabilidade de publicação no intermediário.
- Por que não deve aparecer no HTML: desviaria o foco de modelo mental para garantia operacional.
- Aliases bloqueados no HTML:
  - publisher confirms
  - confirm do publisher
  - confirms
  - confirmação de publicação
- Fonte base: contrato do roadmap

## Conceitos Reservados a Nodes Futuros

### default exchange

- Node responsável: Exchange padrão e publicação direta aparente
- Node ID responsável, quando existir: `basico/02-exchange-padrao-e-publicacao-direta-aparente`
- Menção permitida no HTML atual: curta como fronteira, preferencialmente só como label de próximo node.
- Aliases bloqueados:
  - default exchange
  - amq.default
  - exchange vazia
  - nome vazio
  - empty string exchange
- Condição de exceção: o texto "Exchange padrão e publicação direta aparente" pode aparecer no contexto de posição porque é o label do próximo node.

### direct, fanout, topic

- Node responsável: Direct, fanout e topic
- Node ID responsável, quando existir: `basico/04-direct-fanout-e-topic`
- Menção permitida no HTML atual: nenhuma.
- Aliases bloqueados:
  - direct
  - fanout
  - topic
  - broadcast
  - multicast
  - wildcard
  - curinga
- Condição de exceção: nenhuma.

### headers exchange

- Node responsável: Headers exchange e metadados de roteamento
- Node ID responsável, quando existir: `basico/05-headers-e-metadados-de-roteamento`
- Menção permitida no HTML atual: nenhuma.
- Aliases bloqueados:
  - headers exchange
  - headers
  - x-match
  - metadados de roteamento
- Condição de exceção: títulos de fontes não devem puxar esse termo.

### dead-letter e alternate exchange

- Node responsável: Dead-letter exchanges e retry conceitual; Unroutable, mandatory e alternate exchange
- Node ID responsável, quando existir: `intermediario/03-unroutable-mandatory-e-alternate-exchange`, `intermediario/04-dead-letter-exchanges-e-retry-conceitual`
- Menção permitida no HTML atual: nenhuma.
- Aliases bloqueados:
  - DLX
  - dead-letter
  - dead letter
  - dead-letter exchange
  - alternate exchange
  - AE
  - unroutable
  - sem rota
- Condição de exceção: nenhuma; usar "sem fila alcançada" se precisar explicar zero destino sem nomear o mecanismo.

### competing consumers

- Node responsável: Filas, consumidores e entrega
- Node ID responsável, quando existir: `basico/06-filas-consumidores-e-entrega`
- Menção permitida no HTML atual: nenhuma.
- Aliases bloqueados:
  - competing consumers
  - consumidores competindo
  - concorrência entre consumidores
  - distribuição de carga
  - vários consumidores na mesma fila
- Condição de exceção: nenhuma.

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Exchanges | Sim | `RabbitMQ - Exchanges` |
| F2 | AMQP 0-9-1 Model | Sim | `RabbitMQ - AMQP 0-9-1 Model Explained` |
| F3 | Advanced Message Queuing Protocol Specification | Sim | `AMQP 0-9-1 specification` |
| F4 | Queues | Sim | `RabbitMQ - Queues` |
| F5 | Consumers | Sim | `RabbitMQ - Consumers` |
