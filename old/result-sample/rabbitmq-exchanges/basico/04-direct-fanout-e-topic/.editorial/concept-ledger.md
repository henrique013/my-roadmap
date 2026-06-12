# Concept ledger

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Level: `basico`
- Node: `04-direct-fanout-e-topic`
- Node ID: `basico/04-direct-fanout-e-topic`
- Data: 2026-06-08
- Fonte principal: `research-dump.md`, F1 a F6

## Conceitos Permitidos no HTML

### Tipo de exchange como regra de decisão

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum
- Primeira ocorrência permitida: abertura, desde que ligada ao fato herdado de que bindings já existem
- Explicação mínima exigida antes da primeira ocorrência: explicar que a mesma publicação pode ser avaliada de modos diferentes
- Aliases e paráfrases:
  - tipo da exchange
  - regra de decisão
  - regra de roteamento do tipo
  - como a exchange lê a key
- Termos relacionados que também exigem preparo:
  - direct
  - fanout
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
  - Comparar interpretação da key e dos bindings.
  - Conectar com o node anterior sem redefinir binding.
- Usos proibidos:
  - Abrir tipos especializados, plugins ou E2E.
- Fronteira com nodes futuros: tipos especializados e desenho arquitetural ficam para níveis posteriores.
- Fonte base: F1, F2.

### Direct exchange

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, apenas no título/label do node por contrato
- Primeira ocorrência permitida: título e contexto de posição; no corpo, depois da explicação de igualdade exata
- Explicação mínima exigida antes da primeira ocorrência: mostrar que a decisão compara a key enviada com a key registrada
- Aliases e paráfrases:
  - direct
  - exchange direct
  - troca direta
  - igualdade exata
  - match exato
- Termos relacionados que também exigem preparo:
  - binding key
  - routing key
  - multicast
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Explicar match exato.
  - Explicar entrega para múltiplas filas quando várias bindings têm a mesma key.
- Usos proibidos:
  - Tratar como garantia de destino único.
  - Reabrir default exchange como foco.
- Fronteira com nodes futuros: decisão arquitetural de usar direct em contratos fica para intermediário.
- Fonte base: F1, F2, F4.

### Fanout exchange

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, apenas no título/label do node por contrato
- Primeira ocorrência permitida: título e contexto de posição; no corpo, depois da necessidade de cópia para todos os destinos ligados
- Explicação mínima exigida antes da primeira ocorrência: mostrar que a publicação não precisa escolher por key e deve ser copiada para todos os destinos ligados
- Aliases e paráfrases:
  - fanout
  - exchange fanout
  - broadcast
  - cópia para todos
  - todos os destinos ligados
- Termos relacionados que também exigem preparo:
  - routing key ignorada
  - destinos ligados
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Explicar broadcast por filas ou destinos ligados.
  - Contrastar com filtro por categoria.
- Usos proibidos:
  - Confundir com competição de consumidores em uma fila.
  - Usar como sinônimo de "todos os consumidores do sistema".
- Fronteira com nodes futuros: broadcast versus consumidores competindo será aprofundado depois.
- Fonte base: F1, F2, F3.

### Topic exchange

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, apenas no título/label do node por contrato
- Primeira ocorrência permitida: título e contexto de posição; no corpo, depois da necessidade de escolher por segmentos
- Explicação mínima exigida antes da primeira ocorrência: explicar que a key pode carregar partes separadas por ponto e que o binding registra um padrão
- Aliases e paráfrases:
  - topic
  - exchange topic
  - roteamento por padrão
  - padrão por segmentos
  - routing pattern
- Termos relacionados que também exigem preparo:
  - segmento
  - wildcard
  - `*`
  - `#`
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Explicar match por segmentos.
  - Mostrar relação com direct quando não há wildcards.
- Usos proibidos:
  - Virar guia de naming convention.
  - Ser tratado como sempre melhor que direct.
- Fronteira com nodes futuros: contratos de nomes e governança ficam para outros nodes.
- Fonte base: F1, F5, F6.

### Wildcard `*`

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não, salvo em snippet imediatamente acompanhado de explicação
- Primeira ocorrência permitida: seção topic, depois de explicar segmento
- Explicação mínima exigida antes da primeira ocorrência: explicar que um pedaço da key pode variar ocupando exatamente uma posição
- Aliases e paráfrases:
  - `*`
  - asterisco
  - star
  - wildcard de um segmento
  - exatamente um segmento
- Termos relacionados que também exigem preparo:
  - segmento
  - routing pattern
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Explicar `audit.*.login`.
- Usos proibidos:
  - Dizer que cobre zero ou vários segmentos.
- Fronteira com nodes futuros: não transformar em convenção de nomes.
- Fonte base: F1, F5, F6.

### Wildcard `#`

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não, salvo em snippet imediatamente acompanhado de explicação
- Primeira ocorrência permitida: seção topic, depois de `*`
- Explicação mínima exigida antes da primeira ocorrência: explicar que o restante da key pode ter zero ou mais segmentos
- Aliases e paráfrases:
  - `#`
  - cerquilha
  - hash
  - wildcard amplo
  - zero ou mais segmentos
- Termos relacionados que também exigem preparo:
  - segmento
  - fanout
  - padrão amplo
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Explicar `audit.#`.
  - Mostrar risco de amplitude.
- Usos proibidos:
  - Usar como curinga genérico recomendável sem limite.
- Fronteira com nodes futuros: diagnóstico de volume e governança ficam fora.
- Fonte base: F1, F5, F6.

### Broadcast

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum depois de explicar cópia para todos
- Primeira ocorrência permitida: seção fanout
- Explicação mínima exigida antes da primeira ocorrência: publicação copiada para todos os destinos ligados
- Aliases e paráfrases:
  - broadcast
  - publicar para todos
  - cópia ampla
  - todos recebem uma cópia
- Termos relacionados que também exigem preparo:
  - fanout
  - destinos ligados
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Nomear a intenção de fanout.
- Usos proibidos:
  - Explicar competição de consumidores.
- Fronteira com nodes futuros: consumidores competindo fica para outro node.
- Fonte base: F2, F3.

### Multicast em direct

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, depois da explicação de direct
- Primeira ocorrência permitida: depois de direct e da ideia de múltiplas bindings iguais
- Explicação mínima exigida antes da primeira ocorrência: várias filas podem ter bindings com a mesma key
- Aliases e paráfrases:
  - multicast
  - mais de uma fila com a mesma key
  - várias filas recebem por match exato
- Termos relacionados que também exigem preparo:
  - direct
  - binding key
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Corrigir a leitura de cardinalidade única.
- Usos proibidos:
  - Abrir desenho arquitetural completo.
- Fronteira com nodes futuros: contratos e broadcast versus competição ficam depois.
- Fonte base: F2, F4.

### Binding key e routing key herdadas

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como pré-requisito herdado do node 03
- Primeira ocorrência permitida: abertura
- Explicação mínima exigida antes da primeira ocorrência: não precisa redefinir; basta usar como base herdada
- Aliases e paráfrases:
  - binding key
  - routing key
  - key da publicação
  - key registrada no binding
- Termos relacionados que também exigem preparo:
  - direct
  - topic
- Pode aparecer em:
  - título: não
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - Comparar como direct e topic usam a key.
  - Dizer que fanout ignora a routing key.
- Usos proibidos:
  - Redefinir todo o node 03.
- Fronteira com nodes futuros: E2E e diagnostics não entram.
- Fonte base: node 03, F1, F2.

## Conceitos Permitidos Só no Dump

### Unroutable

- Motivo: ajuda a registrar que mensagens sem match existem, mas não é escopo do HTML.
- Por que não deve aparecer no HTML: tratamento de mensagens sem rota pertence ao intermediário.
- Aliases bloqueados no HTML:
  - unroutable
  - mandatory
  - return
  - alternate exchange
  - AE
- Fonte base: F1, F2.

### Exchange-to-exchange bindings

- Motivo: F1 menciona destino exchange, mas o node básico não deve carregar topologia composta.
- Por que não deve aparecer no HTML: composição avançada está bloqueada para o básico.
- Aliases bloqueados no HTML:
  - exchange-to-exchange
  - E2E
  - destination exchange
  - source exchange composta
- Fonte base: F1.

## Conceitos Reservados a Nodes Futuros

### Roteamento por atributos da próxima etapa

- Node responsável: Headers exchange e metadados de roteamento
- Node ID responsável, quando existir: `basico/05-headers-e-metadados-de-roteamento`
- Menção permitida no HTML atual: curta como contexto de posição e handoff final
- Aliases bloqueados:
  - x-match
  - all-with-x
  - any-with-x
  - metadados como critério principal
- Condição de exceção: o label do próximo node pode aparecer no contexto de posição porque é exigido pela navegação.

### Dead-letter e retry

- Node responsável: Dead Letter Exchanges e retry conceitual
- Node ID responsável, quando existir: `intermediario/04-dead-letter-exchanges-e-retry-conceitual`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - DLX
  - dead-letter
  - retry
  - redelivery
- Condição de exceção: nenhuma.

### Governança e policies

- Node responsável: Policies, x-arguments e permissões
- Node ID responsável, quando existir: `intermediario/05-policies-x-arguments-e-permissoes`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - policy
  - policies
  - permission
  - permissão
  - permissões
  - x-arguments
- Condição de exceção: nenhuma.

### Tipos especializados

- Node responsável: Tipos especializados e plugins
- Node ID responsável, quando existir: `avancado/02-tipos-especializados-e-plugins`
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - plugin
  - plugins
  - local random
  - modulus hash
  - consistent hashing
- Condição de exceção: nenhuma.

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Exchanges | sim | RabbitMQ - Exchanges |
| F2 | AMQP 0-9-1, Model | sim | RabbitMQ - Modelo AMQP 0-9-1 |
| F3 | Publish/Subscribe | sim, após fanout | Tutorial oficial de publish/subscribe |
| F4 | Routing | sim | Tutorial oficial de roteamento |
| F5 | Topics | sim, após topic | Tutorial oficial de tópicos |
| F6 | AMQP 0-9 specification | sim | Especificação AMQP 0-9 |

