# Research dump - Exchange-to-exchange bindings

## Metadados do Node

- Roadmap de origem: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: intermediario
- `node_id`: `intermediario/06-exchange-to-exchange-bindings`
- Slug do node: `06-exchange-to-exchange-bindings`
- Label do node: Exchange-to-exchange bindings
- Posição numérica local no nível: 06 de 07
- Node anterior e próximo do mesmo nível para incrementalidade: anterior `intermediario/05-policies-x-arguments-e-permissoes`; próximo `intermediario/07-publisher-confirms-e-confiabilidade`
- Node anterior e próximo na sequência global do roadmap: anterior `intermediario/05-policies-x-arguments-e-permissoes`; próximo `intermediario/07-publisher-confirms-e-confiabilidade`
- Data da pesquisa: 2026-06-11
- Observações temporais: documentação oficial consultada na série RabbitMQ 4.3. A documentação 4.3 é a referência estável do roadmap; a página `Next` foi verificada apenas como sinal de continuidade, sem introduzir conteúdo de versão futura no HTML.

## Contrato Extraído do Roadmap

- Papel do node na corrente: apresenta composição de roteamento dentro do RabbitMQ sem tratar a mensagem como republicada por aplicação.
- Papel do nível no roadmap tri-level: arquitetura, relações, decisões e trade-offs.
- Pré-requisitos herdados:
  - Entender bindings de exchange para queue e contrato de topologia.
  - Entender que o node anterior separou declaração, policy, permissões e vhost como fronteiras de autoridade.
  - Entender que uma exchange roteia mensagens por bindings e não armazena mensagens como fila.
- O que introduz pela primeira vez:
  - Exchange-to-exchange binding.
  - Source exchange.
  - Destination exchange.
  - Ciclos eliminados.
  - Roteamento transitivo.
- Deve cobrir:
  - Explicar a direção source -> destination em E2E.
  - Mostrar que binding keys e tipos continuam operando normalmente.
  - Distinguir E2E de republicação manual por consumidor intermediário.
  - Registrar que RabbitMQ elimina ciclos e entrega uma cópia por fila em topologias transitivas.
  - Indicar impacto em métricas de ingress da exchange destino.
- Não deve cobrir:
  - Não cobrir federation ou multi-cluster; isso fica no avançado.
  - Não usar E2E como substituto automático de contrato simples.
  - Não repetir fundamentos de binding já cobertos.
- Perguntas do node:
  - E2E republica a mensagem ou estende o roteamento?
  - Como evitar topologia difícil de operar quando há muitas exchanges encadeadas?
  - Por que uma fila deve receber uma única cópia mesmo por rotas transitivas?
- Vocabulário conceitual:
  - E2E binding.
  - `exchange.bind`.
  - source.
  - destination.
  - transitive topology.
  - cycle detection.
- Exemplos e diagramas permitidos:
  - Cenário conceitual de `events.public` roteando para `orders.internal` e `audit.internal`.
  - Mapa HTML/CSS de exchange fonte ligada a exchanges de domínio.
- Armadilhas:
  - Usar E2E para esconder contrato mal definido.
  - Criar grafos difíceis de diagnosticar.
  - Interpretar métricas da exchange destino como se houvesse nova publicação.
- Critério de domínio: consegue explicar E2E como uma extensão de roteamento e identificar quando ela simplifica ou complica a topologia.
- Handoff: o próximo node separa confirmação de publicação de processamento no consumidor.
- Referências específicas do contrato:
  - F9 `https://www.rabbitmq.com/docs/e2e`: semântica oficial de exchange-to-exchange bindings.
  - F1 `https://www.rabbitmq.com/docs/exchanges`: resumo de E2E na documentação de exchanges.

## Matriz Anti-Repetição Aplicável

| Conteúdo | Decisão para este node |
|---|---|
| Exchange como roteador, não armazenamento | Tratar como pré-requisito. Não redefinir exchange. |
| Bindings e routing keys | Usar como base herdada. A nova camada é o destino do binding ser outra exchange. |
| Contrato de topologia e roteamento | Usar para explicar por que composição precisa preservar contrato legível. |
| Policies, x-arguments e permissões | Usar apenas como ponte: E2E também é topologia governada dentro de vhost. Não reabrir precedência ou policies. |
| Publisher confirms e confiabilidade | Reservado para `intermediario/07-publisher-confirms-e-confiabilidade`; não transformar E2E em garantia de processamento. |
| Diagnóstico de routing e observabilidade | Reservado para `avancado/01-diagnostico-de-roteamento-e-observabilidade`; este node só registra o efeito de métricas de ingress da exchange destino. |
| Federation e WAN | Reservado para `avancado/04-federated-exchanges-e-wan`; neste node, E2E fica dentro do roteamento local do broker/vhost. |
| Governança ampla e limite de complexidade | Reservado para `avancado/05-governanca-e-limites-de-complexidade`; aqui o foco é reconhecer quando a composição simplifica ou complica. |

Exemplos que não devem ser repetidos:

- Não repetir o exemplo de DLX e policy do node anterior.
- Não repetir a tabela de permissões `configure`, `write`, `read`.
- Não repetir o exemplo básico de `orders.created` indo diretamente para filas de e-mail e auditoria como centro do node; aqui o foco é source exchange ligada a destination exchanges.

Definições que podem ser tratadas como pré-requisito:

- Binding liga uma exchange de origem a um destino.
- Routing key e binding key já são conceitos conhecidos.
- Tipos direct, fanout, topic e headers já foram apresentados.
- Vhost é a fronteira lógica onde recursos, bindings e permissões vivem.

Termos que precisam ser introduzidos antes do uso visível:

- Exchange-to-exchange binding.
- Source exchange.
- Destination exchange.
- `exchange.bind`.
- Roteamento transitivo.
- Detecção de ciclos.
- Métrica de ingress da exchange destino.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/e2e  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-11  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: fonte principal para semântica oficial de exchange-to-exchange binding, direção source -> destination, uso de `exchange.bind`, ciclo eliminado e entrega única por fila em topologias transitivas.  
Tópicos cobertos: E2E, `exchange.bind`, source, destination, binding keys, tipos de exchange, múltiplos bindings, ciclos, cópia única por fila, auto-delete.  
Limites da fonte: contém exemplos de cliente Java e .NET; o HTML não usa esses exemplos como roteiro de execução.

ID: F2  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-11  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustentar exchange como tabela de roteamento, binding com destination type `exchange`, tipos de exchange roteando para exchanges e o detalhe de E2E não republicar nem atualizar ingress da exchange destino.  
Tópicos cobertos: exchanges, bindings, source/destination, destination type, direct/fanout/topic para exchanges, E2E, ingress metric.  
Limites da fonte: cobre muitos tipos e propriedades; o HTML usa apenas o necessário para o node.

ID: F3  
URL: https://www.rabbitmq.com/docs/access-control  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-11  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3, com nota de permissões passivas em 4.3.1 fora do foco do HTML.  
Motivo de uso: sustentar que `exchange.bind` é operação autorizada por recurso: `configure` na exchange destino e `write` na exchange source.  
Tópicos cobertos: permissões por vhost, operações AMQP 0-9-1, `exchange.bind`, `queue.bind`, `basic.publish`.  
Limites da fonte: usada só para autoridade operacional de topologia; o HTML não reabre o node anterior de permissões.

ID: F4  
URL: https://www.rabbitmq.com/docs/vhosts  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-11  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustentar que exchanges, filas, bindings, permissões e policies pertencem a vhosts e que conexões operam nos recursos daquele vhost.  
Tópicos cobertos: vhost, agrupamento lógico, separação lógica, recursos por vhost, conexão AMQP 0-9-1.  
Limites da fonte: não é fonte principal de E2E; usada para fronteira de escopo.

ID: F5  
URL: https://www.rabbitmq.com/docs/publishers  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-11  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustentar a leitura de publicação em AMQP 0-9-1: publisher publica em exchange, e a topologia de bindings decide filas ou exchanges alcançadas.  
Tópicos cobertos: publicação em exchange, routing topology, source/destination exchanges, mensagens sem rota.  
Limites da fonte: publisher confirms aparecem na página, mas ficam para o próximo node.

ID: F6  
URL: https://www.rabbitmq.com/docs/federated-exchanges  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-11  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: fonte de fronteira para não confundir E2E local com federated exchanges entre nodes ou clusters.  
Tópicos cobertos: exchange federation, upstream, downstream, clusters, WAN, replicação assíncrona.  
Limites da fonte: reservada ao dump e à fronteira; o HTML não ensina federation.

## Síntese por Fonte

- F1 permite afirmar que E2E adiciona `exchange.bind`, ligando uma exchange a outra com semântica igual a bindings exchange-to-queue: unidirecional, usando binding keys e tipos normalmente, com campos source e destination refletindo o fluxo da mensagem.
- F1 também permite afirmar que RabbitMQ detecta e elimina ciclos durante entrega e garante, em topologias transitivas, uma única cópia por fila alcançada.
- F2 permite afirmar que exchanges roteiam para filas, streams ou outras exchanges, que binding possui source name, destination name e destination type, e que E2E não republica mensagens.
- F2 permite afirmar que E2E usa uma única etapa lógica de roteamento sobre o conjunto de bindings da source e das destination exchanges, respeitando tipos, e que a métrica de ingress da exchange destino não é atualizada.
- F3 permite afirmar que `exchange.bind` exige autoridade sobre os dois lados: configure na destination exchange e write na source exchange.
- F4 permite afirmar que a composição E2E acontece dentro da fronteira de vhost em que os recursos existem.
- F5 reforça o modelo herdado: publicar em AMQP 0-9-1 acontece em uma exchange, e a topologia de bindings determina onde a mensagem pode chegar.
- F6 sustenta apenas a fronteira: atravessar locations, nodes, clusters ou WAN é outro mecanismo e pertence ao node avançado.

## Afirmações Técnicas Importantes

Afirmação: E2E binding é um binding entre duas exchanges, não entre exchange e fila.  
Base: F1, F2.  
Condição ou limite: continua sendo binding unidirecional e depende do tipo da exchange e da binding key.  
Impacto didático: muda o destino da aresta sem reabrir fundamentos de binding.

Afirmação: A direção do `exchange.bind` é source -> destination.  
Base: F1.  
Condição ou limite: a assinatura de clientes pode listar destination antes de source; a leitura conceitual deve seguir o fluxo da mensagem.  
Impacto didático: evita inverter mentalmente o grafo.

Afirmação: Binding keys e tipos de exchange continuam funcionando normalmente em E2E.  
Base: F1, F2.  
Condição ou limite: a mensagem só alcança destination exchanges ou filas quando as regras da topologia combinam.  
Impacto didático: E2E não é atalho mágico; é mais uma camada de roteamento.

Afirmação: E2E não republica a mensagem.  
Base: F2.  
Condição ou limite: a documentação descreve como extensão de roteamento; não implica nova publicação por aplicação nem novo evento de ingress na destination exchange.  
Impacto didático: separa composição local de consumidor intermediário que consome e publica de novo.

Afirmação: Em E2E, a métrica de ingress da exchange destino não é atualizada.  
Base: F2.  
Condição ou limite: métricas de filas e streams de destino são atualizadas quando recebem mensagens.  
Impacto didático: impede interpretar dashboard da destination exchange como prova de que nada foi roteado.

Afirmação: RabbitMQ detecta ciclos e, em topologia transitiva, cada fila recebe uma única cópia da mensagem.  
Base: F1.  
Condição ou limite: a garantia se aplica ao roteamento transitivo de uma mensagem dada na topologia avaliada pelo broker.  
Impacto didático: permite falar de grafos sem assustar com duplicação infinita.

Afirmação: Criar um binding E2E toca permissões nos dois lados do vínculo.  
Base: F3.  
Condição ou limite: em AMQP 0-9-1, `exchange.bind` exige configure na destination exchange e write na source exchange.  
Impacto didático: conecta ao node anterior sem reensinar permissões.

Afirmação: E2E local não é mecanismo de replicação entre clusters ou WAN.  
Base: F4, F6, inferência declarada.  
Condição ou limite: F4 diz que conexões operam em recursos do vhost; F6 descreve federation como mecanismo específico para locations/nodes/clusters diferentes.  
Impacto didático: protege o node avançado e evita extrapolação.

## Conceitos Essenciais

### Exchange-to-exchange binding

- Nome técnico: exchange-to-exchange binding, E2E binding.
- Explicação em linguagem simples: uma regra de roteamento que faz uma exchange enviar mensagens compatíveis para outra exchange, em vez de diretamente para uma fila.
- Necessidade neste node: é o conceito central que permite compor topologias.
- Relação com conceitos anteriores: estende binding; não muda o papel de exchange nem de routing key.
- Relação com conceitos futuros: prepara leitura de federation, plugins e governança de complexidade sem entrar nesses temas.
- Risco de confusão: imaginar que há consumidor intermediário ou nova publicação.
- Fonte base: F1, F2.

### Source exchange

- Nome técnico: source exchange.
- Explicação em linguagem simples: exchange onde o binding é adicionado e por onde a mensagem passa primeiro no fluxo E2E.
- Necessidade neste node: ajuda a orientar a direção source -> destination.
- Relação com conceitos anteriores: publisher continua publicando em uma exchange.
- Relação com conceitos futuros: ajuda em diagnóstico de topologia no avançado.
- Risco de confusão: confundir source com exchange destino por causa de assinaturas de API que listam destination antes.
- Fonte base: F1.

### Destination exchange

- Nome técnico: destination exchange.
- Explicação em linguagem simples: exchange alcançada pela source quando o binding E2E combina.
- Necessidade neste node: mostra que a destination exchange ainda aplica suas próprias regras de roteamento.
- Relação com conceitos anteriores: destino de binding antes era fila ou stream; agora pode ser exchange.
- Relação com conceitos futuros: ajuda a separar E2E local de federation.
- Risco de confusão: interpretar métrica de ingress da destination exchange como se fosse nova publicação.
- Fonte base: F1, F2.

### `exchange.bind`

- Nome técnico: `exchange.bind`.
- Explicação em linguagem simples: método/protocolo usado por RabbitMQ para criar um binding de uma exchange para outra.
- Necessidade neste node: dá forma mínima ao contrato da aresta source -> destination.
- Relação com conceitos anteriores: análogo a `queue.bind`, mas destino é exchange.
- Relação com conceitos futuros: não deve virar roteiro de client library.
- Risco de confusão: tratar o snippet como comando operacional a executar.
- Fonte base: F1, F3.

### Roteamento transitivo

- Nome técnico: transitive topology, roteamento transitivo.
- Explicação em linguagem simples: a mensagem pode atravessar mais de uma exchange por bindings encadeados até alcançar filas.
- Necessidade neste node: explica composição sem republicação.
- Relação com conceitos anteriores: exige que o leitor já entenda binding e tipo de exchange.
- Relação com conceitos futuros: aparece em diagnóstico e governança de grafos.
- Risco de confusão: achar que cada caminho cria uma cópia extra na mesma fila.
- Fonte base: F1, F2.

### Detecção de ciclos

- Nome técnico: cycle detection.
- Explicação em linguagem simples: proteção do broker para que loops de exchanges não virem entrega infinita.
- Necessidade neste node: acalma a leitura de grafos, mas não autoriza topologia confusa.
- Relação com conceitos anteriores: bindings já podiam criar múltiplas rotas; aqui podem criar ciclos entre exchanges.
- Relação com conceitos futuros: governança avançada decide quando o grafo ficou difícil demais.
- Risco de confusão: transformar a proteção do broker em permissão para desenhar ciclos.
- Fonte base: F1.

### Métrica de ingress da exchange destino

- Nome técnico: destination exchange ingress metric.
- Explicação em linguagem simples: contador de entrada da exchange destino pode não subir porque E2E não é nova publicação para essa exchange.
- Necessidade neste node: cobre impacto operacional obrigatório do contrato.
- Relação com conceitos anteriores: métricas não foram centro do nível intermediário; aqui aparece como consequência pontual.
- Relação com conceitos futuros: diagnóstico completo fica no avançado.
- Risco de confusão: abrir observabilidade em profundidade cedo demais.
- Fonte base: F2.

## Relações Causais e Estruturais

- Se o publisher precisa publicar em uma entrada estável e diferentes domínios precisam organizar suas próprias filas, uma source exchange pode encaminhar para destination exchanges de domínio; isso reduz acoplamento do publisher aos destinos finais, desde que o contrato de routing continue explícito.
- Se a source exchange é `topic`, a binding key do E2E participa do filtro antes da mensagem alcançar a destination exchange; depois, o tipo da destination exchange também participa do roteamento até filas.
- Se a mesma fila fica alcançável por duas rotas transitivas, RabbitMQ entrega uma única cópia para aquela fila; o grafo pode ter rotas múltiplas sem duplicar indefinidamente a mesma entrega.
- Se uma destination exchange recebe mensagem por E2E, a métrica de ingress dela não deve ser interpretada como publicação direta; a observação correta passa pelas filas/streams finais ou pela source/topologia.
- Se a topologia começa a exigir muitas exchanges encadeadas para entender uma entrega simples, E2E deixou de simplificar e virou custo cognitivo; essa é inferência operacional a partir do contrato do roadmap e das fontes F1/F2.
- Se o desenho precisa atravessar vhosts, clusters, WAN ou locations, E2E local não é a resposta conceitual deste node; isso pertence ao recorte de federation/shovel/replicação futura.

## Exemplos Técnicos Possíveis

### Exemplo condutor escolhido

- Exemplo: `events.public` recebe eventos publicados por produtores; um binding E2E com `orders.*` aponta para `orders.internal`, e outro binding aponta eventos relevantes para `audit.internal`.
- Mudança mostrada: o publisher continua publicando em uma entrada comum; exchanges de domínio recebem fluxo por topologia, não por republicação de consumidor intermediário.
- Conceitos introduzidos: source exchange, destination exchange, binding key, roteamento transitivo, impacto de métricas.
- Risco de escopo: virar desenho de governança completa ou diagnóstico avançado.
- Por que não vira laboratório: será mostrado como mapa conceitual e snippet mínimo de forma, sem comandos, sem client library, sem instrução de execução.

### Exemplo de ciclo/convergência

- Exemplo: duas rotas transitivas chegam a `audit.q`, mas o broker entrega uma cópia; se exchanges apontarem em ciclo, o ciclo é eliminado durante a entrega.
- Mudança mostrada: proteção de roteamento transitivo sem vender ciclos como desenho recomendado.
- Conceitos introduzidos: cycle detection, single copy per queue.
- Risco de escopo: aprofundar algoritmo interno de roteamento.
- Por que não vira laboratório: será apresentado como leitura de consequência, não teste a reproduzir.

## Obrigações de Concretização Didática

Conceito ou relação: direção source -> destination e forma de `exchange.bind`  
Tipo de demanda: forma  
Primitiva visual escolhida: snippet conceitual  
Justificativa da primitiva: a direção é fácil de inverter porque algumas APIs listam destination antes de source; um recorte nomeado deixa a forma visível sem virar comando.  
Exemplo candidato: binding E2E de `events.public` para `orders.internal` com binding key `orders.*`.  
Fonte: F1, F3.  
Por que a prosa pode não bastar: a palavra "destino" pode ser lida como fila final, não como exchange intermediária.  
Risco de virar laboratório ou excesso: mostrar método Java/.NET ou comando de CLI.  
Como manter conceitual e mínimo: usar YAML conceitual com comentário "forma conceitual".  
Fronteira com nodes futuros: não tratar publisher confirms nem automação de deploy.

Conceito ou relação: source exchange ligada a duas destination exchanges  
Tipo de demanda: topologia  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: o leitor precisa ver que o publisher não conhece as filas internas e que destination exchanges seguem roteando.  
Exemplo candidato: `events.public` -> `orders.internal` e `audit.internal`.  
Fonte: F1, F2, F5.  
Por que a prosa pode não bastar: sem mapa, E2E parece apenas "mais um binding" e não uma composição de camadas.  
Risco de virar laboratório ou excesso: desenhar muitos domínios e filas.  
Como manter conceitual e mínimo: uma source, duas destinations, poucas filas finais.  
Fronteira com nodes futuros: não entrar em federation ou WAN.

Conceito ou relação: rota transitiva com ciclo eliminado e cópia única por fila  
Tipo de demanda: estado/risco  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: a proteção contra ciclo e duplicidade é estrutural, não apenas textual.  
Exemplo candidato: duas rotas chegam a `audit.q`; ciclo é ignorado durante entrega.  
Fonte: F1.  
Por que a prosa pode não bastar: a palavra "transitivo" é abstrata.  
Risco de virar laboratório ou excesso: sugerir que ciclos são aceitáveis como desenho normal.  
Como manter conceitual e mínimo: mostrar a garantia e logo depois interpretar como proteção, não recomendação.  
Fronteira com nodes futuros: governança de grafos complexos fica para o avançado.

Conceito ou relação: ingress da destination exchange não sobe  
Tipo de demanda: contraste  
Primitiva visual escolhida: tabela curta  
Justificativa da primitiva: consolida onde olhar sem transformar em diagnóstico avançado.  
Exemplo candidato: source exchange, destination exchange e filas finais.  
Fonte: F2.  
Por que a prosa pode não bastar: métrica de destination exchange pode parecer evidência óbvia de falha.  
Risco de virar laboratório ou excesso: abrir painéis e troubleshooting completo.  
Como manter conceitual e mínimo: três linhas com "onde o sinal aparece".  
Fronteira com nodes futuros: diagnóstico operacional completo fica em `avancado/01-diagnostico-de-roteamento-e-observabilidade`.

## Riscos, Armadilhas e Erros Comuns

- Usar E2E para esconder contrato mal definido: base no contrato do roadmap e inferência operacional a partir de F1/F2. O HTML deve mostrar que composição só ajuda quando a fronteira entre source e destinations é legível.
- Inverter source e destination: base em F1, que alerta que os campos refletem o fluxo da mensagem.
- Interpretar E2E como republicação: base em F2. O HTML deve afirmar que é extensão de roteamento, não consumidor intermediário.
- Ler ingress da destination exchange como prova de publicação: base em F2. O HTML deve mostrar esse detalhe sem virar aula de observabilidade.
- Confiar em detecção de ciclos como autorização para ciclos intencionais: base em F1 e inferência. O HTML deve apresentar a garantia como proteção.
- Misturar E2E local com federation/multi-cluster: base em F4/F6. O HTML deve manter a fronteira curta.

## Limites e Fora de Escopo

- Este node explica E2E como composição de roteamento local dentro do RabbitMQ.
- Este node menciona que permissions e vhost continuam valendo, mas não reensina a matriz do node anterior.
- Este node menciona métricas de ingress apenas para evitar leitura errada da destination exchange.
- Este node não ensina federation, shovel, WAN, replicação assíncrona ou topologia entre clusters.
- Este node não ensina publisher confirms, consumer acknowledgements ou garantias de processamento.
- Este node não vira implementação com Java, .NET, CLI, HTTP API ou Terraform.
- Este node não propõe laboratório, exercício, hands-on, desafio ou projeto final.

## Divergências, Versões e Notas Temporais

- A documentação oficial usada está em RabbitMQ 4.3, coerente com o contrato do roadmap.
- O tema central é estável na documentação RabbitMQ: E2E aparece como extensão de protocolo RabbitMQ sobre AMQP 0-9-1.
- A nota temporal relevante de RabbitMQ 4.3.1 sobre declarações passivas em access control não altera o HTML, porque o node não ensina declaração passiva.
- A documentação `Next` foi aberta apenas para checar se a página E2E não indicava mudança conceitual recente óbvia; o dump mantém a versão 4.3.

### Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| Semântica E2E | F1, F2 | Base principal do HTML. |
| Source -> destination | F1 | Preparar antes de `exchange.bind`. |
| Tipos e binding keys | F1, F2 | Usar como extensão de conceitos anteriores. |
| Não republicação e ingress metric | F2 | Ponto obrigatório e delicado. |
| Permissão para criar binding E2E | F3 | Ponte com node anterior, sem aprofundar. |
| Vhost e fronteira local | F4 | Limite conceitual. |
| Publicação em exchange | F5 | Reforço do exemplo condutor. |
| Federation como fora de escopo | F6 | Usar no dump, não como ensino visível. |

### Lacunas Pesquisadas e Resolvidas

Lacuna: E2E aumenta a métrica de ingress da exchange destino?  
Busca feita: documentação oficial de exchanges e E2E.  
Fonte que resolveu: F2.  
Decisão: registrar no dump e explicar no HTML que E2E não republica e a ingress metric da destination exchange não sobe.

Lacuna: O que acontece com ciclos e múltiplos caminhos para a mesma fila?  
Busca feita: página oficial de E2E.  
Fonte que resolveu: F1.  
Decisão: explicar cycle detection e uma cópia por fila como proteção do broker.

Lacuna: Que permissões são necessárias para `exchange.bind`?  
Busca feita: access-control RabbitMQ 4.3.  
Fonte que resolveu: F3.  
Decisão: mencionar em tabela curta que o vínculo toca destination e source, sem reabrir permissões.

Lacuna: E2E atravessa vhosts ou clusters?  
Busca feita: vhosts e federated exchanges.  
Fonte que resolveu: F4 e F6.  
Decisão: tratar como fronteira; não ensinar federation.

### Lacunas Remanescentes

Não há lacuna relevante que bloqueie o HTML. O algoritmo interno exato de deduplicação de rotas não foi aprofundado porque a documentação oficial entrega a garantia conceitual necessária e o contrato do node não pede implementação interna.

## Ordem de Introdução Conceitual

Conceito: composição de routing  
Necessidade: abrir a situação antes do termo E2E.  
Explicação antes do nome: um publisher quer manter uma entrada estável, enquanto domínios internos precisam organizar seus próprios destinos.  
Nomeação: depois de mostrar que a aresta pode apontar para outra exchange.  
Depende de: exchange, binding, routing key já conhecidos.  
Pode usar depois para: explicar destination exchange e roteamento transitivo.  
Não entrar ainda em: federation, governança avançada.  
Visual possível: mapa topológico.  
Fonte base: F2, F5.

Conceito: exchange-to-exchange binding  
Necessidade: nomear a aresta que liga exchanges.  
Explicação antes do nome: binding cujo destino não é fila, mas outra exchange.  
Nomeação: primeiro bloco narrativo após o problema de composition.  
Depende de: composição de routing.  
Pode usar depois para: `exchange.bind`, source, destination, transitive topology.  
Não entrar ainda em: exemplos de client library.  
Visual possível: topologia source -> destinations.  
Fonte base: F1, F2.

Conceito: source exchange  
Necessidade: orientar a direção.  
Explicação antes do nome: exchange onde a mensagem entra no trecho da topologia.  
Nomeação: ao ler a direção da aresta.  
Depende de: E2E binding.  
Pode usar depois para: permissões e métricas.  
Não entrar ainda em: publisher confirms.  
Visual possível: label no mapa.  
Fonte base: F1.

Conceito: destination exchange  
Necessidade: mostrar que a segunda exchange ainda roteia.  
Explicação antes do nome: exchange alcançada pela source e que aplica suas próprias regras.  
Nomeação: junto com source.  
Depende de: E2E binding.  
Pode usar depois para: ingress metric e roteamento transitivo.  
Não entrar ainda em: federation.  
Visual possível: label no mapa.  
Fonte base: F1, F2.

Conceito: `exchange.bind`  
Necessidade: dar forma ao contrato.  
Explicação antes do nome: método que cria o vínculo entre duas exchanges.  
Nomeação: depois do mapa source/destination.  
Depende de: source, destination.  
Pode usar depois para: permissões de destination/source.  
Não entrar ainda em: Java/.NET/CLI.  
Visual possível: snippet conceitual.  
Fonte base: F1, F3.

Conceito: roteamento transitivo  
Necessidade: explicar encadeamento sem republicação.  
Explicação antes do nome: a mensagem pode atravessar exchanges ligadas e ainda terminar em filas.  
Nomeação: após o exemplo condutor.  
Depende de: source/destination e tipos de exchange.  
Pode usar depois para: cópia única por fila.  
Não entrar ainda em: algoritmo interno.  
Visual possível: grafo pequeno.  
Fonte base: F1, F2.

Conceito: detecção de ciclos  
Necessidade: explicar segurança de grafos.  
Explicação antes do nome: um caminho que volta para exchange anterior não gera loop infinito de entrega.  
Nomeação: depois de demonstrar rota transitiva.  
Depende de: roteamento transitivo.  
Pode usar depois para: limite de complexidade.  
Não entrar ainda em: governança avançada.  
Visual possível: ciclo pequeno sinalizado como proteção.  
Fonte base: F1.

Conceito: métricas de ingress da exchange destino  
Necessidade: resolver leitura operacional obrigatória.  
Explicação antes do nome: se não há nova publicação para a destination exchange, um contador de entrada dela pode não subir.  
Nomeação: perto do final, depois de "não republica".  
Depende de: destination exchange e não republicação.  
Pode usar depois para: leitura correta de sinais.  
Não entrar ainda em: diagnóstico completo.  
Visual possível: tabela curta.  
Fonte base: F2.

## Insumos para o Ledger Editorial

Conceito: Exchange-to-exchange binding  
Tipo: termo  
Pode aparecer depois de: situação de composition em que uma exchange precisa apontar para outra.  
Explicação mínima antes do nome: binding cujo destino é outra exchange.  
Primeira nomeação permitida: início do corpo narrativo, depois da abertura.  
Aliases e paráfrases: exchange-to-exchange binding, E2E, E2E binding, binding entre exchanges, vínculo entre exchanges.  
Pode ser usado depois para: source/destination, roteamento transitivo, `exchange.bind`.  
Não usar para: federation, republicação por consumidor, contrato genérico sem fronteira.  
Pode aparecer em título/lead/tabela/visual/referência: título sim; lead sim; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: federation e governança de complexidade ficam no avançado.  
Fonte base: F1, F2.

Conceito: Source exchange  
Tipo: papel  
Pode aparecer depois de: explicar que a aresta tem direção.  
Explicação mínima antes do nome: exchange de onde o fluxo sai.  
Primeira nomeação permitida: bloco de direção source -> destination.  
Aliases e paráfrases: source, source exchange, exchange fonte, origem.  
Pode ser usado depois para: permissões, métrica e topologia.  
Não usar para: publisher ou aplicação produtora.  
Pode aparecer em título/lead/tabela/visual/referência: título não; lead não; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: não abrir publisher confirms.  
Fonte base: F1.

Conceito: Destination exchange  
Tipo: papel  
Pode aparecer depois de: explicar source exchange.  
Explicação mínima antes do nome: exchange que recebe o fluxo roteado pela source e continua roteando.  
Primeira nomeação permitida: bloco de direção source -> destination.  
Aliases e paráfrases: destination, destination exchange, exchange destino, destino.  
Pode ser usado depois para: ingress metric, permission configure.  
Não usar para: fila final.  
Pode aparecer em título/lead/tabela/visual/referência: título não; lead não; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: não abrir federation.  
Fonte base: F1, F2.

Conceito: `exchange.bind`  
Tipo: função/método  
Pode aparecer depois de: source e destination estarem preparados.  
Explicação mínima antes do nome: método que cria o binding de exchange para exchange.  
Primeira nomeação permitida: snippet conceitual.  
Aliases e paráfrases: exchange.bind, método de binding de exchange para exchange.  
Pode ser usado depois para: permissões de configure/write.  
Não usar para: comandos executáveis ou client library.  
Pode aparecer em título/lead/tabela/visual/referência: título não; lead não; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: não virar automação de topologia.  
Fonte base: F1, F3.

Conceito: Roteamento transitivo  
Tipo: mecanismo  
Pode aparecer depois de: exemplo com source e destination exchanges.  
Explicação mínima antes do nome: mensagem atravessa mais de uma exchange por bindings encadeados.  
Primeira nomeação permitida: seção sobre caminhos que atravessam exchanges.  
Aliases e paráfrases: roteamento transitivo, transitive topology, topologia transitiva, rota transitiva, caminhos transitivos.  
Pode ser usado depois para: cópia única por fila e ciclo eliminado.  
Não usar para: replicação entre clusters.  
Pode aparecer em título/lead/tabela/visual/referência: título sim; lead não; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: diagnóstico e governança avançados.  
Fonte base: F1, F2.

Conceito: Detecção de ciclos  
Tipo: mecanismo  
Pode aparecer depois de: roteamento transitivo.  
Explicação mínima antes do nome: broker elimina loops durante entrega.  
Primeira nomeação permitida: bloco de segurança do grafo.  
Aliases e paráfrases: cycle detection, detecção de ciclos, ciclo eliminado, ciclos eliminados, loop eliminado.  
Pode ser usado depois para: explicar proteção sem recomendar ciclos.  
Não usar para: justificar topologia confusa.  
Pode aparecer em título/lead/tabela/visual/referência: título sim; lead não; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: governança de complexidade fica no avançado.  
Fonte base: F1.

Conceito: Métrica de ingress da exchange destino  
Tipo: estado/sinal  
Pode aparecer depois de: não republicação estar preparada.  
Explicação mínima antes do nome: contador de entrada da destination exchange não representa nova publicação por E2E.  
Primeira nomeação permitida: bloco final de leitura operacional.  
Aliases e paráfrases: ingress metric, métrica de ingress, taxa de entrada, inbound message rate, contador de entrada.  
Pode ser usado depois para: evitar leitura incorreta de dashboard.  
Não usar para: abrir troubleshooting avançado.  
Pode aparecer em título/lead/tabela/visual/referência: título sim; lead não; tabela sim; visual sim; referência sim.  
Fronteira com nodes futuros: observabilidade fica no avançado.  
Fonte base: F2.

Conceito: Federation  
Motivo: fronteira explícita do contrato do roadmap.  
Por que não deve aparecer no HTML: o node não deve ensinar multi-cluster/WAN; uma menção curta sem nome técnico basta para preservar fronteira.  
Aliases bloqueados no HTML: federation, federated exchange, federated exchanges, federação, exchange federada, exchanges federadas, WAN, multi-cluster, cluster remoto.  
Fonte base: F6.

Fonte: F1 `https://www.rabbitmq.com/docs/e2e`  
Termos carregados pelo título: Exchange to Exchange Bindings.  
Pode aparecer visível no HTML: sim.  
Forma visível recomendada: RabbitMQ - Exchange to Exchange Bindings.  
Decisão: essencial no rodapé.

Fonte: F2 `https://www.rabbitmq.com/docs/exchanges`  
Termos carregados pelo título: Exchanges.  
Pode aparecer visível no HTML: sim.  
Forma visível recomendada: RabbitMQ - exchanges.  
Decisão: essencial no rodapé.

Fonte: F3 `https://www.rabbitmq.com/docs/access-control`  
Termos carregados pelo título: access control, permissions.  
Pode aparecer visível no HTML: sim, depois da ponte com permissões.  
Forma visível recomendada: RabbitMQ - permissões de recursos.  
Decisão: pode aparecer no rodapé.

Fonte: F4 `https://www.rabbitmq.com/docs/vhosts`  
Termos carregados pelo título: virtual hosts.  
Pode aparecer visível no HTML: sim, se vhost for citado.  
Forma visível recomendada: RabbitMQ - virtual hosts.  
Decisão: pode aparecer no rodapé.

Fonte: F6 `https://www.rabbitmq.com/docs/federated-exchanges`  
Termos carregados pelo título: Federated Exchanges.  
Pode aparecer visível no HTML: não.  
Forma visível recomendada: manter só no dump.  
Decisão: bloqueada no HTML.

## Candidatos de Narrativa para o HTML

Pergunta-motor possível:

- Como compor duas camadas de roteamento sem transformar uma aplicação ou consumer intermediário em roteador manual?

Situação de abertura possível:

- Um publisher publica em `events.public`; os domínios `orders` e `audit` precisam receber partes do fluxo, mas o publisher não deve conhecer todas as filas internas.

Transformação acompanhada:

- Começar com publisher -> source exchange; trocar destino direto para fila por destino exchange; mostrar destination exchanges roteando; fechar com transitividade, ciclos e métricas.

Narrativa dominante:

- Topológica com construção incremental.

Por que esta narrativa combina com o node:

- E2E é uma relação estrutural entre recursos; o entendimento nasce de ver direção, fronteiras e consequências de um grafo pequeno.

Exemplo condutor possível:

- `events.public` como source exchange; `orders.internal` e `audit.internal` como destination exchanges; filas finais `orders.worker.q` e `audit.q`.

Momento de nomeação dos conceitos:

- Nomear E2E depois de mostrar a necessidade de apontar para outra exchange; nomear source/destination quando a direção aparecer; nomear `exchange.bind` depois do mapa; nomear roteamento transitivo depois do encadeamento; nomear ingress metric apenas depois de "não republica".

Abstrações que precisam virar visual:

- Direção source -> destination.
- Topologia com source e duas destinations.
- Rotas transitivas convergindo e ciclo eliminado.
- Métrica de ingress como leitura de sinal.

Contrastes realmente necessários:

- E2E versus republicação por consumidor intermediário.
- Destination exchange como etapa de roteamento, não fila final.
- Proteção contra ciclo versus desenho recomendado.

Riscos, limites e armadilhas que devem ficar no bastidor:

- Discussão completa de federation.
- Diagnóstico operacional com dashboards.
- Governança ampla de complexidade.

Riscos de virar fórmula:

- Virar tabela de "quando usar / quando não usar" cedo demais.
- Virar lista de comandos `exchangeBind`.

Risco de tom corretivo:

- A página deve construir o modelo positivo de composition antes de negar republicação, métricas e ciclos.
