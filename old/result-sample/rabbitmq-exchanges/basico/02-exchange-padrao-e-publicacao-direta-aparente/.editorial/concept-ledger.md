# Concept ledger

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Level: `basico`
- Node: `02-exchange-padrao-e-publicacao-direta-aparente`
- Node ID: `basico/02-exchange-padrao-e-publicacao-direta-aparente`
- Data: 2026-06-08
- Fonte principal: `.tmp/roadmaps/rabbitmq-exchanges/basico/02-exchange-padrao-e-publicacao-direta-aparente/research-dump.md`

## Conceitos Permitidos no HTML

### Exchange padrão / default exchange

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, no `title` e no H1 como label do node; no corpo, preparar como exchange especial que já existe.
- Primeira ocorrência permitida: `title`, H1 e lead.
- Explicação mínima exigida antes da primeira ocorrência: no corpo, retomar que o publisher continua publicando em uma exchange e então apresentar a exchange especial.
- Aliases e paráfrases:
  - exchange padrão
  - default exchange
  - exchange especial
  - exchange que já existe
  - exchange pré-declarada
  - pre-declared exchange
- Termos relacionados que também exigem preparo:
  - nome vazio
  - string vazia
  - binding automático
  - routing key como nome da fila
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar a aparência de publicar em fila.
  - contrastar com direct exchange própria.
  - registrar que não é exchange regular para bindings customizados.
- Usos proibidos:
  - apresentar como topologia de domínio.
  - tratar como ausência de exchange.
  - ensinar permissões ou governance.
- Fronteira com nodes futuros: direct em profundidade fica no node 04; governança fica no intermediário.
- Fonte base: F1, F2, F3.

### Nome vazio da exchange

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, se aparecer como literal dentro da pergunta-motor imediatamente explicado.
- Primeira ocorrência permitida: abertura narrativa ou snippet conceitual.
- Explicação mínima exigida antes da primeira ocorrência: dizer que a exchange especial é selecionada por um valor sem caracteres no campo de exchange.
- Aliases e paráfrases:
  - `""`
  - string vazia
  - nome vazio
  - empty string exchange name
  - `exchange=""`
  - `exchange=''`
- Termos relacionados que também exigem preparo:
  - default exchange
  - routing key
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar o campo de publicação AMQP 0-9-1.
  - distinguir de `amq.default`.
- Usos proibidos:
  - dizer que significa "sem exchange".
  - usar como routing key.
- Fronteira com nodes futuros: diferenças de permissões e nomes operacionais ficam fora.
- Fonte base: F1, F2, F5.

### Routing key como nome da fila

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como material observado no lead/snippet inicial e no contexto de posição como label do próximo node exigido pelo contrato; como conceito explicativo, não.
- Primeira ocorrência permitida: lead, snippet conceitual ou contexto de posição; a primeira ocorrência explicativa deve vir depois de mostrar que a default exchange precisa de um valor para escolher a fila.
- Explicação mínima exigida antes da primeira ocorrência explicativa: apresentar como a chave que acompanha a publicação e, neste caso específico, carrega o nome da fila.
- Aliases e paráfrases:
  - routing key
  - `routing_key`
  - chave de roteamento
  - chave da publicação
  - nome da fila como chave
- Termos relacionados que também exigem preparo:
  - binding automático
  - fila
- Pode aparecer em:
  - título: não
  - lead: sim, apenas como campo observado no exemplo inicial
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - aparecer no contexto de posição como parte do label `Bindings, routing key e destinos`.
  - aparecer no lead como par de campos que motiva a pergunta do node.
  - no caso específico da default exchange, igualar ao nome da fila.
  - aparecer em snippet conceitual de campos.
- Usos proibidos:
  - generalizar que routing key sempre é nome de fila.
  - comparar padrões de topic ou binding key.
- Fronteira com nodes futuros: node 03 separa routing key, binding key e destinos.
- Fonte base: F1, F2, F3, F5.

### Binding automático

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de apresentar a fila e a routing key como nome da fila.
- Explicação mínima exigida antes da primeira ocorrência: dizer que o broker cria a ligação da fila com a default exchange no momento da declaração da fila.
- Aliases e paráfrases:
  - binding automático
  - ligação automática
  - vínculo automático
  - regra automática
  - ligação criada pelo broker
- Termos relacionados que também exigem preparo:
  - default exchange
  - routing key
  - fila
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar a rota pela default exchange.
  - dizer que a aplicação não cria bindings manuais nessa exchange.
- Usos proibidos:
  - aprofundar source/destination ou binding key.
  - sugerir bind/unbind manual na default exchange.
- Fronteira com nodes futuros: node 03 aprofunda binding; este node só usa a regra automática.
- Fonte base: F1, F2, F3.

### Publicação direta aparente

- Tipo: efeito didático
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como pergunta-motor.
- Primeira ocorrência permitida: H1 por label do node; no corpo, depois de mostrar `exchange=""` e `routing_key`.
- Explicação mínima exigida antes da primeira ocorrência: mostrar que o publisher informa o nome da fila, mas ainda passa pela default exchange.
- Aliases e paráfrases:
  - publicação direta aparente
  - parece publicar direto
  - aparência de envio direto
  - envio direto aparente
  - conveniência de envio para fila
- Termos relacionados que também exigem preparo:
  - default exchange
  - nome vazio
  - binding automático
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - nomear a impressão causada por exemplos simples.
  - fechar o critério de domínio do node.
- Usos proibidos:
  - transformar em recomendação de arquitetura.
- Fronteira com nodes futuros: contratos de domínio ficam no intermediário.
- Fonte base: F2, F5.

### Direct exchange própria

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois que a default exchange já estiver compreendida.
- Explicação mínima exigida antes da primeira ocorrência: dizer que é uma exchange declarada pela aplicação para expor uma rota explícita, em vez do nome da fila.
- Aliases e paráfrases:
  - direct exchange própria
  - exchange direct própria
  - exchange separada
  - exchange de domínio
  - topologia explícita
  - `orders.direct`
- Termos relacionados que também exigem preparo:
  - default exchange
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
  - comparação curta com default exchange.
  - recomendação conceitual para topologia explícita sem passo a passo.
- Usos proibidos:
  - ensinar tipos clássicos em profundidade.
  - abrir fanout, topic ou headers.
- Fronteira com nodes futuros: direct completo fica no node 04.
- Fonte base: F1, F2.

### `amq.default`

- Tipo: nome de referência
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que o campo de publicação usa `""`.
- Explicação mínima exigida antes da primeira ocorrência: dizer que RabbitMQ pode mostrar outro identificador para a mesma exchange em alguns contextos, mas esse não é o valor do campo de publicação AMQP 0-9-1.
- Aliases e paráfrases:
  - `amq.default`
  - nome de referência `amq.default`
- Termos relacionados que também exigem preparo:
  - nome vazio
  - default exchange
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: não
  - visual/aria-label: não
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - nota curta de fronteira para não usar `amq.default` como nome de publicação.
- Usos proibidos:
  - discutir permissões.
  - discutir governance.
  - ensinar regex ou operações `configure`, `write`, `read`.
- Fronteira com nodes futuros: permissões ficam no intermediário.
- Fonte base: F1.

### `task_queue`

- Tipo: exemplo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como exemplo condutor.
- Primeira ocorrência permitida: abertura narrativa.
- Explicação mínima exigida antes da primeira ocorrência: apresentar como uma fila simples de trabalho usada para ler o mecanismo, não como topologia de domínio.
- Aliases e paráfrases:
  - `task_queue`
  - fila de trabalho
  - fila operacional simples
- Termos relacionados que também exigem preparo:
  - routing key
  - default exchange
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - exemplo condutor do node.
  - contraste com `orders.direct`.
- Usos proibidos:
  - virar tutorial de execução.
  - substituir uma discussão de contrato de domínio.
- Fronteira com nodes futuros: não usar exemplo de pedidos do node 01.
- Fonte base: F5.

## Conceitos Permitidos Só no Dump

### `mandatory`

- Motivo: comportamento de mensagem sem rota pertence ao intermediário.
- Por que não deve aparecer no HTML: invadiria `intermediario/03-unroutable-mandatory-e-alternate-exchange`.
- Aliases bloqueados no HTML:
  - `mandatory`
  - flag mandatory
  - mensagem retornada ao publisher
- Fonte base: F4.

### Alternate Exchange

- Motivo: fallback de rota pertence ao intermediário.
- Por que não deve aparecer no HTML: desviaria a página para mensagens sem rota.
- Aliases bloqueados no HTML:
  - Alternate Exchange
  - alternate exchange
  - AE
  - exchange alternativa
- Fonte base: F4.

### Publisher confirms

- Motivo: confiabilidade de publicação pertence ao intermediário.
- Por que não deve aparecer no HTML: o node atual é sobre endereçamento pela default exchange, não confirmação.
- Aliases bloqueados no HTML:
  - publisher confirm
  - publisher confirms
  - confirmação de publisher
- Fonte base: F4.

### Permissões RabbitMQ

- Motivo: governança e acesso ficam em node posterior.
- Por que não deve aparecer no HTML: o contrato proíbe discutir permissões e governance.
- Aliases bloqueados no HTML:
  - permissões
  - governance
  - configure
  - write permission
  - read permission
  - regex de permissão
- Fonte base: F1.

## Conceitos Reservados a Nodes Futuros

### Binding key

- Node responsável: Bindings, routing key e destinos
- Node ID responsável, quando existir: `basico/03-bindings-routing-key-e-destinos`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - binding key
  - chave de binding
  - chave do binding
  - source exchange
  - destination queue
  - destination exchange
- Condição de exceção: nenhuma; usar "ligação automática" no HTML atual.

### Tipos clássicos completos

- Node responsável: Direct, fanout e topic
- Node ID responsável, quando existir: `basico/04-direct-fanout-e-topic`
- Menção permitida no HTML atual: curta para direct exchange própria, sem fanout/topic.
- Aliases bloqueados:
  - fanout
  - topic
  - headers exchange
  - headers
  - wildcard
  - multicast
- Condição de exceção: nenhuma.

### Mensagem sem rota

- Node responsável: Unroutable, mandatory e Alternate Exchange
- Node ID responsável, quando existir: `intermediario/03-unroutable-mandatory-e-alternate-exchange`
- Menção permitida no HTML atual: no máximo fronteira sem termo técnico; preferir omitir.
- Aliases bloqueados:
  - unroutable
  - sem rota
  - mensagem sem rota
  - descarte
  - basic.return
- Condição de exceção: nenhuma.

### Contrato de topologia

- Node responsável: Contrato de topologia e roteamento
- Node ID responsável, quando existir: `intermediario/01-contrato-de-topologia-e-roteamento`
- Menção permitida no HTML atual: curta como "topologia explícita".
- Aliases bloqueados:
  - topology contract
  - contrato de routing key
  - ownership
  - ownership de exchange
  - event contract
- Condição de exceção: nenhuma.

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Exchanges | Sim | `RabbitMQ - Exchanges` |
| F2 | AMQP 0-9-1 Model | Sim | `RabbitMQ - AMQP 0-9-1 Model Explained` |
| F3 | Advanced Message Queuing Protocol Specification | Sim | `AMQP 0-9-1 specification` |
| F4 | Publishers | Sim, depois de publicar em exchange estar preparado | `RabbitMQ - Publishers` |
| F5 | Hello World tutorial | Sim, depois do snippet conceitual | `RabbitMQ - Hello World tutorial` |
