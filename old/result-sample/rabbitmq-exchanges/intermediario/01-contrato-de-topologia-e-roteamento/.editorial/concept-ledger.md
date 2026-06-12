# Concept ledger

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Level: intermediario
- Node: Contrato de topologia e roteamento
- Node ID: intermediario/01-contrato-de-topologia-e-roteamento
- Data: 2026-06-09
- Fonte principal: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/01-contrato-de-topologia-e-roteamento/research-dump.md`

## Conceitos Permitidos no HTML

### Contrato de publicação

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois da situação `orders-api` publicando em uma exchange com routing key sem conhecer fila final.
- Explicação mínima exigida antes da primeira ocorrência: exchange alvo e routing key formam a parte estável que o producer respeita.
- Aliases e paráfrases:
  - acordo de publicação
  - parte pública da topologia
  - contrato entre producer e topologia
  - contrato público de publicação
- Termos relacionados que também exigem preparo:
  - contrato de roteamento
  - topologia pública
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - separar exchange/routing key de fila consumidora.
  - explicar evolução por binding sem mudar publisher.
  - avaliar estabilidade de nomes e keys.
- Usos proibidos:
  - tratar como schema completo de payload.
  - tratar como garantia de entrega.
  - entrar em permissions, policies ou confirms.
- Fronteira com nodes futuros: confiabilidade de publicação fica em `intermediario/07`; policies e permissions ficam em `intermediario/05`.
- Fonte base: F1, F2, F3.

### Convenção de routing key

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como `orders.created` explicado no exemplo.
- Primeira ocorrência permitida: depois que `orders.created` for apresentado como intenção de publicação.
- Explicação mínima exigida antes da primeira ocorrência: a string carrega significado de roteamento para o domínio, não o nome de uma fila.
- Aliases e paráfrases:
  - padrão de routing key
  - formato de routing key
  - vocabulário de routing
  - key de domínio
- Termos relacionados que também exigem preparo:
  - routing key pública
  - binding key
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - comparar `orders.created` com nome de fila.
  - explicar compatibilidade de publicação.
  - sustentar matriz de decisão.
- Usos proibidos:
  - reexplicar topic wildcards em profundidade.
  - abrir migração de routing keys com mecanismos de fallback.
- Fronteira com nodes futuros: falha de rota fica em `intermediario/03`.
- Fonte base: F1, F4, F5.

### Ownership de exchange

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de mostrar que a exchange compartilhada é ponto estável entre vários publishers e bindings.
- Explicação mínima exigida antes da primeira ocorrência: responsabilidade por nome, significado e evolução da exchange.
- Aliases e paráfrases:
  - dono da exchange
  - responsabilidade pela exchange
  - ownership do contrato
  - responsabilidade pelo contrato
- Termos relacionados que também exigem preparo:
  - evolução do contrato
  - compatibilidade
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - comparar recortes por domínio, evento, severidade e tenant.
  - explicar quem protege semântica e compatibilidade.
- Usos proibidos:
  - discutir permissões de RabbitMQ.
  - transformar em governança avançada.
- Fronteira com nodes futuros: governança ampla fica em `avancado/05`.
- Fonte base: F6 e inferência a partir de F1/F3.

### Fronteira publisher-topology-consumer

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum de separação entre producer, exchange, bindings e filas.
- Primeira ocorrência permitida: depois do visual principal.
- Explicação mínima exigida antes da primeira ocorrência: publisher conhece exchange/routing key; topologia conhece bindings; consumer conhece fila.
- Aliases e paráfrases:
  - fronteira entre publisher e consumer
  - separação publisher, topologia e consumer
  - quem conhece quem
- Termos relacionados que também exigem preparo:
  - topologia
  - binding
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - organizar a explicação visual.
  - mostrar o que muda ao adicionar consumidor.
- Usos proibidos:
  - virar diagnóstico operacional.
- Fronteira com nodes futuros: diagnóstico fica em `avancado/01`.
- Fonte base: F1, F2, F5.

### Fila de grupo consumidor

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como fila de um serviço específico no exemplo.
- Primeira ocorrência permitida: depois de mostrar filas atrás dos bindings.
- Explicação mínima exigida antes da primeira ocorrência: fila usada por um serviço ou grupo de consumidores como detalhe de consumo.
- Aliases e paráfrases:
  - fila do serviço
  - fila interna de consumo
  - fila de destino do serviço
  - fila consumidora
- Termos relacionados que também exigem preparo:
  - consumer group
  - serviço consumidor
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - separar nomes internos de filas do contrato público.
  - preparar o handoff para o próximo node.
- Usos proibidos:
  - decidir modelo de consumidores concorrentes.
- Fronteira com nodes futuros: `intermediario/02` decide cópia por fila versus competição dentro da mesma fila.
- Fonte base: F5.

### Definitions como forma de topologia

- Tipo: fonte
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que exchanges, filas e bindings são peças explícitas da topologia.
- Explicação mínima exigida antes da primeira ocorrência: RabbitMQ trata exchanges, queues e bindings como metadata/topology exportável.
- Aliases e paráfrases:
  - definições de schema
  - recorte de definitions
  - topologia como artefato
- Termos relacionados que também exigem preparo:
  - schema
  - metadata
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: não
  - visual/aria-label: não
  - referências: sim
  - comentário final: não
- Usos permitidos:
  - introduzir snippet conceitual mínimo.
  - reforçar que bindings são parte da topologia.
- Usos proibidos:
  - ensinar export/import.
  - mostrar comando ou endpoint.
- Fronteira com nodes futuros: operations, permissions e policies ficam fora.
- Fonte base: F6.

## Conceitos Permitidos Só no Dump

### permissions

- Motivo: tema reservado a node próprio.
- Por que não deve aparecer no HTML: discutir configure/write/read invadiria `intermediario/05`.
- Aliases bloqueados no HTML:
  - permissions
  - permissões
  - configure permission
  - write permission
  - read permission
- Fonte base: F7.

### policy

- Motivo: tema reservado a node próprio.
- Por que não deve aparecer no HTML: policies e x-arguments ficam em `intermediario/05`.
- Aliases bloqueados no HTML:
  - policy
  - policies
  - política
  - políticas
  - x-arguments
  - argumentos opcionais
- Fonte base: F1, F7.

### alternate exchange

- Motivo: tema reservado a node próprio.
- Por que não deve aparecer no HTML: fallback de roteamento fica em `intermediario/03`.
- Aliases bloqueados no HTML:
  - alternate exchange
  - AE
  - exchange alternativa
  - fallback de roteamento
- Fonte base: F1.

### publisher confirms

- Motivo: tema reservado a node próprio.
- Por que não deve aparecer no HTML: confiabilidade de aceite pelo broker fica em `intermediario/07`.
- Aliases bloqueados no HTML:
  - confirms
  - publisher confirm
  - publisher confirms
  - confirmação do publisher
- Fonte base: F2.

## Conceitos Reservados a Nodes Futuros

### decisão de entrega do próximo node

- Node responsável: Broadcast vs consumidores competindo
- Node ID responsável, quando existir: `intermediario/02-broadcast-vs-consumidores-competindo`
- Menção permitida no HTML atual: curta como handoff final
- Aliases bloqueados:
  - competing consumers
  - cópia por consumidor
- Condição de exceção: o label canônico do próximo node pode aparecer no contexto de posição e no fechamento narrativo curto.

### DLX e retry

- Node responsável: Dead Letter Exchanges e retry conceitual
- Node ID responsável, quando existir: `intermediario/04-dead-letter-exchanges-e-retry-conceitual`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - DLX
  - dead letter
  - retry
  - redelivery
- Condição de exceção: nenhuma.

### exchange-to-exchange bindings

- Node responsável: Exchange-to-exchange bindings
- Node ID responsável, quando existir: `intermediario/06-exchange-to-exchange-bindings`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - E2E
  - exchange-to-exchange
  - exchange para exchange
- Condição de exceção: nenhuma.

### topologia multi-cluster

- Node responsável: Federated exchanges e WAN
- Node ID responsável, quando existir: `avancado/04-federated-exchanges-e-wan`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - federation
  - federated
  - WAN
  - multi-cluster
- Condição de exceção: nenhuma.

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | exchanges | sim | Documentação oficial de exchanges |
| F2 | publishers | sim | Guia oficial de publishers |
| F3 | AMQP 0-9-1 | sim | Guia oficial do modelo AMQP 0-9-1 |
| F4 | AMQP 0-9-1 specification | sim | Especificação AMQP 0-9-1 |
| F5 | queues | sim | Documentação oficial de filas |
| F6 | schema definitions | sim | Definições de schema do RabbitMQ |
| F7 | access control | não | manter apenas no dump |
