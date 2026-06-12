# Research dump - Policies, x-arguments e permissões

## Metadados do Node

- Roadmap de origem: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: intermediario
- `node_id`: `intermediario/05-policies-x-arguments-e-permissoes`
- Slug do node: `05-policies-x-arguments-e-permissoes`
- Label do node: Policies, x-arguments e permissões
- Posição numérica local no nível: 05 de 07
- Node anterior e próximo do mesmo nível para incrementalidade: anterior `intermediario/04-dead-letter-exchanges-e-retry-conceitual`; próximo `intermediario/06-exchange-to-exchange-bindings`
- Node anterior e próximo na sequência global do roadmap: anterior `intermediario/04-dead-letter-exchanges-e-retry-conceitual`; próximo `intermediario/06-exchange-to-exchange-bindings`
- Data da pesquisa: 2026-06-10
- Observações temporais: a pesquisa usou documentação oficial RabbitMQ versão 4.3. O detalhe temporal relevante é RabbitMQ 4.3.1: declarações passivas passaram a exigir ao menos uma permissão no recurso alvo. Esse ponto entra como nota de precisão, não como eixo narrativo.

## Contrato Extraído do Roadmap

- Papel do node na corrente: mostra como configurações de exchange e fila devem ser governadas para evitar redeploy e conflitos de autoridade.
- Papel do nível no roadmap tri-level: arquitetura, relações, decisões e trade-offs.
- Pré-requisitos herdados:
  - Entender AE, DLX e argumentos opcionais como configurações de topologia.
  - Entender que exchange roteia, fila armazena e bindings ligam recursos dentro de um vhost.
  - Entender que o node anterior já separou DLX de AE; este node usa DLX e AE apenas como exemplos de configuração governada.
- O que introduz pela primeira vez:
  - Policies.
  - Operator policies.
  - `x-arguments`.
  - Precedência.
  - Permissões configure/write/read.
  - Virtual host.
- Deve cobrir:
  - Explicar por que policies servem para parâmetros que podem mudar em runtime.
  - Comparar policy versus argumento hardcoded na declaração por cliente.
  - Descrever precedência entre argumentos, policies e operator policies em nível conceitual.
  - Relacionar permissões de configure, write e read à declaração, publicação, binding e DLX.
  - Mostrar vhost como fronteira de isolamento de topologia.
- Não deve cobrir:
  - Não virar guia completo de segurança.
  - Não reensinar DLX/AE; usar como exemplos de configuração.
  - Não tratar policies como solução para qualquer propriedade imutável.
- Perguntas do node:
  - Por que hardcoded x-arguments dificultam mudança de DLX?
  - Que permissão o publisher precisa para publicar em uma exchange?
  - Como vhost e permission regex protegem domínios de eventos?
- Vocabulário conceitual:
  - policy.
  - operator policy.
  - `x-argument`.
  - runtime parameter.
  - vhost.
  - configure permission.
  - write permission.
  - read permission.
- Exemplos e diagramas permitidos:
  - Cenário conceitual de policy aplicando DLX a um grupo de filas `orders.*`.
  - Matriz de ownership: app declara fila, plataforma aplica policy, publisher escreve em exchange.
- Armadilhas:
  - Embedar configuração operacional em código quando policy seria mais flexível.
  - Achar que policy muda qualquer argumento a qualquer momento.
  - Dar write amplo demais em exchanges de outros domínios.
- Critério de domínio: consegue diferenciar configuração declarada pela aplicação, policy operacional e permissão necessária para publicar ou configurar topologia.
- Handoff: com governança local clara, o próximo node mostra composição de topologias com exchange-to-exchange bindings.
- Referências específicas do contrato:
  - F10 `https://www.rabbitmq.com/docs/policies`: policies como mecanismo declarativo por vhost.
  - F11 `https://www.rabbitmq.com/docs/access-control`: autorização, vhosts e permissões.
  - F1 `https://www.rabbitmq.com/docs/exchanges`: precedência de argumentos e policies em exchanges.
  - F7 `https://www.rabbitmq.com/docs/dlx`: recomendação de policies para DLX.

## Matriz Anti-Repetição Aplicável

| Conteúdo | Decisão para este node |
|---|---|
| Exchange como roteador, não armazenamento | Tratar como pré-requisito. Não redefinir exchange. |
| Bindings e routing keys | Usar apenas quando explicar que configurar uma fila ou binding exige permissão no recurso certo. |
| AE e DLX como problemas diferentes | Usar como exemplos de configuração já conhecidos. Não reensinar a diferença. |
| Policies e x-arguments | Este node é a primeira introdução canônica. Pode nomear e explicar em profundidade conceitual. |
| Composição avançada de topologia | Reservada para `intermediario/06-exchange-to-exchange-bindings`; não abrir E2E. |
| Governança ampla e limites de complexidade | Reservada para `avancado/05-governanca-e-limites-de-complexidade`; aqui o foco é autoridade local de configuração e permissões. |

Exemplos que não devem ser repetidos:

- Não repetir o fluxo de mensagem inválida para fila de quarentena como centro do node anterior.
- Não repetir tabela de causas de dead-lettering.
- Não repetir o exemplo de migração de routing key do node de AE.
- Não transformar permissões em checklist operacional completo.

Definições que podem ser tratadas como pré-requisito:

- DLX é exchange normal configurada na fila.
- AE é fallback quando uma exchange não encontra rota.
- Fila e exchange são recursos nomeados dentro de vhost.
- Publisher publica em exchange; consumers leem de filas.

Termos que precisam ser introduzidos antes do uso visível:

- policy.
- operator policy.
- `x-argument`.
- runtime parameter.
- vhost.
- permissões configure, write e read.
- precedência.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/policies  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: base principal para policies, operator policies, x-arguments, escopo por vhost, prioridade, update em runtime e limites do que policy pode configurar.  
Tópicos cobertos: policies, runtime parameters, optional arguments, apply-to, prioridade, conflitos, operator policies, update de policies.  
Limites da fonte: contém exemplos de comandos; o HTML não deve transformar esses exemplos em roteiro de execução.

ID: F2  
URL: https://www.rabbitmq.com/docs/access-control  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3, com nota específica de RabbitMQ 4.3.1 sobre declarações passivas.  
Motivo de uso: sustentar a semântica de configure, write e read e a tabela de operações AMQP 0-9-1.  
Tópicos cobertos: autenticação, autorização, vhost, recursos, configure, write, read, permissões para `exchange.declare`, `queue.declare`, `basic.publish`, `queue.bind`, `exchange.bind`, DLX e AE.  
Limites da fonte: usada para permissões de recursos, não como guia completo de hardening ou autenticação.

ID: F3  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustentar a precedência entre `x-arguments`, policies e operator policies no contexto de exchanges.  
Tópicos cobertos: optional arguments, policy-defined key precedence, operator policies, exchanges e fronteira com E2E.  
Limites da fonte: E2E aparece apenas como próximo node; este dump usa a fonte para precedência.

ID: F4  
URL: https://www.rabbitmq.com/docs/dlx  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustentar o exemplo de DLX governada por policy e a recomendação contra x-arguments hardcoded.  
Tópicos cobertos: `dead-letter-exchange`, `dead-letter-routing-key`, policy vs optional arguments, precedência para DLX, permissões verificadas na declaração da fila.  
Limites da fonte: DLX é exemplo de configuração; não reabrir o modelo completo de dead-lettering.

ID: F5  
URL: https://www.rabbitmq.com/docs/parameters  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustentar que policies são exemplo de runtime parameters e que alguns parâmetros são vinculados a vhost.  
Tópicos cobertos: runtime parameters, parâmetros por vhost, parâmetros globais, atualização fora do arquivo de configuração principal.  
Limites da fonte: não é uma referência detalhada de policies; complementa F1.

ID: F6  
URL: https://www.rabbitmq.com/docs/vhosts  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustentar vhost como agrupamento lógico e fronteira de permissões, resources, policies e bindings.  
Tópicos cobertos: vhost, separação lógica, escopo de permissões, recursos dentro do vhost, conexão de cliente.  
Limites da fonte: não tratar vhost como isolamento físico de recursos.

## Síntese por Fonte

- F1 permite afirmar que policies são um mecanismo declarativo e escopado por vhost para ajustar argumentos opcionais de filas, exchanges, streams e alguns plugins. Também sustenta que policies existem para propriedades que podem mudar em runtime e que nem todo argumento cabe em policy.
- F2 permite afirmar que RabbitMQ verifica permissões de recursos dentro de um vhost e distingue configure, write e read. A mesma fonte liga operações AMQP 0-9-1 a recursos específicos: declarar exchange exige configure na exchange; publicar exige write na exchange; consumir exige read na fila; declarar fila com DLX exige configure na fila, read na fila e write na DLX.
- F3 permite afirmar que, quando a mesma chave vem de `x-arguments` e de policy, o argumento do cliente prevalece; operator policy funciona como guardrail acima das duas fontes, com regra especial para valores numéricos.
- F4 permite usar DLX como exemplo concreto: a documentação recomenda policy para `dead-letter-exchange` e desencoraja `x-arguments` hardcoded por exigirem redeploy ou redeclaração para mudar. Também sustenta a verificação de permissões na declaração da fila com DLX.
- F5 permite afirmar que policies são uma forma de runtime parameter e que runtime parameters podem ser por vhost ou globais.
- F6 permite afirmar que vhost é a fronteira lógica em que vivem exchanges, filas, bindings, permissões e policies. Permissões são por vhost, não globais por padrão.

## Afirmações Técnicas Importantes

Afirmação: `x-arguments` são argumentos opcionais enviados pelo cliente ao declarar filas ou exchanges.  
Base: F1, F3.  
Condição ou limite: alguns argumentos só podem ser definidos na declaração; policy não substitui propriedade imutável.  
Impacto didático: separa "configuração que nasce com o recurso" de "ajuste operacional por policy".

Afirmação: Policies foram criadas para configurar grupos de recursos por padrão declarativo e com mudança em runtime.  
Base: F1, F5.  
Condição ou limite: a policy precisa casar o nome e o tipo do recurso; se o pattern ou apply-to não casar, nada muda.  
Impacto didático: mostra por que `orders.*` pode receber uma regra comum sem redeploy dos produtores ou consumidores.

Afirmação: Nem todo argumento opcional pode ser controlado por policy.  
Base: F1.  
Condição ou limite: tipo de fila e prioridade máxima de classic queue são exemplos de valores fixos na declaração.  
Impacto didático: impede o erro de tratar policy como ferramenta universal.

Afirmação: Quando a mesma chave aparece em `x-arguments` e policy comum, o valor do argumento do cliente prevalece.  
Base: F3, F4.  
Condição ou limite: operator policy pode impor guardrail acima de ambos.  
Impacto didático: explica por que código com valor hardcoded pode impedir a mudança operacional pretendida.

Afirmação: Operator policies são guardrails de operador e podem limitar valores controlados por aplicação ou policy comum.  
Base: F1, F3.  
Condição ou limite: para valores numéricos, a documentação descreve uso do menor valor quando existe limite de operator policy.  
Impacto didático: permite explicar "plataforma impõe teto" sem virar guia de administração.

Afirmação: Um vhost agrupa recursos e define a fronteira onde permissões e policies são interpretadas.  
Base: F6, F2, F1.  
Condição ou limite: vhost é isolamento lógico, não garantia de isolamento físico de CPU, memória ou disco.  
Impacto didático: ajuda a entender por que a mesma exchange name pode existir em vhosts diferentes com permissões diferentes.

Afirmação: `configure`, `write` e `read` têm sentido operacional diferente: alterar/criar recurso, injetar mensagem e recuperar mensagem.  
Base: F2.  
Condição ou limite: a tabela oficial é por operação e protocolo; este node usa o recorte AMQP 0-9-1.  
Impacto didático: evita usar "permissão de RabbitMQ" como bloco único sem semântica.

Afirmação: Para publicar em uma exchange, o usuário precisa de `write` nessa exchange.  
Base: F2.  
Condição ou limite: a conexão já precisa estar autorizada no vhost.  
Impacto didático: conecta publisher a uma fronteira mínima de autorização.

Afirmação: Para declarar uma fila com DLX, o usuário precisa de configure na fila, read na própria fila e write na exchange de DLX.  
Base: F2, F4.  
Condição ou limite: as permissões são verificadas na declaração da fila.  
Impacto didático: mostra por que DLX não é só uma chave de configuração; ela aponta para outro recurso que também exige autoridade.

Afirmação: Declarações passivas têm regra específica a partir de RabbitMQ 4.3.1.  
Base: F2.  
Condição ou limite: basta ao menos uma permissão no recurso alvo, diferente da declaração não passiva que exige configure.  
Impacto didático: entra apenas como nota temporal para precisão, sem comandar a narrativa.

## Conceitos Essenciais

### Configuração declarada pelo cliente

- Nome técnico: optional arguments, `x-arguments`.
- Explicação em linguagem simples: pares chave-valor enviados na criação ou re-declaração do recurso para ligar uma capacidade opcional.
- Necessidade neste node: mostrar onde a aplicação coloca configurações quando declara fila ou exchange.
- Relação com conceitos anteriores: DLX e AE já apareceram como recursos configuráveis.
- Relação com conceitos futuros: alguns limites avançados de quorum queues podem usar argumentos ou policies.
- Risco de confusão: achar que todo argumento pode ser removido por policy depois.
- Fonte base: F1, F3, F4.

### Policy

- Nome técnico: policy.
- Explicação em linguagem simples: regra por vhost que casa recursos por nome e aplica um conjunto de argumentos opcionais a esses recursos.
- Necessidade neste node: dar uma forma operacional para "mudar um comportamento de grupo sem redeploy".
- Relação com conceitos anteriores: aplica DLX, AE, TTL e outros parâmetros já conhecidos ou citados.
- Relação com conceitos futuros: será usada como base de governança em nodes avançados.
- Risco de confusão: tratar policy como propriedade do código da aplicação.
- Fonte base: F1, F5.

### Operator policy

- Nome técnico: operator policy.
- Explicação em linguagem simples: regra de operador que impõe guardrails acima da configuração de aplicação e da policy comum.
- Necessidade neste node: explicar a terceira camada de autoridade e a noção de teto operacional.
- Relação com conceitos anteriores: complementa a governança local de filas e exchanges.
- Relação com conceitos futuros: guarda relação com governança e limites de complexidade.
- Risco de confusão: achar que operator policy é apenas policy com prioridade maior.
- Fonte base: F1, F3.

### Precedência

- Nome técnico: precedence.
- Explicação em linguagem simples: regra que decide qual valor efetivo vale quando mais de uma fonte tenta configurar a mesma chave.
- Necessidade neste node: mostrar por que configuração hardcoded pode bloquear mudança por policy.
- Relação com conceitos anteriores: DLX pode vir de policy ou de argumento da fila.
- Relação com conceitos futuros: ajuda a entender conflitos de configuração.
- Risco de confusão: aplicar uma regra única para todos os tipos de valor e recurso.
- Fonte base: F3, F4.

### Virtual host

- Nome técnico: vhost.
- Explicação em linguagem simples: espaço lógico onde recursos, permissões e policies são interpretados.
- Necessidade neste node: localizar a fronteira de isolamento de topologia.
- Relação com conceitos anteriores: exchanges, filas e bindings existem dentro de um vhost.
- Relação com conceitos futuros: multi-vhost e multi-cluster não entram neste node.
- Risco de confusão: tratar vhost como isolamento físico.
- Fonte base: F6, F2.

### Permissões de recurso

- Nome técnico: configure, write, read.
- Explicação em linguagem simples: três tipos de autoridade sobre recurso: criar/alterar, injetar mensagem, ler mensagem.
- Necessidade neste node: conectar ownership de topologia a ações concretas.
- Relação com conceitos anteriores: publisher, consumer, queue, exchange e binding já foram apresentados.
- Relação com conceitos futuros: segurança completa e auditoria ficam fora do node.
- Risco de confusão: dar permissões amplas só para "fazer funcionar".
- Fonte base: F2.

## Relações Causais e Estruturais

| Relação | Condição | Consequência didática |
|---|---|---|
| Valor em `x-argument` de cliente vence policy comum | mesma chave aparece nos dois lugares | valor hardcoded reduz flexibilidade operacional |
| Operator policy impõe guardrail | operador define limite compatível | aplicação pode pedir menos, mas não ultrapassar o teto |
| Policy casa por pattern e apply-to | nome e tipo do recurso combinam | grupo de filas ou exchanges recebe a mesma definição |
| Vhost separa nomes e permissões | conexão entra em um vhost específico | a mesma exchange name em outro vhost é outro recurso |
| Publicar em exchange exige write | AMQP 0-9-1 `basic.publish` | publisher pode ser limitado ao domínio correto |
| Declarar fila com DLX exige permissões em fila e DLX | fila aponta para exchange de DLX | configuração de retry/quarentena cruza ownership de recursos |

## Exemplos Técnicos Possíveis

### Policy para grupo de filas `orders.*`

- Mudança mostrada: uma configuração de DLX deixa de estar acoplada à declaração de cada fila e passa a ser aplicada por regra de nome.
- Conceitos introduzidos: policy, pattern, apply-to, runtime parameter, precedência.
- Risco de escopo: pode virar comando `rabbitmqctl set_policy`; o HTML deve usar snippet conceitual curto, não sequência executável.
- Por que não vira laboratório: o exemplo mostra forma e autoridade, não pede execução.

### Matriz de ownership

- Mudança mostrada: app declara fila, plataforma aplica guardrail, publisher escreve em exchange, consumer lê fila.
- Conceitos introduzidos: configure/write/read, vhost, operator policy.
- Risco de escopo: pode virar guia de RBAC completo.
- Por que não vira laboratório: a matriz não usa nomes de usuário reais nem comandos.

### Precedência de fontes

- Mudança mostrada: mesma chave nasce em três camadas possíveis.
- Conceitos introduzidos: `x-argument`, policy, operator policy, valor efetivo.
- Risco de escopo: detalhes numéricos podem parecer tuning.
- Por que não vira laboratório: manter como fluxo conceitual de decisão.

## Obrigações de Concretização Didática

Conceito ou relação: diferença entre `x-argument` hardcoded e policy por grupo.  
Tipo de demanda: contraste.  
Primitiva visual escolhida: componente HTML/CSS.  
Justificativa da primitiva: o leitor precisa ver onde a mesma chave nasce e por que uma forma fica presa ao ciclo de vida da declaração.  
Exemplo candidato: `orders.created`, `orders.billing` e `orders.audit` recebendo `dead-letter-exchange` por uma policy de filas `orders.*`.  
Fonte: F1, F4.  
Por que a prosa pode não bastar: sem forma visual, "policy vs argumento" vira vocabulário abstrato.  
Risco de virar laboratório ou excesso: mostrar comando real de policy.  
Como manter conceitual e mínimo: usar snippet de pseudo-definição, sem prompt de shell e sem sequência.  
Fronteira com nodes futuros: não abrir diagnóstico, métricas ou E2E.

Conceito ou relação: precedência entre argumento do cliente, policy comum e operator policy.  
Tipo de demanda: ordem e fronteira.  
Primitiva visual escolhida: componente HTML/CSS com três camadas.  
Justificativa da primitiva: precedência é relação de autoridade, não lista de termos.  
Exemplo candidato: mesma chave de limite ou DLX aparece em camadas diferentes e resulta em valor efetivo.  
Fonte: F3, F4, F1.  
Por que a prosa pode não bastar: a ordem de autoridade é fácil de inverter.  
Risco de virar laboratório ou excesso: tentar listar todas as chaves de policy.  
Como manter conceitual e mínimo: usar poucas chaves exemplares e declarar que nem toda chave é elegível.  
Fronteira com nodes futuros: governança corporativa ampla fica no avançado.

Conceito ou relação: permissões configure/write/read por operação.  
Tipo de demanda: mapeamento.  
Primitiva visual escolhida: tabela.  
Justificativa da primitiva: a fonte oficial é uma tabela de operação para recurso, e a síntese por papel fica mais escaneável em tabela curta.  
Exemplo candidato: publisher, aplicação que declara fila, consumer e configuração de DLX.  
Fonte: F2, F4.  
Por que a prosa pode não bastar: os três verbos se parecem se ficarem em parágrafo.  
Risco de virar laboratório ou excesso: cobrir todos os comandos AMQP.  
Como manter conceitual e mínimo: escolher apenas operações relevantes ao roadmap de exchanges.  
Fronteira com nodes futuros: não abrir hardening, tags de usuário ou backend de autorização.

Conceito ou relação: vhost como fronteira lógica.  
Tipo de demanda: fronteira.  
Primitiva visual escolhida: componente HTML/CSS de duas áreas.  
Justificativa da primitiva: a mesma exchange name em dois vhosts precisa aparecer como dois recursos distintos.  
Exemplo candidato: `billing.events` em `prod.orders` e `prod.payments`.  
Fonte: F6, F2.  
Por que a prosa pode não bastar: "mesmo nome, recurso diferente" é relação espacial.  
Risco de virar laboratório ou excesso: explicar multi-tenant completo.  
Como manter conceitual e mínimo: mostrar vhost como caixa lógica e relacionar só a permissões e policies.  
Fronteira com nodes futuros: não abrir federation nem conexão entre vhosts.

## Riscos, Armadilhas e Erros Comuns

- Colocar `dead-letter-exchange` como argumento fixo na declaração de todas as filas e descobrir depois que mudar a DLX exige redeploy e re-declaração. Base: F1, F4.
- Achar que policy muda tudo; há argumentos que só fazem sentido na criação do recurso. Base: F1.
- Definir duas policies com mesma prioridade e pattern sobreposto e criar escolha não determinística. Base: F1.
- Dar `write` amplo em exchanges fora do domínio do publisher. Base: F2, F6.
- Declarar fila com DLX sem perceber que isso exige autoridade sobre a fila e sobre a exchange de DLX. Base: F2, F4.
- Confundir vhost com isolamento físico e prometer separação de recursos que a documentação não promete. Base: F6.
- Usar operator policy como substituto de ownership claro; ela é guardrail, não desenho de contrato. Base: inferência a partir de F1 e do contrato do roadmap.

## Limites e Fora de Escopo

Este node explica:

- quando preferir policy a `x-argument` hardcoded;
- o que muda quando existe operator policy;
- como pensar precedência;
- quais permissões importam para declarar, publicar, bindar, consumir e configurar DLX;
- por que vhost é fronteira de topologia e autorização.

Este node apenas menciona como fronteira:

- AE e DLX, sem reensinar seus fluxos;
- runtime parameters além de policies;
- declaração passiva em RabbitMQ 4.3.1;
- conflitos de policy como risco de governança.

Fica para outro node ou outro nível:

- E2E bindings: `intermediario/06-exchange-to-exchange-bindings`;
- publisher confirms: `intermediario/07-publisher-confirms-e-confiabilidade`;
- diagnóstico e observabilidade: `avancado/01-diagnostico-de-roteamento-e-observabilidade`;
- governança ampla e limites de complexidade: `avancado/05-governanca-e-limites-de-complexidade`;
- hardening completo, LDAP/OAuth, tags de usuário e backends de autorização: fora do recorte deste roadmap.

## Divergências, Versões e Notas Temporais

- O recorte principal é RabbitMQ 4.3. A documentação oficial exibe versão 4.3 e banner de disponibilidade dessa série.
- Em RabbitMQ 4.3.1, declarações passivas mudaram a exigência para "ao menos uma permissão" no recurso alvo. A página HTML pode mencionar esse detalhe apenas como nota de precisão se a narrativa precisar diferenciar declaração passiva e declaração que altera recurso.
- O comportamento de policy e operator policy é estável no recorte de RabbitMQ 4.3, mas chaves elegíveis por policy variam por recurso e por feature. O HTML deve evitar lista fechada de todas as chaves.

## Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| Policies, pattern, apply-to e prioridade | F1 | Base principal. |
| Runtime parameter | F1, F5 | Policy como exemplo prático. |
| `x-arguments` e limites | F1, F3, F4 | Usar só exemplos necessários. |
| Precedência | F3, F4, F1 | Operator policy como guardrail. |
| Permissões configure/write/read | F2 | Recorte AMQP 0-9-1. |
| DLX e permissões cruzadas | F2, F4 | Exemplo herdado do node anterior. |
| Vhost | F6, F2 | Fronteira lógica, não física. |

## Lacunas Pesquisadas e Resolvidas

Lacuna: Policy pode alterar qualquer argumento opcional?  
Busca feita: documentação oficial de policies e optional arguments.  
Fonte que resolveu: F1.  
Decisão: HTML deve afirmar que policies cobrem certos argumentos e features, mas não propriedades imutáveis como tipo de fila.

Lacuna: Qual camada vence entre policy e argumento do cliente?  
Busca feita: seção de precedência em exchanges e DLX.  
Fonte que resolveu: F3, F4.  
Decisão: explicar que argumento do cliente vence policy comum; operator policy age como guardrail acima.

Lacuna: Que permissão é necessária para publicar?  
Busca feita: tabela de permissões AMQP 0-9-1.  
Fonte que resolveu: F2.  
Decisão: publisher precisa de write na exchange dentro do vhost.

Lacuna: DLX adiciona exigência de permissão especial?  
Busca feita: documentação de DLX e access control.  
Fonte que resolveu: F2, F4.  
Decisão: incluir que declarar fila com DLX envolve configure/read na fila e write na exchange de DLX.

## Lacunas Remanescentes

Não há lacuna que bloqueie o HTML. A página deve preservar limites: não prometer que policies atualizam propriedades imutáveis, não transformar exemplos em comandos, não listar todo o modelo de segurança e não abrir E2E.

## Ordem de Introdução Conceitual

Conceito: configuração que muda sem redeploy.  
Necessidade: abrir a página com um problema observável: trocar DLX de várias filas `orders.*` sem alterar cada serviço.  
Explicação antes do nome: mostrar que uma mesma decisão pode estar presa ao código ou aplicada por regra externa.  
Nomeação: policy.  
Depende de: DLX e fila como pré-requisitos.  
Pode usar depois para: runtime parameter, pattern e apply-to.  
Não entrar ainda em: comandos de criação de policy.  
Visual possível: contraste policy vs declaração hardcoded.  
Fonte base: F1, F4.

Conceito: `x-argument`.  
Necessidade: explicar onde a aplicação embute a configuração quando declara recurso.  
Explicação antes do nome: "argumento opcional enviado junto da declaração".  
Nomeação: `x-argument`.  
Depende de: declaração de fila ou exchange.  
Pode usar depois para: precedência e rigidez operacional.  
Não entrar ainda em: lista completa de argumentos.  
Visual possível: snippet conceitual de uma declaração de fila com `dead-letter-exchange`.  
Fonte base: F1, F3, F4.

Conceito: runtime parameter.  
Necessidade: situar policy como configuração do broker que vive fora do código da aplicação.  
Explicação antes do nome: "valor armazenado no broker e alterável em operação".  
Nomeação: runtime parameter.  
Depende de: policy.  
Pode usar depois para: escopo por vhost.  
Não entrar ainda em: shovel, federation upstream e parâmetros globais.  
Visual possível: nenhum obrigatório; frase basta.  
Fonte base: F5, F1.

Conceito: operator policy.  
Necessidade: explicar que plataforma pode impor teto de segurança/capacidade.  
Explicação antes do nome: "camada de guardrail acima do pedido da aplicação".  
Nomeação: operator policy.  
Depende de: policy e precedência.  
Pode usar depois para: guardrail e valor efetivo.  
Não entrar ainda em: administração completa de operator policies.  
Visual possível: pilha de autoridade.  
Fonte base: F1, F3.

Conceito: precedência.  
Necessidade: resolver conflito de autoridade para a mesma chave.  
Explicação antes do nome: "quando três lugares tentam controlar a mesma peça, o broker precisa escolher um valor efetivo".  
Nomeação: precedência.  
Depende de: `x-argument`, policy e operator policy.  
Pode usar depois para: leitura correta de conflitos.  
Não entrar ainda em: todos os algoritmos por tipo de chave.  
Visual possível: camadas.  
Fonte base: F3, F4.

Conceito: vhost.  
Necessidade: localizar onde nomes, policies e permissões valem.  
Explicação antes do nome: "caixa lógica na qual os recursos existem".  
Nomeação: vhost.  
Depende de: recursos nomeados.  
Pode usar depois para: permissões por domínio.  
Não entrar ainda em: isolamento físico ou shovel entre vhosts.  
Visual possível: duas caixas lógicas.  
Fonte base: F6.

Conceito: configure/write/read.  
Necessidade: traduzir autorização em ações de topologia e publicação.  
Explicação antes do nome: "alterar recurso, injetar mensagem, recuperar mensagem".  
Nomeação: permissões configure, write e read.  
Depende de: vhost e recursos.  
Pode usar depois para: matriz de ownership.  
Não entrar ainda em: autenticação, tags e backends.  
Visual possível: tabela.  
Fonte base: F2.

## Insumos para o Ledger Editorial

Conceito: policy  
Tipo: termo  
Pode aparecer depois de: situação de mudança operacional em várias filas.  
Explicação mínima antes do nome: regra por vhost que casa nomes e aplica argumentos opcionais.  
Primeira nomeação permitida: após exemplo `orders.*` introduzir a necessidade.  
Aliases e paráfrases: policy, policies, política, políticas, regra de policy, regra por vhost.  
Pode ser usado depois para: runtime parameter, pattern, apply-to, atualização sem redeploy.  
Não usar para: qualquer propriedade imutável.  
Pode aparecer em título/lead/tabela/visual/referência: sim após preparação; no título principal sim porque é label canônico do node.  
Fronteira com nodes futuros: governança ampla fica no avançado.  
Fonte base: F1.

Conceito: `x-argument`  
Tipo: parâmetro  
Pode aparecer depois de: explicar declaração de recurso pelo cliente.  
Explicação mínima antes do nome: argumento opcional enviado na declaração.  
Primeira nomeação permitida: depois do contraste com configuração presa ao código.  
Aliases e paráfrases: x-argument, x-arguments, optional argument, argumento opcional, argumentos opcionais, argumento do cliente, client-provided argument.  
Pode ser usado depois para: precedência e rigidez.  
Não usar para: todo tipo de configuração do RabbitMQ.  
Pode aparecer em título/lead/tabela/visual/referência: sim após preparação; no título principal sim por label canônico.  
Fronteira com nodes futuros: delivery-limit e quorum queues avançadas ficam no avançado.  
Fonte base: F1, F3, F4.

Conceito: operator policy  
Tipo: termo  
Pode aparecer depois de: policy comum e conflito de autoridade.  
Explicação mínima antes do nome: policy de operador que impõe guardrail.  
Primeira nomeação permitida: na seção sobre camadas de autoridade.  
Aliases e paráfrases: operator policy, operator policies, política de operador, guardrail do operador.  
Pode ser usado depois para: teto, proteção, valor efetivo.  
Não usar para: priority comum.  
Pode aparecer em título/lead/tabela/visual/referência: sim após preparação.  
Fronteira com nodes futuros: governança ampla fica no avançado.  
Fonte base: F1, F3.

Conceito: runtime parameter  
Tipo: termo  
Pode aparecer depois de: policy explicada como configuração mantida no broker.  
Explicação mínima antes do nome: parâmetro alterável em operação, escopado por vhost quando aplicável.  
Primeira nomeação permitida: nota curta após policy.  
Aliases e paráfrases: runtime parameter, runtime parameters, parâmetro em runtime, parâmetro de runtime, parâmetro dinâmico.  
Pode ser usado depois para: situar policy.  
Não usar para: abrir shovel/federation.  
Pode aparecer em título/lead/tabela/visual/referência: referência sim; título principal não.  
Fronteira com nodes futuros: federation fica no avançado.  
Fonte base: F5.

Conceito: vhost  
Tipo: termo  
Pode aparecer depois de: explicar espaço lógico de recursos.  
Explicação mínima antes do nome: espaço lógico de recursos, permissões e policies.  
Primeira nomeação permitida: antes da matriz de permissões.  
Aliases e paráfrases: vhost, virtual host, virtual hosts, host virtual, fronteira lógica.  
Pode ser usado depois para: escopo de policy e autorização.  
Não usar para: isolamento físico.  
Pode aparecer em título/lead/tabela/visual/referência: sim após preparação.  
Fronteira com nodes futuros: multi-vhost operacional fica fora.  
Fonte base: F6.

Conceito: configure/write/read  
Tipo: papel  
Pode aparecer depois de: explicar operações sobre recursos.  
Explicação mínima antes do nome: criar/alterar, publicar/injetar, consumir/ler.  
Primeira nomeação permitida: na matriz de ownership.  
Aliases e paráfrases: configure permission, write permission, read permission, permissão configure, permissão write, permissão read, permissões de recurso.  
Pode ser usado depois para: publisher, declaração de fila, DLX, consumer.  
Não usar para: autenticação completa.  
Pode aparecer em título/lead/tabela/visual/referência: sim após preparação.  
Fronteira com nodes futuros: segurança completa fora do roadmap.  
Fonte base: F2.

Conceito permitido só no dump: passive declaration.  
Motivo: nota temporal específica de RabbitMQ 4.3.1.  
Por que não deve aparecer no HTML: desviaria da linha narrativa principal.  
Aliases bloqueados no HTML: passive declaration, declaração passiva, declarações passivas.  
Fonte base: F2.

Conceito reservado a nodes futuros: exchange-to-exchange binding.  
Node responsável: Exchange-to-exchange bindings.  
Node ID responsável: `intermediario/06-exchange-to-exchange-bindings`.  
Menção permitida no HTML atual: handoff final curto pelo label do próximo node.  
Aliases bloqueados: E2E binding, exchange.bind, roteamento transitivo, exchange-to-exchange.  
Condição de exceção: link de navegação ou nome do próximo node no contexto de posição.

Conceito reservado a nodes futuros: publisher confirms.  
Node responsável: Publisher confirms e confiabilidade.  
Node ID responsável: `intermediario/07-publisher-confirms-e-confiabilidade`.  
Menção permitida no HTML atual: nenhuma.  
Aliases bloqueados: publisher confirm, publisher confirms, confirmação de publicação.  
Condição de exceção: nenhuma.

Títulos de fontes e termos de referência:

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Policies | Sim | RabbitMQ - policies |
| F2 | Authentication, Authorisation, Access Control | Sim | RabbitMQ - permissões de recursos |
| F3 | Exchanges | Sim | RabbitMQ - exchanges e precedência de argumentos |
| F4 | Dead Letter Exchanges | Sim | RabbitMQ - configuração de DLX |
| F5 | Runtime Parameters | Sim, depois de preparar runtime parameter | RabbitMQ - runtime parameters |
| F6 | Virtual Hosts | Sim, depois de preparar vhost | RabbitMQ - virtual hosts |

## Candidatos de Narrativa para o HTML

Pergunta-motor possível:

- Como mudar uma regra de topologia em dezenas de filas sem redeploy de cada aplicação e sem dar permissão ampla demais?

Situação de abertura possível:

- O domínio `orders` tem várias filas que usam a mesma DLX. Se a DLX fica hardcoded na declaração de cada fila, a troca de destino vira mudança de aplicação. Se fica em policy, vira mudança operacional dentro do vhost.

Transformação acompanhada:

- Uma configuração nasce no código como argumento opcional, passa a ser policy por grupo, ganha guardrail de operator policy e termina com permissões mínimas por papel.

Narrativa dominante:

- Construção incremental com fronteira de autoridade.

Por que esta narrativa combina com o node:

- O tema não é "segurança" em abstrato; é governança de quem controla topologia e quais camadas vencem quando há conflito.

Exemplo condutor possível:

- Fila `orders.created`, `orders.billing` e `orders.audit` precisam usar uma DLX comum `orders.dlx`. A aplicação declara filas com nomes previsíveis; a plataforma aplica policy sobre `orders.*`; publisher recebe write só em `orders.events`; consumidor recebe read na fila; a aplicação que declara a fila precisa de configure na fila e permissões envolvidas na DLX.

Momento de nomeação dos conceitos:

- Primeiro necessidade de mudar sem redeploy; depois `x-argument`; depois policy; depois runtime parameter; depois operator policy e precedência; depois vhost; por fim configure/write/read.

Abstrações que precisam virar visual:

- Contraste entre configuração presa no cliente e policy por grupo.
- Camada de precedência.
- Mapa de permissões por papel.
- Vhost como fronteira lógica.

Contrastes realmente necessários:

- `x-argument` vs policy.
- policy comum vs operator policy.
- configure vs write vs read.

Riscos, limites e armadilhas que devem ficar no bastidor:

- Não listar todos os comandos de policy.
- Não transformar em matriz completa de todas as operações AMQP.
- Não abrir autenticação, tags ou backends.

Riscos de virar fórmula:

- Abrir com "objetivo", "pré-requisitos" ou "checklist".
- Copiar o contrato do roadmap como seções visíveis.

Risco de tom corretivo:

- O tema convida a dizer "não faça x-arguments"; a página deve primeiro mostrar a consequência prática e só depois nomear o risco.
