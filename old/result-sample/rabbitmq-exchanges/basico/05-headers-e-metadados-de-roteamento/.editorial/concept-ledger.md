# Concept ledger

## Metadados

- Roadmap: rabbitmq-exchanges
- Level: basico
- Node: Headers exchange e metadados de roteamento
- Node ID: basico/05-headers-e-metadados-de-roteamento
- Data: 2026-06-08
- Fonte principal: research-dump.md, F2 e F3

## Conceitos Permitidos no HTML

### Atributos independentes de roteamento

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum
- Primeira ocorrencia permitida: abertura narrativa, antes de headers exchange
- Explicacao minima exigida antes da primeira ocorrencia: mostrar que a decisao nao forma uma hierarquia textual unica
- Aliases e parafrases:
  - atributos independentes
  - criterios independentes
  - eixos independentes
  - etiquetas independentes
- Termos relacionados que tambem exigem preparo:
  - tenant
  - format
  - priority
- Pode aparecer em:
  - titulo: nao
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: nao
  - comentario final: sim
- Usos permitidos:
  - justificar quando headers e mais natural que uma routing key longa
  - comparar com hierarquia textual de topic
- Usos proibidos:
  - transformar em contrato de topologia completo
  - usar como recomendacao para todo dado de negocio
- Fronteira com nodes futuros: contratos, naming e governanca ficam no intermediario
- Fonte base: F2 e inferencia do contrato

### Routing key

- Tipo: termo herdado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim
- Primeira ocorrencia permitida: lead, como conceito herdado do node 04
- Explicacao minima exigida antes da primeira ocorrencia: nao exigida; herdado
- Aliases e parafrases:
  - key textual
  - chave de roteamento
  - routing key textual
- Termos relacionados que tambem exigem preparo:
  - topic
  - binding
- Pode aparecer em:
  - titulo: nao
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - explicar que headers exchange ignora esse campo
  - comparar com topic e direct ja herdados
- Usos proibidos:
  - reensinar direct/fanout/topic em profundidade
- Fronteira com nodes futuros: mensagens sem rota e mandatory ficam fora
- Fonte base: node 04, F2, F3

### Message headers

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "mapa de metadados"
- Primeira ocorrencia permitida: primeira secao de fronteira entre key, headers e payload
- Explicacao minima exigida antes da primeira ocorrencia: dizer que a mensagem carrega metadados separados do corpo
- Aliases e parafrases:
  - headers da mensagem
  - cabecalhos da mensagem
  - mapa de metadados
  - metadados da mensagem
- Termos relacionados que tambem exigem preparo:
  - payload opaco
  - argumentos do binding
- Pode aparecer em:
  - titulo: sim, pelo titulo do node
  - lead: nao, salvo como parte do label do node
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - fonte de atributos avaliados por headers exchange
  - contraste com corpo/payload
- Usos proibidos:
  - tratar como schema de payload
  - tratar como dados automaticamente seguros para negocio sensivel
- Fronteira com nodes futuros: serializers e schema de payload fora do roadmap deste node
- Fonte base: F2, F3

### Payload opaco

- Tipo: fronteira
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como "corpo nao lido pela exchange"
- Primeira ocorrencia permitida: primeira secao visual
- Explicacao minima exigida antes da primeira ocorrencia: separar corpo da mensagem dos headers
- Aliases e parafrases:
  - corpo opaco
  - corpo da mensagem nao interpretado
  - payload nao lido
  - broker nao abre o corpo
- Termos relacionados que tambem exigem preparo:
  - message headers
- Pode aparecer em:
  - titulo: nao
  - lead: nao
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - reforcar que headers exchange nao roteia lendo JSON, XML ou binario
- Usos proibidos:
  - abrir detalhes de serializer ou schema
- Fronteira com nodes futuros: payload schema e serializers fora de escopo
- Fonte base: F2, F3

### Headers exchange

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim no titulo e no contexto por ser label do node
- Primeira ocorrencia permitida: H1 e contexto; no corpo, depois de preparar atributos independentes e headers
- Explicacao minima exigida antes da primeira ocorrencia no corpo: mostrar que a exchange compara metadados da mensagem com regra do binding
- Aliases e parafrases:
  - exchange de headers
  - tipo headers
  - roteamento por headers
  - routing by attributes
- Termos relacionados que tambem exigem preparo:
  - message headers
  - argumentos do binding
  - `x-match`
- Pode aparecer em:
  - titulo: sim
  - lead: sim como label/tema
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - explicar tipo que ignora routing key e avalia headers
  - completar tipos classicos do nivel basico
- Usos proibidos:
  - tratar como substituto automatico de topic
  - abrir plugins e tipos especializados
- Fronteira com nodes futuros: plugins ficam no avancado
- Fonte base: F2, F3

### Argumentos do binding

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim como "regra registrada na ligacao"
- Primeira ocorrencia permitida: secao que mostra a regra de match
- Explicacao minima exigida antes da primeira ocorrencia: dizer que a ligacao registra pares nome/valor
- Aliases e parafrases:
  - binding arguments
  - argumentos da ligacao
  - pares no binding
  - regra do binding
- Termos relacionados que tambem exigem preparo:
  - `x-match`
  - message headers
- Pode aparecer em:
  - titulo: nao
  - lead: nao
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - explicar onde ficam os criterios da headers exchange
- Usos proibidos:
  - discutir policies, permissoes ou operator policies
  - confundir com argumentos de declaracao de exchange
- Fronteira com nodes futuros: policies e permissoes ficam no intermediario
- Fonte base: F1, F2, F3

### `x-match`

- Tipo: parametro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: nao, salvo em snippet/tabela depois de explicado
- Primeira ocorrencia permitida: depois de explicar a pergunta "todos ou qualquer criterio?"
- Explicacao minima exigida antes da primeira ocorrencia: mostrar que multiplos headers precisam de uma regra de combinacao
- Aliases e parafrases:
  - x-match
  - argumento especial de match
  - seletor all/any
- Termos relacionados que tambem exigem preparo:
  - `all`
  - `any`
  - `all-with-x`
  - `any-with-x`
- Pode aparecer em:
  - titulo: nao
  - lead: nao
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - diferenciar regra restritiva e permissiva
- Usos proibidos:
  - tratar como header da mensagem
  - abrir linguagem de query ou politica
- Fronteira com nodes futuros: `x-arguments` gerais ficam fora
- Fonte base: F2, F3

### `all` e `any`

- Tipo: valor de parametro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: nao
- Primeira ocorrencia permitida: tabela de `x-match`
- Explicacao minima exigida antes da primeira ocorrencia: explicar que a lista de criterios precisa ser lida como "todos" ou "qualquer"
- Aliases e parafrases:
  - todos os pares
  - qualquer par
  - regra restritiva
  - regra permissiva
- Termos relacionados que tambem exigem preparo:
  - `x-match`
- Pode aparecer em:
  - titulo: nao
  - lead: nao
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - explicar seletividade da regra
- Usos proibidos:
  - sugerir que `any` avalia qualquer header da mensagem fora do binding
- Fronteira com nodes futuros: nao virar linguagem de filtro avancada
- Fonte base: F2, F3

### `all-with-x` e `any-with-x`

- Tipo: valor de parametro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: nao
- Primeira ocorrencia permitida: depois de `all` e `any`
- Explicacao minima exigida antes da primeira ocorrencia: explicar que headers com prefixo `x-` podem ficar dentro ou fora da avaliacao
- Aliases e parafrases:
  - variantes with-x
  - considerar headers x-
  - incluir headers x-
- Termos relacionados que tambem exigem preparo:
  - headers iniciados por `x-`
  - `x-match`
- Pode aparecer em:
  - titulo: nao
  - lead: nao
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: nao
- Usos permitidos:
  - diferenciar comportamento RabbitMQ 4.3
- Usos proibidos:
  - generalizar para todo broker AMQP
  - criar convencao de negocio baseada em `x-`
- Fronteira com nodes futuros: governanca de convencoes fica fora
- Fonte base: F2

### Topic exchange

- Tipo: termo herdado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, herdado do node 04
- Primeira ocorrencia permitida: comparacao final
- Explicacao minima exigida antes da primeira ocorrencia: nao exigida; herdado
- Aliases e parafrases:
  - topic
  - routing key segmentada
  - padrao por segmentos
- Termos relacionados que tambem exigem preparo:
  - routing key
- Pode aparecer em:
  - titulo: nao
  - lead: nao
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referencias: sim
  - comentario final: sim
- Usos permitidos:
  - comparar hierarquia textual com atributos independentes
- Usos proibidos:
  - reensinar `*`, `#` e patterns
- Fronteira com nodes futuros: contrato de nomenclatura fica no intermediario
- Fonte base: node 04, F2

## Conceitos Permitidos So no Dump

### Presenca sem valor em binding arguments

- Motivo: a especificacao permite match por presenca quando o argumento nao tem valor.
- Por que nao deve aparecer no HTML: aumentaria densidade do basico sem ser necessario para o criterio de dominio.
- Aliases bloqueados no HTML:
  - sem valor
  - presenca de header
  - field without value
- Fonte base: F3

### Field tables

- Motivo: explica o formato AMQP de pares nome/valor.
- Por que nao deve aparecer no HTML: e detalhe de protocolo, nao necessario para a narrativa do node.
- Aliases bloqueados no HTML:
  - field table
  - tabelas de campo
  - tabela AMQP
- Fonte base: F3

## Conceitos Reservados a Nodes Futuros

### Consumers, acknowledgements e distribuicao de trabalho

- Node responsavel: Filas, consumidores e entrega
- Node ID responsavel, quando existir: `basico/06-filas-consumidores-e-entrega`
- Mencao permitida no HTML atual: curta como handoff final
- Aliases bloqueados:
  - consumer ack
  - consumidores competindo
  - distribuicao de trabalho
- Condicao de excecao: somente no contexto de posicao ou handoff final.

### Policies, permissoes e governanca de argumentos

- Node responsavel: Policies, x-arguments e permissoes
- Node ID responsavel, quando existir: `intermediario/05-policies-x-arguments-e-permissoes`
- Mencao permitida no HTML atual: nenhuma ou fronteira curta
- Aliases bloqueados:
  - policy
  - policies
  - operator policy
  - permissoes
  - permission
  - access control
- Condicao de excecao: referencias tecnicas da fonte nao devem dominar o HTML.

### DLX, AE, mandatory e mensagens sem rota

- Node responsavel: Unroutable, mandatory e alternate exchange / Dead letter exchanges e retry conceitual
- Node ID responsavel, quando existir: `intermediario/03-unroutable-mandatory-e-alternate-exchange`
- Mencao permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - DLX
  - dead-letter
  - dead letter
  - alternate exchange
  - AE
  - mandatory
  - return
- Condicao de excecao: nenhuma no HTML atual.

### Serializers e schema de payload

- Node responsavel: fora do node atual
- Node ID responsavel, quando existir: nao aplicavel
- Mencao permitida no HTML atual: curta como fora de escopo sem detalhar
- Aliases bloqueados:
  - serializer
  - serializers
  - payload schema
  - schema do payload
  - JSON schema
  - XML schema
- Condicao de excecao: mencionar que o corpo nao e interpretado pela exchange sem abrir formatos.

### Plugins e tipos especializados

- Node responsavel: Tipos especializados e plugins
- Node ID responsavel, quando existir: `avancado/02-tipos-especializados-e-plugins`
- Mencao permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - plugin
  - plugins
  - exchange especializada
  - tipo especializado
- Condicao de excecao: nenhuma no HTML atual.

## Titulos de Fontes e Termos de Referencia

| Fonte | Termos carregados pelo titulo | Pode aparecer visivel? | Forma visivel recomendada |
|---|---|---|---|
| https://www.rabbitmq.com/docs/exchanges | Exchanges | sim | Documentacao oficial de exchanges |
| https://www.rabbitmq.com/tutorials/amqp-concepts | AMQP 0-9-1, Model, Concepts | sim | Guia oficial AMQP 0-9-1 |
| https://www.rabbitmq.com/assets/files/amqp0-9-1-43a54a005e97180a4fbe6e567a125d84.pdf | AMQP 0-9-1 specification | sim | Especificacao AMQP 0-9-1 |
