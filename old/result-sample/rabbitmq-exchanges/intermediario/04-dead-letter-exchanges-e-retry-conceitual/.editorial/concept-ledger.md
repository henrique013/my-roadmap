# Concept ledger

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Level: intermediario
- Node: Dead Letter Exchanges e retry conceitual
- Node ID: intermediario/04-dead-letter-exchanges-e-retry-conceitual
- Data: 2026-06-10
- Fonte principal: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/04-dead-letter-exchanges-e-retry-conceitual/research-dump.md`

## Conceitos Permitidos no HTML

### Mensagem já dentro da fila

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum
- Primeira ocorrência permitida: abertura, depois de retomar a fronteira com o node anterior
- Explicação mínima exigida antes da primeira ocorrência: mostrar que a exchange já encontrou destino e que o problema agora acontece depois da fila
- Aliases e paráfrases:
  - mensagem já está na fila
  - mensagem entrou na fila
  - depois da fila
  - dentro da fila
- Termos relacionados que também exigem preparo:
  - saída da fila
  - entrega ao consumer
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - separar DLX de AE
  - preparar consumer acknowledgement
- Usos proibidos:
  - sugerir que a exchange armazena a mensagem
- Fronteira com nodes futuros: diagnóstico de fila fica fora
- Fonte base: F1, F6, F7 no dump

### Dead Letter Exchange

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, apenas como label contratual do node em `.node-context`
- Primeira ocorrência permitida: label contratual do node; no corpo narrativo, depois de mostrar uma mensagem saindo de uma fila por decisão ou condição
- Explicação mínima exigida antes da primeira ocorrência: explicar que a fila pode republicar a mensagem para uma exchange normal
- Aliases e paráfrases:
  - Dead Letter Exchange
  - DLX
  - exchange de dead-letter
  - exchange de saída
- Termos relacionados que também exigem preparo:
  - dead-lettering
  - dead-lettered
  - fila de quarentena
- Pode aparecer em:
  - título: sim, após o lead já preparar a fronteira
  - lead: sim, se a frase já disser que é exchange usada por filas
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - exchange normal configurada em filas
  - destino de republicação de mensagens dead-lettered
- Usos proibidos:
  - chamar DLX de fila
  - tratar DLX como tipo especial de exchange
- Fronteira com nodes futuros: segurança de republicação, at-least-once dead-lettering e detalhes de quorum queues ficam fora
- Fonte base: F1 no dump

### Dead-lettering

- Tipo: evento
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de mostrar que a mensagem sai de uma fila por rejeição, expiração ou limite
- Explicação mínima exigida antes da primeira ocorrência: dizer que o evento é a saída da fila com republicação para uma DLX configurada
- Aliases e paráfrases:
  - dead-lettering
  - dead-lettered
  - mensagem dead-lettered
  - mensagem dead-lettered
- Termos relacionados que também exigem preparo:
  - DLX
  - retry queue
  - quarantine queue
- Pode aparecer em:
  - título: sim
  - lead: sim, se preparado
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - nomear o movimento da mensagem a partir da fila
  - listar causas
- Usos proibidos:
  - usar como sinônimo de erro genérico
- Fronteira com nodes futuros: headers de auditoria e garantias avançadas ficam fora
- Fonte base: F1 no dump

### Negative acknowledgement

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que o consumer não assumiu a mensagem como concluída
- Explicação mínima exigida antes da primeira ocorrência: consumer pode reconhecer positivamente ou rejeitar/nackar uma entrega
- Aliases e paráfrases:
  - negative acknowledgement
  - nack
  - rejeição
  - rejeitar a entrega
  - `basic.nack`
  - `basic.reject`
- Termos relacionados que também exigem preparo:
  - `requeue`
  - consumer acknowledgement
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar saída por `requeue=false`
  - contrastar com ack positivo
- Usos proibidos:
  - confundir com publisher confirm
- Fronteira com nodes futuros: publisher confirms ficam para outro node
- Fonte base: F2, F9 no dump

### `requeue`

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar a decisão do consumer ao rejeitar uma entrega
- Explicação mínima exigida antes da primeira ocorrência: `requeue` decide se a entrega volta para a fila ou sai para outro destino configurado
- Aliases e paráfrases:
  - `requeue=true`
  - `requeue=false`
  - requeue
  - devolver para a fila
  - recolocar na fila
- Termos relacionados que também exigem preparo:
  - redelivery
  - loop de redelivery
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - contrastar tentativa imediata com dead-lettering planejado
- Usos proibidos:
  - recomendar retry infinito
- Fronteira com nodes futuros: redelivery limit avançado e delayed retry nativo ficam fora
- Fonte base: F2, F8 no dump

### TTL

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de introduzir a necessidade de esperar antes de tentar de novo
- Explicação mínima exigida antes da primeira ocorrência: tempo máximo de permanência de uma mensagem na fila antes de expirar
- Aliases e paráfrases:
  - TTL
  - Time-to-Live
  - tempo de vida
  - expiração
  - expirar
- Termos relacionados que também exigem preparo:
  - fila de espera
  - retry queue
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar dead-lettering por expiração
  - explicar retry com atraso conceitual
- Usos proibidos:
  - tratar como scheduler exato
- Fronteira com nodes futuros: tuning e políticas detalhadas ficam fora
- Fonte base: F3 no dump

### Queue length limit

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: na lista de gatilhos depois que dead-lettering já foi preparado
- Explicação mínima exigida antes da primeira ocorrência: limite de mensagens ou bytes que pode forçar remoção ou dead-lettering
- Aliases e paráfrases:
  - queue length limit
  - limite de fila
  - limite de tamanho da fila
  - limite de comprimento da fila
- Termos relacionados que também exigem preparo:
  - overflow
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - causa de dead-lettering
- Usos proibidos:
  - abrir estratégia de capacidade
- Fronteira com nodes futuros: operação e observabilidade avançadas ficam fora
- Fonte base: F4 no dump

### Delivery limit

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: na lista de gatilhos depois de declarar que é restrito a quorum queues
- Explicação mínima exigida antes da primeira ocorrência: limite de tentativas em quorum queues que pode remover ou dead-letter a mensagem
- Aliases e paráfrases:
  - delivery limit
  - delivery-limit
  - limite de entrega
- Termos relacionados que também exigem preparo:
  - quorum queue
  - redelivery
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim, como fronteira
  - tabela: sim, como fronteira
  - visual/aria-label: sim, como fronteira
  - referências: sim
  - comentário final: não
- Usos permitidos:
  - completar a lista de causas de dead-lettering
  - mencionar que o aprofundamento fica para node avançado
- Usos proibidos:
  - generalizar para classic queues
  - detalhar contadores e delayed retry
- Fronteira com nodes futuros: node avançado de quorum queues
- Fonte base: F1, F8 no dump

### Retry queue

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que retry planejado precisa de espera, limite e retorno controlado
- Explicação mínima exigida antes da primeira ocorrência: fila de espera usada para uma nova tentativa posterior
- Aliases e paráfrases:
  - retry queue
  - fila de retry
  - fila de espera
  - espera antes da nova tentativa
- Termos relacionados que também exigem preparo:
  - TTL
  - backoff
  - DLX
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - modelo conceitual de retry com atraso
- Usos proibidos:
  - ensinar implementação completa de backoff
- Fronteira com nodes futuros: delayed retry nativo e redelivery limits avançados ficam fora
- Fonte base: F1, F3, F8 no dump

### Quarantine queue

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que uma mensagem pode não dever voltar ao fluxo principal
- Explicação mínima exigida antes da primeira ocorrência: fila de destino para análise quando a mensagem deve ser isolada
- Aliases e paráfrases:
  - quarantine queue
  - fila de quarentena
  - fila de análise
  - isolamento para análise
- Termos relacionados que também exigem preparo:
  - DLX
  - dead-lettering
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - destino conceitual de mensagens inválidas ou esgotadas
- Usos proibidos:
  - sugerir que a fila se gerencia sozinha sem observabilidade
- Fronteira com nodes futuros: diagnóstico operacional avançado fica fora
- Fonte base: F1, F9 no dump

### Policy e x-arguments

- Tipo: configuração
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, se apenas no label do próximo node ou em frase de handoff
- Primeira ocorrência permitida: depois de explicar que DLX é configuração da fila
- Explicação mínima exigida antes da primeira ocorrência: policies podem aplicar parâmetros a grupos de filas e são mais alteráveis que argumentos fixos em código
- Aliases e paráfrases:
  - policy
  - policies
  - x-arguments
  - argumentos opcionais
  - argumento fixo
- Termos relacionados que também exigem preparo:
  - permissões
  - governança
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim, como nota curta
  - tabela: sim
  - visual/aria-label: não
  - referências: sim
  - comentário final: sim, como handoff
- Usos permitidos:
  - registrar preferência por policies quando aplicável
  - apontar para o próximo node
- Usos proibidos:
  - explicar precedência, permissões ou operator policies
- Fronteira com nodes futuros: próximo node aprofunda o tema
- Fonte base: F1, F5 no dump

## Conceitos Permitidos Só no Dump

### `x-death`

- Motivo: útil para observabilidade e histórico de dead-lettering, mas abre diagnóstico e análise operacional.
- Por que não deve aparecer no HTML: desloca o node para headers e investigação, reservados para nodes avançados.
- Aliases bloqueados no HTML:
  - x-death
  - x-first-death
  - x-last-death
- Fonte base: F1 no dump

### At-least-once dead-lettering

- Motivo: detalhe de segurança de republicação em quorum queues.
- Por que não deve aparecer no HTML: pertence ao node avançado de quorum queues, DLX e redelivery limits.
- Aliases bloqueados no HTML:
  - at-least-once dead-lettering
  - publisher confirms internos
- Fonte base: F1, F8 no dump

### Contadores avançados de quorum queues

- Motivo: importantes para RabbitMQ 4.3, mas específicos demais para o escopo intermediário.
- Por que não deve aparecer no HTML: invadiria o node avançado.
- Aliases bloqueados no HTML:
  - x-delivery-count
  - x-acquired-count
  - acquired-count
  - delivery-count
- Fonte base: F8 no dump

### Overflow detalhado

- Motivo: necessário para capacidade e comportamento de filas, não para o modelo conceitual de DLX.
- Por que não deve aparecer no HTML: o node só precisa dizer que queue length limit pode dead-letter mensagens.
- Aliases bloqueados no HTML:
  - reject-publish-dlx
  - reject-publish
  - drop-head
- Fonte base: F4 no dump

## Conceitos Reservados a Nodes Futuros

### Governança detalhada de policies

- Node responsável: Policies, x-arguments e permissões
- Node ID responsável, quando existir: intermediario/05-policies-x-arguments-e-permissoes
- Menção permitida no HTML atual: curta como handoff final e nota de preferência por policies
- Aliases bloqueados:
  - operator policies
  - precedência de policy
  - prioridade da policy
- Condição de exceção: o label do próximo node pode aparecer no contexto de posição

### Publisher confirms em profundidade

- Node responsável: Publisher confirms e confiabilidade
- Node ID responsável, quando existir: intermediario/07-publisher-confirms-e-confiabilidade
- Menção permitida no HTML atual: nenhuma ou curta como fronteira se necessário
- Aliases bloqueados:
  - confirmSelect
  - confirmação do publisher
  - publisher confirm
- Condição de exceção: títulos de fonte podem ser adaptados para não usar o termo visível

### Diagnóstico operacional de DLX

- Node responsável: Diagnóstico de roteamento e observabilidade
- Node ID responsável, quando existir: avancado/01-diagnostico-de-roteamento-e-observabilidade
- Menção permitida no HTML atual: curta como necessidade de observabilidade, sem ferramentas
- Aliases bloqueados:
  - dashboard
  - métrica de DLQ
  - tracing
  - Prometheus
- Condição de exceção: nenhuma

### Quorum queues avançadas

- Node responsável: Quorum queues, DLX e limites de redelivery
- Node ID responsável, quando existir: avancado/03-quorum-queues-dlx-e-redelivery-limits
- Menção permitida no HTML atual: curta como causa de delivery-limit
- Aliases bloqueados:
  - delayed retry nativo
  - Raft
  - quorum leader
  - redelivery limit avançado
- Condição de exceção: `delivery limit` pode aparecer como causa de dead-lettering

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| RabbitMQ: Dead Letter Exchanges | Dead Letter Exchange, DLX | sim | Documentação de Dead Letter Exchanges |
| RabbitMQ: Consumer Acknowledgements and Publisher Confirms | publisher confirms | sim, com adaptação | Documentação sobre acknowledgements de consumidor |
| RabbitMQ: Time-to-Live and Expiration | TTL, expiração | sim | Documentação de TTL e expiração |
| RabbitMQ: Queue Length Limit | queue length limit | sim | Documentação de limite de fila |
| RabbitMQ: Policies | policies | sim | Documentação de policies |
| RabbitMQ: Publishers | publishers, publicação sem rota | sim | Documentação de publishers |
| RabbitMQ: Alternate Exchanges | AE | sim, como fonte de fronteira | Documentação de Alternate Exchanges |
| RabbitMQ: Quorum Queues | quorum queues | sim, como fonte de fronteira | Documentação de quorum queues |
| RabbitMQ: Reliability Guide | reliability | sim, com adaptação | Guia de confiabilidade |
