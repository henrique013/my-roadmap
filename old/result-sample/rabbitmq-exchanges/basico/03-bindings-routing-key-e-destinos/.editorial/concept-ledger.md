# Concept ledger

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Level: `basico`
- Node: `03-bindings-routing-key-e-destinos`
- Node ID: `basico/03-bindings-routing-key-e-destinos`
- Data: 2026-06-08
- Fonte principal: `research-dump.md`

## Conceitos Permitidos no HTML

### Binding

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum "ligação" ou "regra de saída"
- Primeira ocorrência permitida: depois de a exchange ser apresentada como uma tabela sem saídas
- Explicação mínima exigida antes da primeira ocorrência: regra que conecta uma exchange de origem a um destino
- Aliases e paráfrases:
  - binding
  - ligação
  - regra de roteamento
  - regra de saída
  - linha da tabela
- Termos relacionados que também exigem preparo:
  - source exchange
  - destination
  - binding key
  - binding arguments
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - regra que liga source exchange a destino
  - linha de topologia avaliada pela exchange
  - ponte entre routing key da publicação e destino
- Usos proibidos:
  - tratar binding como mensagem
  - tratar binding como fila ou armazenamento
  - tratar binding como consumer
- Fronteira com nodes futuros: tipos de exchange e E2E usam bindings, mas não devem ser reexplicados agora.
- Fonte base: F1, F2, F6.

### Routing key

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, herdada do node anterior, mas precisa ser recontextualizada
- Primeira ocorrência permitida: lead ou abertura, acompanhada da ideia de valor enviado na publicação
- Explicação mínima exigida antes da primeira ocorrência: valor que acompanha a publicação e pode ajudar a exchange a escolher rotas
- Aliases e paráfrases:
  - routing key
  - chave de roteamento
  - chave da publicação
  - valor enviado pelo publisher
- Termos relacionados que também exigem preparo:
  - binding key
  - publisher
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
  - valor da publicação
  - dado comparado por alguns tipos de exchange
  - chave que pode coincidir com o critério do binding
- Usos proibidos:
  - chamar a key da regra de routing key sem explicar o contexto
  - afirmar que toda routing key é nome de fila
  - afirmar que todos os tipos de exchange a usam do mesmo modo
- Fronteira com nodes futuros: wildcards, padrões e tipos clássicos ficam no próximo node.
- Fonte base: F1, F2, F3, F6.

### Binding key

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de binding e routing key terem sido separados
- Explicação mínima exigida antes da primeira ocorrência: chave registrada na regra de binding como critério
- Aliases e paráfrases:
  - binding key
  - chave do binding
  - key da regra
  - critério da ligação
  - chave registrada na regra
- Termos relacionados que também exigem preparo:
  - binding
  - routing key
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - critério do binding
  - valor que pode coincidir com a routing key da publicação
- Usos proibidos:
  - tratar como valor sempre enviado pelo publisher
  - explicar match exato, wildcard ou pattern em profundidade
- Fronteira com nodes futuros: regras detalhadas de match ficam em `basico/04-direct-fanout-e-topic`.
- Fonte base: F1, F2, F4, F6.

### Source exchange

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "exchange de origem"
- Primeira ocorrência permitida: depois de binding como relação direcional
- Explicação mínima exigida antes da primeira ocorrência: exchange onde a regra começa e onde a publicação é avaliada
- Aliases e paráfrases:
  - source exchange
  - exchange de origem
  - origem do binding
  - source
- Termos relacionados que também exigem preparo:
  - destination
  - binding
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - exchange que possui os bindings avaliados
  - origem de uma relação source -> destination
- Usos proibidos:
  - confundir source com publisher
  - usar upstream/downstream
- Fronteira com nodes futuros: composição avançada e federation não entram.
- Fonte base: F1, F4, F5.

### Destination e destination type

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "destino"
- Primeira ocorrência permitida: depois de binding como regra de saída
- Explicação mínima exigida antes da primeira ocorrência: recurso para onde a regra aponta e sua categoria
- Aliases e paráfrases:
  - destination
  - destino
  - destination type
  - tipo de destino
  - destination queue
  - destination exchange
  - stream como destino
- Termos relacionados que também exigem preparo:
  - queue
  - stream
  - exchange
- Pode aparecer em:
  - título: sim, se o título já estiver no contexto do node
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - indicar queue, stream ou exchange como destino da regra
  - classificar a saída de um binding
- Usos proibidos:
  - explicar stream em profundidade
  - explicar exchange-to-exchange binding em profundidade
  - tratar destination como consumer final
- Fronteira com nodes futuros: filas/consumers no node 06; E2E no intermediário.
- Fonte base: F1, F3, F4, F5.

### Binding arguments

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de a forma do binding já estar estabelecida
- Explicação mínima exigida antes da primeira ocorrência: parâmetros opcionais carregados pela regra
- Aliases e paráfrases:
  - binding arguments
  - argumentos
  - argumentos de binding
  - parâmetros da regra
- Termos relacionados que também exigem preparo:
  - binding
  - tipo de exchange
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - mapa opcional da regra
  - parâmetro lido por alguns tipos de exchange
- Usos proibidos:
  - payload da mensagem
  - configuração global da exchange
  - policy
- Fronteira com nodes futuros: headers exchange e `x-match` ficam para `basico/05-headers-e-metadados-de-roteamento`.
- Fonte base: F1, F4.

### Tabela de roteamento vazia

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "sem saídas" ou "sem regras"
- Primeira ocorrência permitida: abertura
- Explicação mínima exigida antes da primeira ocorrência: exchange sem bindings não tem regra para encaminhar a publicação
- Aliases e paráfrases:
  - tabela de roteamento vazia
  - tabela sem linhas
  - exchange sem bindings
  - sem saídas
  - sem regra de saída
- Termos relacionados que também exigem preparo:
  - binding
  - rota
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - estado de uma exchange recém-declarada sem regras
  - contraste com fila vazia
- Usos proibidos:
  - buffer de mensagens
  - fila vazia
  - promessa de retenção até criar binding
- Fronteira com nodes futuros: tratamento de mensagens sem rota fica no intermediário.
- Fonte base: F1, F2, F3.

### Zero, uma ou várias rotas

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como consequência da avaliação das regras
- Primeira ocorrência permitida: depois de binding e routing key
- Explicação mínima exigida antes da primeira ocorrência: a exchange avalia suas regras e pode encontrar nenhuma, uma ou mais saídas
- Aliases e paráfrases:
  - zero rota
  - uma rota
  - várias rotas
  - múltiplos destinos
  - mais de uma saída
- Termos relacionados que também exigem preparo:
  - binding
  - destination
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - cardinalidade de roteamento inicial
  - múltiplas cópias para destinos diferentes
- Usos proibidos:
  - competir consumers
  - guarantees ou confirmação
  - returned messages
- Fronteira com nodes futuros: consumers no node 06; returns e AE no intermediário.
- Fonte base: F1, F2.

## Conceitos Permitidos Só no Dump

### mandatory

- Motivo: pertence ao tratamento de publicação sem rota.
- Por que não deve aparecer no HTML: abriria o node intermediário de unroutable.
- Aliases bloqueados no HTML:
  - mandatory
  - mandatory flag
- Fonte base: F3.

### Alternate exchange

- Motivo: pertence ao tratamento de mensagens sem rota.
- Por que não deve aparecer no HTML: invadiria `intermediario/03-unroutable-mandatory-e-alternate-exchange`.
- Aliases bloqueados no HTML:
  - alternate exchange
  - AE
- Fonte base: F1, F3.

### Returned message

- Motivo: sinal operacional de publicação sem rota.
- Por que não deve aparecer no HTML: o node atual só trata ausência de rota em nível conceitual.
- Aliases bloqueados no HTML:
  - returned message
  - returned messages
  - mensagem retornada
  - mensagens retornadas
- Fonte base: F3.

### Publisher confirm

- Motivo: confirmação broker -> publisher fica em node intermediário.
- Por que não deve aparecer no HTML: confundiria decisão de rota com sinal de confiabilidade.
- Aliases bloqueados no HTML:
  - publisher confirm
  - publisher confirms
  - confirm do publisher
- Fonte base: F3.

### x-match

- Motivo: conceito próprio de headers exchange.
- Por que não deve aparecer no HTML: pertence ao node 05.
- Aliases bloqueados no HTML:
  - x-match
  - headers exchange
- Fonte base: F1.

## Conceitos Reservados a Nodes Futuros

### Direct exchange

- Node responsável: Direct, fanout e topic
- Node ID responsável, quando existir: `basico/04-direct-fanout-e-topic`
- Menção permitida no HTML atual: apenas no contexto de navegação do próximo node
- Aliases bloqueados:
  - direct exchange
- Condição de exceção: o label do próximo node pode aparecer em `data-node-position`.

### Fanout exchange

- Node responsável: Direct, fanout e topic
- Node ID responsável, quando existir: `basico/04-direct-fanout-e-topic`
- Menção permitida no HTML atual: apenas no contexto de navegação do próximo node
- Aliases bloqueados:
  - fanout exchange
- Condição de exceção: o label do próximo node pode aparecer em `data-node-position`.

### Topic exchange

- Node responsável: Direct, fanout e topic
- Node ID responsável, quando existir: `basico/04-direct-fanout-e-topic`
- Menção permitida no HTML atual: apenas no contexto de navegação do próximo node
- Aliases bloqueados:
  - topic exchange
- Condição de exceção: o label do próximo node pode aparecer em `data-node-position`.

### Headers exchange

- Node responsável: Headers exchange e metadados de roteamento
- Node ID responsável, quando existir: `basico/05-headers-e-metadados-de-roteamento`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - headers exchange
  - roteamento por headers
  - x-match
- Condição de exceção: nenhuma no HTML atual.

### Mensagens sem rota

- Node responsável: Unroutable, mandatory e alternate exchange
- Node ID responsável, quando existir: `intermediario/03-unroutable-mandatory-e-alternate-exchange`
- Menção permitida no HTML atual: curta como consequência conceitual, sem termos operacionais
- Aliases bloqueados:
  - unroutable
  - sem rota
  - mensagem sem rota
  - mensagens sem rota
  - mandatory
  - alternate exchange
  - returned message
- Condição de exceção: usar "nenhuma saída" ou "não encontra destino inicial" é permitido.

### Exchange-to-exchange bindings

- Node responsável: Exchange-to-exchange bindings
- Node ID responsável, quando existir: `intermediario/06-exchange-to-exchange-bindings`
- Menção permitida no HTML atual: curta como fronteira
- Aliases bloqueados:
  - exchange-to-exchange
  - E2E
  - composição entre exchanges
- Condição de exceção: dizer que destination type pode ser `exchange` sem aprofundar.

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| RabbitMQ - Exchanges | exchanges | Sim | RabbitMQ - Exchanges |
| RabbitMQ - AMQP 0-9-1 Model Explained | AMQP 0-9-1 | Sim | RabbitMQ - Modelo AMQP 0-9-1 |
| RabbitMQ - Publishers | publishers | Sim | RabbitMQ - Publishers |
| RabbitMQ - HTTP API Reference | HTTP API | Sim | RabbitMQ - Referência da API HTTP |
| RabbitMQ - Exchange-to-exchange bindings | exchange-to-exchange bindings | Não | Manter no dump; no HTML basta dizer que destination type `exchange` existe |
| AMQP 0-9-1 specification | AMQP 0-9-1 | Sim | Especificação AMQP 0-9-1 |
