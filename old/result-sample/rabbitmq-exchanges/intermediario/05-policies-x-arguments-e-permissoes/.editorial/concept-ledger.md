# Concept ledger

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Level: intermediario
- Node: Policies, x-arguments e permissões
- Node ID: intermediario/05-policies-x-arguments-e-permissoes
- Data: 2026-06-10
- Fonte principal: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/05-policies-x-arguments-e-permissoes/research-dump.md`

## Conceitos Permitidos no HTML

### Policy

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, no título principal e no contexto do node; no corpo, somente depois da situação de mudança operacional
- Primeira ocorrência permitida: título principal e, depois, primeiro bloco narrativo que mostra uma regra por vhost aplicada a várias filas
- Explicação mínima exigida antes da primeira ocorrência: no corpo, regra por vhost que casa recursos por nome e aplica argumentos opcionais a grupos de filas ou exchanges
- Aliases e paráfrases:
  - policy
  - policies
  - política
  - políticas
  - regra de policy
  - regra por vhost
- Termos relacionados que também exigem preparo:
  - pattern
  - apply-to
  - prioridade de policy
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar configuração alterável em runtime para grupos de recursos
  - aplicar DLX ou TTL como exemplo já conhecido
  - explicar casamento por nome e tipo de recurso
- Usos proibidos:
  - prometer mudança de qualquer argumento
  - substituir ownership de topologia
  - virar sequência de comandos
- Fronteira com nodes futuros: governança ampla fica no nível avançado
- Fonte base: F1

### X-argument

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, no título principal; no corpo, somente depois de explicar argumento opcional enviado na declaração do recurso
- Primeira ocorrência permitida: título principal e bloco de contraste entre declaração da aplicação e regra operacional
- Explicação mínima exigida antes da primeira ocorrência: argumento opcional fornecido pelo cliente ao declarar fila ou exchange
- Aliases e paráfrases:
  - x-argument
  - x-arguments
  - optional argument
  - optional arguments
  - argumento opcional
  - argumentos opcionais
  - argumento do cliente
  - argumentos do cliente
  - client-provided argument
  - client-provided arguments
- Termos relacionados que também exigem preparo:
  - declaração de fila
  - argumento hardcoded
- Pode aparecer em:
  - título: sim
  - lead: sim
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - mostrar configuração presa ao ciclo de vida da declaração
  - explicar precedência contra policy comum
  - usar `dead-letter-exchange` como exemplo mínimo
- Usos proibidos:
  - listar todos os argumentos opcionais
  - usar como sinônimo de qualquer configuração do broker
- Fronteira com nodes futuros: quorum queues e limites avançados ficam em node avançado
- Fonte base: F1, F3, F4

### Runtime parameter

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois que policy já foi explicada como configuração mantida no broker
- Explicação mínima exigida antes da primeira ocorrência: parâmetro alterável em operação, armazenado pelo broker
- Aliases e paráfrases:
  - runtime parameter
  - runtime parameters
  - parâmetro em runtime
  - parâmetros em runtime
  - parâmetro de runtime
  - parâmetros de runtime
  - parâmetro dinâmico
- Termos relacionados que também exigem preparo:
  - vhost-scoped parameter
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - situar policy no modelo de configuração do RabbitMQ
- Usos proibidos:
  - abrir federation, shovel ou parâmetros globais
- Fronteira com nodes futuros: federation fica no nível avançado
- Fonte base: F5

### Operator policy

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: após policy comum e após a necessidade de guardrail ser mostrada
- Explicação mínima exigida antes da primeira ocorrência: policy de operador que limita ou protege valores definidos por aplicação ou policy comum
- Aliases e paráfrases:
  - operator policy
  - operator policies
  - política de operador
  - políticas de operador
  - guardrail do operador
  - guardrail operacional
- Termos relacionados que também exigem preparo:
  - guardrail
  - teto
  - valor efetivo
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar teto de proteção para parâmetros controlados por aplicação
  - fechar o raciocínio de precedência
- Usos proibidos:
  - tratar como priority comum
  - substituir desenho de contrato
- Fronteira com nodes futuros: governança ampla fica no nível avançado
- Fonte base: F1, F3

### Precedência

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de policy, x-argument e operator policy aparecerem como camadas possíveis
- Explicação mínima exigida antes da primeira ocorrência: regra que decide qual valor efetivo vale quando duas ou três camadas tentam controlar a mesma chave
- Aliases e paráfrases:
  - precedência
  - precedence
  - valor efetivo
  - camada vencedora
  - regra de autoridade
- Termos relacionados que também exigem preparo:
  - policy comum
  - operator policy
  - argumento do cliente
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar conflito de chave
  - mostrar por que hardcoded reduz flexibilidade
- Usos proibidos:
  - prometer uma regra idêntica para todo tipo de chave
- Fronteira com nodes futuros: conflitos organizacionais maiores ficam no avançado
- Fonte base: F3, F4

### Vhost

- Tipo: termo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar espaço lógico de recursos
- Explicação mínima exigida antes da primeira ocorrência: fronteira lógica onde nomes de recursos, policies e permissões valem
- Aliases e paráfrases:
  - vhost
  - vhosts
  - virtual host
  - virtual hosts
  - host virtual
  - hosts virtuais
  - fronteira lógica
- Termos relacionados que também exigem preparo:
  - recurso nomeado
  - escopo por vhost
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar escopo de permissions e policies
  - mostrar que nomes iguais em vhosts diferentes são recursos diferentes
- Usos proibidos:
  - prometer isolamento físico
  - abrir fluxo entre vhosts
- Fronteira com nodes futuros: multi-vhost operacional e federation ficam fora
- Fonte base: F6, F2

### Permissões configure, write e read

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de recursos e vhost terem sido preparados
- Explicação mínima exigida antes da primeira ocorrência: configure cria ou altera recurso; write injeta mensagem; read recupera mensagem
- Aliases e paráfrases:
  - configure
  - write
  - read
  - configure permission
  - write permission
  - read permission
  - permissão configure
  - permissão write
  - permissão read
  - permissões de recurso
  - permission regex
- Termos relacionados que também exigem preparo:
  - resource permission
  - exchange
  - queue
- Pode aparecer em:
  - título: sim
  - lead: sim, se a frase já explicar autoridade
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - mapear declaração, publicação, binding e consumo
  - explicar permissões envolvidas em DLX
- Usos proibidos:
  - virar guia completo de segurança
  - abrir autenticação, tags e backends
- Fronteira com nodes futuros: hardening completo fora do recorte
- Fonte base: F2, F4

## Conceitos Permitidos Só no Dump

### Declaração passiva

- Motivo: nota temporal de RabbitMQ 4.3.1.
- Por que não deve aparecer no HTML: desviaria da narrativa principal para detalhe de verificação de existência.
- Aliases bloqueados no HTML:
  - passive declaration
  - passive declarations
  - declaração passiva
  - declarações passivas
- Fonte base: F2

### User tags e backends de autenticação

- Motivo: pertencem a guia completo de segurança, fora do escopo deste node.
- Por que não deve aparecer no HTML: a página deve tratar permissões de recursos, não autenticação completa.
- Aliases bloqueados no HTML:
  - user tags
  - tags de usuário
  - LDAP
  - OAuth
  - backend de autorização
  - backend de autenticação
- Fonte base: F2

## Conceitos Reservados a Nodes Futuros

### Composição local entre exchanges

- Node responsável: Exchange-to-exchange bindings
- Node ID responsável, quando existir: intermediario/06-exchange-to-exchange-bindings
- Menção permitida no HTML atual: curta como handoff final e no contexto de posição
- Aliases bloqueados:
  - E2E binding
  - E2E bindings
  - exchange.bind
  - roteamento transitivo
  - topologia transitiva
- Condição de exceção: nome do próximo node no bloco de posição ou handoff final

### Publisher confirms

- Node responsável: Publisher confirms e confiabilidade
- Node ID responsável, quando existir: intermediario/07-publisher-confirms-e-confiabilidade
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - publisher confirm
  - publisher confirms
  - confirmação de publicação
  - confirmações de publicação
- Condição de exceção: nenhuma

### Diagnóstico operacional

- Node responsável: Diagnóstico de roteamento e observabilidade
- Node ID responsável, quando existir: avancado/01-diagnostico-de-roteamento-e-observabilidade
- Menção permitida no HTML atual: nenhuma
- Aliases bloqueados:
  - métricas de unroutable
  - tracing
  - firehose
  - observabilidade de roteamento
- Condição de exceção: nenhuma

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Policies | Sim | RabbitMQ - policies |
| F2 | Authentication, Authorisation, Access Control | Sim | RabbitMQ - permissões de recursos |
| F3 | Exchanges | Sim | RabbitMQ - exchanges e precedência de argumentos |
| F4 | Dead Letter Exchanges | Sim | RabbitMQ - configuração de DLX |
| F5 | Runtime Parameters | Sim, depois de preparar o termo | RabbitMQ - runtime parameters |
| F6 | Virtual Hosts | Sim, depois de preparar o termo | RabbitMQ - virtual hosts |
