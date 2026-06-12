# Concept ledger

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Level: intermediario
- Node: Exchange-to-exchange bindings
- Node ID: intermediario/06-exchange-to-exchange-bindings
- Data: 2026-06-11
- Fonte principal: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/06-exchange-to-exchange-bindings/research-dump.md`

## Conceitos Permitidos no HTML

### Exchange-to-exchange binding

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, no título e no contexto do node; no corpo, somente depois da situação de composição entre exchanges
- Primeira ocorrência permitida: abertura e primeiro bloco narrativo que mostra uma exchange apontando para outra exchange
- Explicação mínima exigida antes da primeira ocorrência: binding cujo destino é outra exchange, não fila
- Aliases e paráfrases:
  - exchange-to-exchange binding
  - exchange-to-exchange bindings
  - E2E
  - E2E binding
  - E2E bindings
  - binding entre exchanges
  - vínculo entre exchanges
- Termos relacionados que também exigem preparo:
  - source exchange
  - destination exchange
  - roteamento transitivo
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar composição local de roteamento
  - nomear a aresta source -> destination
  - contrastar com republicação manual, depois de preparar o modelo
- Usos proibidos:
  - tratar como mecanismo entre clusters
  - substituir contrato simples sem critério
  - virar roteiro de client library
- Fronteira com nodes futuros: federation e governança ampla ficam no avançado
- Fonte base: F1, F2

### Source exchange

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois que a direção da aresta for descrita
- Explicação mínima exigida antes da primeira ocorrência: exchange de onde a mensagem sai no vínculo E2E
- Aliases e paráfrases:
  - source
  - source exchange
  - exchange fonte
  - origem
- Termos relacionados que também exigem preparo:
  - destination exchange
  - `exchange.bind`
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - orientar direção do fluxo
  - explicar permissões do binding
  - interpretar métricas
- Usos proibidos:
  - usar como sinônimo de publisher
  - abrir publisher confirms
- Fronteira com nodes futuros: confiabilidade do publisher fica no próximo node
- Fonte base: F1

### Destination exchange

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: junto da explicação da direção source -> destination
- Explicação mínima exigida antes da primeira ocorrência: exchange alcançada pela source e que continua roteando
- Aliases e paráfrases:
  - destination
  - destination exchange
  - exchange destino
  - destino
- Termos relacionados que também exigem preparo:
  - métrica de ingress
  - roteamento transitivo
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar a segunda camada de roteamento
  - contrastar com fila final
  - explicar a métrica de ingress
- Usos proibidos:
  - tratar como fila
  - tratar como cluster remoto
- Fronteira com nodes futuros: topologia entre clusters fica no avançado
- Fonte base: F1, F2

### `exchange.bind`

- Tipo: função
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de source e destination estarem claros
- Explicação mínima exigida antes da primeira ocorrência: método que cria o binding entre duas exchanges
- Aliases e paráfrases:
  - exchange.bind
  - método de binding de exchange para exchange
  - operação de binding entre exchanges
- Termos relacionados que também exigem preparo:
  - configure na destination exchange
  - write na source exchange
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: não
- Usos permitidos:
  - mostrar forma conceitual mínima
  - conectar com permissões de topologia
- Usos proibidos:
  - aparecer como comando executável
  - abrir exemplos Java ou .NET
- Fronteira com nodes futuros: automação de topologia não é tema do roadmap
- Fonte base: F1, F3

### Roteamento transitivo

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de uma mensagem atravessar source e destination exchanges no exemplo
- Explicação mínima exigida antes da primeira ocorrência: mensagem pode atravessar exchanges encadeadas por bindings até chegar a filas
- Aliases e paráfrases:
  - roteamento transitivo
  - transitive topology
  - topologia transitiva
  - rota transitiva
  - caminhos transitivos
- Termos relacionados que também exigem preparo:
  - detecção de ciclos
  - cópia única por fila
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar composition sem republicação
  - preparar cycle detection
- Usos proibidos:
  - usar como sinônimo de replicação
  - abrir detalhes de algoritmo interno
- Fronteira com nodes futuros: diagnóstico de grafos fica no avançado
- Fonte base: F1, F2

### Detecção de ciclos

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de roteamento transitivo estar claro
- Explicação mínima exigida antes da primeira ocorrência: RabbitMQ elimina loops durante a entrega para evitar ciclo infinito
- Aliases e paráfrases:
  - cycle detection
  - detecção de ciclos
  - ciclos eliminados
  - ciclo eliminado
  - loop eliminado
- Termos relacionados que também exigem preparo:
  - cópia única por fila
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar proteção do broker
  - mostrar que proteção não é convite para grafo opaco
- Usos proibidos:
  - vender ciclos como desenho recomendado
  - detalhar algoritmo interno
- Fronteira com nodes futuros: governança ampla de complexidade fica no avançado
- Fonte base: F1

### Métrica de ingress da exchange destino

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que E2E não republica
- Explicação mínima exigida antes da primeira ocorrência: contador de entrada da destination exchange não sobe por E2E porque não há nova publicação nela
- Aliases e paráfrases:
  - ingress metric
  - métrica de ingress
  - taxa de entrada
  - inbound message rate
  - contador de entrada
  - métrica de entrada
- Termos relacionados que também exigem preparo:
  - republicação
  - target queues
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - evitar leitura errada de sinal operacional
  - apontar para filas finais como sinais atualizados
- Usos proibidos:
  - abrir troubleshooting completo
  - transformar em aula de observabilidade
- Fronteira com nodes futuros: diagnóstico operacional fica no avançado
- Fonte base: F2

## Conceitos Permitidos Só no Dump

### Federation

- Motivo: fronteira explícita com node avançado.
- Por que não deve aparecer no HTML: a página deve evitar ensinar multi-cluster ou WAN neste node.
- Aliases bloqueados no HTML:
  - federation
  - federated exchange
  - federated exchanges
  - federação
  - exchange federada
  - exchanges federadas
  - WAN
  - multi-cluster
  - cluster remoto
- Fonte base: F6

## Conceitos Reservados a Nodes Futuros

### Confiabilidade do próximo node

- Node responsável: Publisher confirms e confiabilidade
- Node ID responsável, quando existir: intermediario/07-publisher-confirms-e-confiabilidade
- Menção permitida no HTML atual: curta como handoff final, sem explicação
- Aliases bloqueados:
- Condição de exceção: só no contexto de "próximo node".

### Diagnóstico de roteamento

- Node responsável: Diagnóstico de roteamento e observabilidade
- Node ID responsável, quando existir: avancado/01-diagnostico-de-roteamento-e-observabilidade
- Menção permitida no HTML atual: nenhuma, exceto leitura pontual da métrica de ingress
- Aliases bloqueados:
  - troubleshooting
  - diagnóstico completo
  - investigation
  - investigação operacional
- Condição de exceção: não se aplica.

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Exchange to Exchange Bindings | sim | RabbitMQ - Exchange to Exchange Bindings |
| F2 | Exchanges | sim | RabbitMQ - exchanges |
| F3 | Access Control | sim | RabbitMQ - permissões de recursos |
| F4 | Virtual Hosts | sim | RabbitMQ - virtual hosts |
| F5 | Publishers | sim | RabbitMQ - publishers |
| F6 | Federated Exchanges | não | manter só no dump |
