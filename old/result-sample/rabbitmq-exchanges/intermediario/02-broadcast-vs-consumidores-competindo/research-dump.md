# Research dump - Broadcast vs consumidores competindo

## Metadados do Node

- Roadmap de origem: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: intermediario
- `node_id`: `intermediario/02-broadcast-vs-consumidores-competindo`
- Slug do node: `02-broadcast-vs-consumidores-competindo`
- Label do node: Broadcast vs consumidores competindo
- Posição numérica local no nível: 02 de 07
- Node anterior e próximo do mesmo nível para incrementalidade: anterior `intermediario/01-contrato-de-topologia-e-roteamento`; próximo `intermediario/03-unroutable-mandatory-e-alternate-exchange`
- Node anterior e próximo na sequência global do roadmap: anterior `intermediario/01-contrato-de-topologia-e-roteamento`; próximo `intermediario/03-unroutable-mandatory-e-alternate-exchange`
- Data da pesquisa: 2026-06-10
- Observações temporais: documentação oficial consultada na versão RabbitMQ 4.3. O recorte é RabbitMQ 4.3 e AMQP 0-9-1. Fontes oficiais foram usadas para comportamento de exchange, fila, consumidor, acknowledge, prefetch e métricas de capacidade.

## Contrato Extraído do Roadmap

- Papel do node na corrente: isolar a decisão arquitetural que mais causa erro: cópia por fila é diferente de distribuição entre consumers de uma mesma fila.
- Papel do nível no roadmap tri-level: arquitetura, relações, decisões e trade-offs.
- Pré-requisitos herdados:
  - Entender filas e consumidores como destino de entrega, não como tipo de exchange.
  - Entender o node anterior: producers publicam em uma exchange e uma convenção de routing; filas de consumidores são detalhe de topologia quando o contrato estável permite.
- Introduz pela primeira vez:
  - Broadcast para várias filas.
  - Competing consumers.
  - Multicast por direct/topic.
  - Distribuição por consumer capacity e prefetch.
- Deve cobrir:
  - Explicar broadcast como múltiplas filas recebendo cópias da mesma publicação.
  - Explicar load balancing como consumidores competindo por mensagens da mesma fila.
  - Mostrar que fanout não entrega uma cópia para cada consumer se todos estão na mesma fila.
  - Conectar prefetch e capacidade de consumer à distribuição, sem entrar em tuning detalhado.
- Não deve cobrir:
  - Não repetir detalhes de fanout/direct/topic além do necessário.
  - Não transformar prefetch em guia operacional.
  - Não discutir single active consumer e ordenação em profundidade.
  - Não abrir unroutable, mandatory, Alternate Exchange, DLX, policies, permissões, confirms ou tipos especializados.
- Perguntas do node:
  - Se três serviços precisam processar o mesmo evento, quantas filas são necessárias?
  - Se três workers dividem trabalho, eles ficam em filas separadas ou na mesma fila?
  - Como prefetch pode afetar a distribuição observada?
- Vocabulário conceitual:
  - broadcast
  - copy per queue
  - competing consumers
  - consumer capacity
  - prefetch
  - queue group
- Exemplos e diagramas permitidos:
  - Contraste visual com uma exchange ligada a três filas versus uma fila ligada a três consumers.
  - Cenário de e-mail, auditoria e analytics recebendo o mesmo evento em filas separadas.
- Armadilhas:
  - Usar fanout esperando balanceamento.
  - Criar uma fila por worker quando a intenção é dividir trabalho.
  - Colocar serviços diferentes na mesma fila e esperar que todos recebam o evento.
- Critério de domínio: consegue decidir se um cenário exige cópias independentes em filas separadas ou concorrência dentro de uma única fila.
- Handoff: depois da distribuição planejada, o próximo node trata a publicação que não encontra rota.
- Referências específicas do contrato:
  - F1 `https://www.rabbitmq.com/docs/exchanges`: fanout, direct e bindings para múltiplos destinos.
  - F4 `https://www.rabbitmq.com/docs/queues`: filas como armazenamento e entrega.
  - F5 `https://www.rabbitmq.com/docs/consumers`: consumidores e capacidade de consumo.
  - F6 `https://www.rabbitmq.com/docs/confirms`: prefetch e acknowledgements como base de entrega.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto:
  - `basico/01-modelo-amqp-e-papel-da-exchange`: exchange como roteador, não armazenamento.
  - `basico/03-bindings-routing-key-e-destinos`: binding liga exchange a destino.
  - `basico/04-direct-fanout-e-topic`: tipos clássicos de exchange e diferença básica entre direct, fanout e topic.
  - `basico/06-filas-consumidores-e-entrega`: fila armazena até entrega e consumers recebem a partir de filas.
  - `intermediario/01-contrato-de-topologia-e-roteamento`: contrato de publicação separa producer, topologia e consumidores.
- Conteúdo que pode ser reutilizado:
  - Exchange roteia para destinos ligados por bindings.
  - Filas são onde mensagens ficam antes de serem entregues.
  - Mudanças de consumidores podem ser alteração de topologia, não de producer, quando o contrato de publicação permanece estável.
- Conteúdo reservado a nodes futuros:
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: mensagem sem rota, `mandatory`, `basic.return`, Alternate Exchange e fallback de roteamento.
  - `intermediario/04-dead-letter-exchanges-e-retry-conceitual`: mensagens que saem de filas por rejeição, expiração, limite ou retry.
  - `intermediario/05-policies-x-arguments-e-permissoes`: governança por policies, argumentos opcionais e permissões.
  - `intermediario/06-exchange-to-exchange-bindings`: composição entre exchanges.
  - `intermediario/07-publisher-confirms-e-confiabilidade`: aceite pelo broker, persistência e confirms.
  - `avancado/02-tipos-especializados-e-plugins`: particionamento por hash e exchange types especializados.
- Exemplos que não devem ser repetidos:
  - Não repetir o exemplo principal do node anterior sobre domínio `orders` como contrato de routing.
  - Não refazer a aula de direct, fanout e topic.
  - Não usar DLX, AE ou confirms como exemplo condutor.
- Definições que podem ser tratadas como pré-requisito:
  - Binding é a relação que conecta exchange a fila.
  - Routing key já é vocabulário conhecido.
  - Consumer já foi apresentado como subscription de entrega a partir de uma fila.
- Termos que ainda precisam ser introduzidos no HTML:
  - Cópia por fila.
  - Concorrência dentro da fila.
  - Broadcast.
  - Competing consumers.
  - Consumer capacity.
  - Prefetch.
  - Grupo de consumidores, como tradução conceitual de uma fila compartilhada por instâncias equivalentes.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta que tipos de exchange controlam como mensagens publicadas são roteadas e que fanout roteia uma cópia para cada destino ligado.  
Tópicos cobertos: exchange types, fanout, direct, topic, default exchange, bindings e destinos.  
Limites da fonte: cobre roteamento por exchange; não define a semântica de consumo dentro de uma fila.

ID: F2  
URL: https://www.rabbitmq.com/tutorials/tutorial-two-python  
Tipo: tutorial oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta o modelo de work queue em que múltiplos workers recebem tarefas compartilhadas a partir de uma fila, além da relação didática entre prefetch e distribuição observada.  
Tópicos cobertos: work queues, round-robin dispatching, acknowledgements, fair dispatch e `prefetch_count`.  
Limites da fonte: é tutorial com exemplo Python; o HTML deve usar o comportamento conceitual, não montar laboratório ou sequência de comandos.

ID: F3  
URL: https://www.rabbitmq.com/tutorials/tutorial-three-python  
Tipo: tutorial oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta publish/subscribe com uma fila por receptor interessado e binding de cada fila à exchange.  
Tópicos cobertos: fanout exchange, temporary queues, bindings e publicação para vários receptores.  
Limites da fonte: tutorial usa filas temporárias para logs; o node aplica a mesma relação a filas de serviços duráveis sem virar tutorial de código.

ID: F4  
URL: https://www.rabbitmq.com/docs/queues  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta que filas são coleções ordenadas de mensagens e ponto de acumulação/entrega para consumidores.  
Tópicos cobertos: papel de filas, enfileirar, entregar, FIFO observado com ressalvas, nomes de filas e relação com consumidores.  
Limites da fonte: ordering real pode ser afetado por prioridades, requeue e outros recursos; esse node não entra em ordenação profunda.

ID: F5  
URL: https://www.rabbitmq.com/docs/consumers  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta que consumers consomem de filas, que delivery começa quando a fila tem mensagens, e que consumer capacity indica quanto tempo a fila consegue entregar imediatamente.  
Tópicos cobertos: consumers, subscription, fila alvo, consumer capacity, métricas e prefetch como fator de capacidade.  
Limites da fonte: consumer capacity é um sinal operacional, não prova única de sizing ou distribuição correta.

ID: F6  
URL: https://www.rabbitmq.com/docs/consumer-prefetch  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta a semântica do `prefetch_count` no RabbitMQ, incluindo a diferença entre escopo AMQP 0-9-1 e aplicação por consumidor no RabbitMQ.  
Tópicos cobertos: consumer prefetch, `basic.qos`, limite por consumer, zero como sem limite e consumidores independentes.  
Limites da fonte: não deve virar tuning; o node usa a fonte para explicar por que a distribuição observada pode mudar.

ID: F7  
URL: https://www.rabbitmq.com/docs/confirms  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte: RabbitMQ 4.3  
Motivo de uso: sustenta acknowledgements, janela de entregas não confirmadas e relação entre prefetch, throughput e consumo de memória.  
Tópicos cobertos: consumer acknowledgements, publisher confirms como conceito separado, channel prefetch, entregas em flight e requeue.  
Limites da fonte: publisher confirms são fora de escopo deste node, salvo como fronteira explícita de não confundir aceite de publicação com processamento.

## Síntese por Fonte

- F1 permite afirmar que o tipo da exchange decide a regra de roteamento. Fanout envia uma cópia de cada mensagem a cada destino ligado, direct usa equivalência exata de binding key e routing key, e topic pode agir como fanout para bindings com padrão amplo. Para este node, a afirmação crítica é: a cópia nasce no roteamento para destinos ligados, não na quantidade de consumers presos à mesma fila.
- F2 permite afirmar que uma work queue distribui tarefas entre múltiplos workers. O tutorial mostra que, quando há muitos workers na mesma fila, as tarefas são compartilhadas entre eles, e que prefetch pode impedir que um worker receba novas entregas antes de confirmar as anteriores.
- F3 permite afirmar que publish/subscribe exige uma fila para cada receptor que precisa observar todos os eventos do fluxo. O tutorial usa fila temporária para cada consumidor de logs, mas a relação estrutural é a mesma para filas duráveis por serviço.
- F4 permite afirmar que a fila é coleção ordenada de mensagens e ponto onde a mensagem aguarda até ser entregue a consumidores. Isso sustenta o contraste: uma publicação roteada para três filas vira três pontos de acumulação independentes.
- F5 permite afirmar que consumers consomem de filas e que consumer capacity mede a capacidade da fila de entregar imediatamente. O valor é pista de capacidade, não explicação suficiente para decidir broadcast.
- F6 permite afirmar que RabbitMQ aplica `prefetch_count` separadamente a cada novo consumer, diferente do escopo compartilhado do AMQP 0-9-1, e que `0` significa sem limite. O node só precisa desse mecanismo para explicar distribuição observada.
- F7 permite afirmar que prefetch limita uma janela de mensagens entregues e ainda não confirmadas; quando a janela chega ao limite, o RabbitMQ para de entregar mais mensagens naquele canal até algum ack liberar espaço. Essa relação explica por que consumidores rápidos, lentos ou com janelas diferentes podem observar distribuição desigual.

## Afirmações Técnicas Importantes

Afirmação: Broadcast em RabbitMQ, no recorte deste roadmap, significa rotear uma publicação para múltiplas filas, de modo que cada fila receba sua própria cópia lógica para consumo independente.  
Base: F1, F3, F4  
Condição ou limite: a explicação vale para exchanges e filas AMQP 0-9-1; streams e super streams ficam fora do recorte.  
Impacto didático: responde quantas filas são necessárias quando e-mail, auditoria e analytics precisam processar o mesmo evento.

Afirmação: Competing consumers significa múltiplos consumers registrados na mesma fila, concorrendo por entregas; cada mensagem entregue sai para um consumidor de cada vez dentro daquele grupo de consumo.  
Base: F2, F4, F5, F7  
Condição ou limite: redelivery pode fazer uma mensagem aparecer novamente após falha ou requeue; isso não transforma a fila em broadcast.  
Impacto didático: separa escala horizontal de workers equivalentes da necessidade de cópias independentes.

Afirmação: Fanout não entrega uma cópia para cada consumer quando todos os consumers estão na mesma fila; fanout copia para cada fila, stream ou exchange ligada.  
Base: F1, F3, F4, F5  
Condição ou limite: a quantidade de consumers de uma fila influencia quem recebe cada entrega daquela fila, não a quantidade de cópias criadas pelo exchange.  
Impacto didático: corrige a confusão principal sem depender de negação como tom dominante.

Afirmação: Direct ou topic também podem produzir multicast quando mais de uma fila tem binding compatível com a publicação.  
Base: F1; inferência declarada a partir de direct roteando para um ou mais destinos com equivalência de binding key e topic roteando por padrões compatíveis.  
Condição ou limite: o node não deve reensinar direct/topic; basta mostrar que broadcast arquitetural não é sinônimo obrigatório de fanout.  
Impacto didático: evita reduzir a decisão a "fanout versus work queue".

Afirmação: Prefetch não decide se há broadcast ou competição; ele limita quantas entregas não confirmadas cada consumer pode manter e, por isso, altera a distribuição observada entre consumers de uma mesma fila.  
Base: F2, F6, F7  
Condição ou limite: tuning detalhado de valor, throughput e latência fica fora de escopo.  
Impacto didático: permite falar de distribuição desigual sem transformar o node em guia operacional.

Afirmação: Consumer capacity é métrica por fila que indica quanto tempo a fila consegue entregar imediatamente aos consumers; baixa capacidade pode indicar falta de consumers, consumers lentos ou prefetch baixo.  
Base: F5  
Condição ou limite: a própria documentação trata a métrica como hint; aplicações precisam coletar métricas específicas.  
Impacto didático: conecta capacidade ao modelo de competing consumers sem prometer diagnóstico completo.

Afirmação: Colocar serviços diferentes na mesma fila cria competição entre eles; isso não é assinatura de evento para todos, é divisão de entregas.  
Base: F2, F3, F4, F5; inferência declarada a partir de fila como ponto de entrega e publish/subscribe exigindo fila própria para ouvir todos os eventos.  
Condição ou limite: se dois processos executam o mesmo papel, compartilhar fila pode ser correto; se executam papéis diferentes, geralmente precisam de filas distintas.  
Impacto didático: é a decisão operacional que o leitor precisa dominar.

## Conceitos Essenciais

### Cópia por fila

- Explicação simples: a mesma publicação entra em filas diferentes quando a exchange tem múltiplos destinos compatíveis.
- Por que é necessária: é a peça que torna e-mail, auditoria e analytics independentes.
- Relação com conceitos anteriores: depende de exchange, binding e fila já introduzidos.
- Relação com conceitos futuros: o próximo node tratará o caso em que não há destino compatível.
- Riscos de confusão: achar que a cópia é por consumer.
- Fonte base: F1, F3, F4.

### Broadcast

- Explicação simples: distribuição para vários destinos interessados no mesmo evento.
- Por que é necessário: nomeia a necessidade depois que o leitor vê múltiplas filas.
- Relação com conceitos anteriores: fanout já foi apresentado; aqui broadcast vira decisão de topologia.
- Relação com conceitos futuros: hash exchange e tipos especializados podem distribuir por chave sem ser broadcast.
- Riscos de confusão: tratar qualquer fanout como balanceamento de carga.
- Fonte base: F1, F3.

### Consumidores competindo

- Explicação simples: vários workers equivalentes recebem mensagens da mesma fila, cada entrega sendo atribuída a um deles.
- Por que é necessário: nomeia escala horizontal de processamento.
- Relação com conceitos anteriores: consumers já foram apresentados como subscriptions de entrega.
- Relação com conceitos futuros: single active consumer e ordenação não entram aqui.
- Riscos de confusão: colocar serviços diferentes na mesma fila.
- Fonte base: F2, F5, F7.

### Grupo de consumidores

- Explicação simples: uma fila compartilhada por instâncias que fazem o mesmo papel lógico.
- Por que é necessário: ajuda a distinguir "três workers do mesmo serviço" de "três serviços diferentes".
- Relação com conceitos anteriores: fila de grupo consumidor foi preparada no node anterior.
- Relação com conceitos futuros: governança de nomes e permissões fica para node posterior.
- Riscos de confusão: usar uma fila por worker quando o papel é igual.
- Fonte base: F2, F5; inferência de design.

### Prefetch

- Explicação simples: limite de mensagens entregues e ainda não confirmadas que um consumer ou canal pode manter.
- Por que é necessário: explica por que distribuição observada não é só "um para cada".
- Relação com conceitos anteriores: acknowledge já é pré-requisito de entrega segura.
- Relação com conceitos futuros: throughput detalhado, redelivery loops e confirms ficam fora ou para nodes futuros.
- Riscos de confusão: pensar que prefetch cria cópias ou define topologia.
- Fonte base: F2, F6, F7.

### Consumer capacity

- Explicação simples: sinal de quanto tempo uma fila consegue entregar imediatamente para seus consumers.
- Por que é necessário: conecta a pergunta sobre distribuição à capacidade real de consumo.
- Relação com conceitos anteriores: fila e consumer já são conhecidos.
- Relação com conceitos futuros: diagnóstico completo fica para `avancado/01`.
- Riscos de confusão: tratar a métrica como prova única de problema de topologia.
- Fonte base: F5.

## Relações Causais e Estruturais

- Se um evento precisa ser processado por três serviços diferentes, então cada serviço precisa de uma fila própria ligada de forma compatível à exchange, porque cada fila mantém sua própria cópia para consumo.
- Se três instâncias fazem o mesmo trabalho, então elas podem compartilhar a mesma fila, porque a fila distribui entregas entre consumers equivalentes.
- Se três serviços diferentes compartilham a mesma fila, então eles competem pelas entregas e cada serviço verá apenas parte do fluxo, salvo redeliveries por falha.
- Se um worker tem muitas entregas em flight por causa de prefetch alto, então outro worker pode parecer ocioso mesmo quando há distribuição por fila compartilhada, porque a janela local ainda não liberou novas entregas.
- Se uma fila tem baixa consumer capacity, então a fila pode estar esperando consumers, processamento ou janelas de prefetch mais adequadas; isso indica capacidade de entrega, não se a topologia é broadcast ou competição.
- Se direct ou topic têm múltiplas filas com bindings compatíveis, então a publicação pode atingir vários destinos sem usar fanout; a decisão é "quantas filas precisam da cópia", não "qual palavra de exchange soa como broadcast".

## Exemplos Técnicos Possíveis

### Evento `pedido.criado` com três serviços

- Mudança mostrada: uma publicação sai da exchange e vira três cópias em três filas.
- Conceitos introduzidos: cópia por fila, broadcast, independência de consumo.
- Risco de escopo: repetir o node anterior sobre contrato de routing.
- Como evitar laboratório: não fornecer comandos; usar nomes de filas e serviços apenas como leitura conceitual.

### Fila `relatorio.gerar` com três workers

- Mudança mostrada: mensagens entram em uma fila e consumers equivalentes recebem entregas diferentes.
- Conceitos introduzidos: consumidores competindo, grupo de consumidores, capacidade.
- Risco de escopo: virar guia de `basic_qos`.
- Como evitar laboratório: mostrar uma sequência curta de entregas, sem instrução de execução.

### `prefetch` como janela de entregas

- Mudança mostrada: um consumer com janela cheia não recebe nova entrega até confirmar alguma anterior.
- Conceitos introduzidos: prefetch, in flight, distribuição observada.
- Risco de escopo: tuning detalhado de valores.
- Como evitar laboratório: usar valores pequenos e fictícios, sem recomendar configuração.

## Obrigações de Concretização Didática

Conceito ou relação: cópia por fila versus competição dentro da fila  
Tipo de demanda: contraste  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: o leitor precisa ver que a bifurcação acontece antes da fila no broadcast e dentro da fila na competição.  
Exemplo candidato: exchange de eventos ligada a filas de e-mail, auditoria e analytics versus fila de relatório ligada a três workers.  
Fonte: F1, F2, F3, F4, F5  
Por que a prosa pode não bastar: sem forma visual, "três consumidores" e "três filas" parecem variações superficiais do mesmo desenho.  
Risco de virar laboratório ou excesso: baixo se o visual usar nomes conceituais e não comandos.  
Como manter conceitual e mínimo: usar duas colunas, cada uma com percurso curto da publicação até destino.  
Fronteira com nodes futuros: não discutir unroutable, AE, DLX ou confirms.

Conceito ou relação: prefetch como janela de mensagens ainda não confirmadas  
Tipo de demanda: estado  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: o leitor precisa ver uma janela cheia impedindo novas entregas para um consumer, enquanto outro ainda pode receber.  
Exemplo candidato: worker A com duas entregas em processamento e worker B com espaço livre.  
Fonte: F2, F6, F7  
Por que a prosa pode não bastar: a palavra `prefetch` pode soar como balanceamento, quando é limite local de entregas pendentes.  
Risco de virar laboratório ou excesso: médio se valores forem tratados como recomendação.  
Como manter conceitual e mínimo: usar "janela cheia" e "janela com espaço" sem recomendar número real.  
Fronteira com nodes futuros: não abrir tuning, throughput detalhado, redelivery loops ou quorum queue limits.

Conceito ou relação: escolha entre uma fila por serviço e uma fila por grupo equivalente  
Tipo de demanda: fronteira  
Primitiva visual escolhida: tabela curta  
Justificativa da primitiva: depois da narrativa, a decisão precisa ficar escaneável por intenção técnica.  
Exemplo candidato: "todos precisam ver" versus "um deles precisa fazer".  
Fonte: F1, F2, F3, F5  
Por que a prosa pode não bastar: a decisão costuma se perder em nomes de exchange; a tabela recoloca a pergunta no papel dos consumidores.  
Risco de virar laboratório ou excesso: baixo se não listar comandos nem configuração.  
Como manter conceitual e mínimo: duas linhas principais, com consequência e sinal de revisão.  
Fronteira com nodes futuros: não incluir casos de fallback, retry, policies ou hash.

## Riscos, Armadilhas e Erros Comuns

- Usar fanout esperando balanceamento: base F1 e F2. Fanout cria cópia por destino ligado; balanceamento entre workers acontece na fila compartilhada.
- Criar uma fila por worker quando o papel é igual: base F2 e F5. Isso cria cópias independentes e pode multiplicar trabalho, não distribuir.
- Colocar serviços diferentes na mesma fila: base F3, F4 e F5. A fila passa a dividir entregas entre papéis que deveriam receber todos os eventos.
- Interpretar consumer capacity como resposta de topologia: base F5. A métrica ajuda a ver capacidade de entrega, não decide se o evento deveria ter múltiplas filas.
- Tratar prefetch como forma de broadcast: base F6 e F7. Prefetch limita entregas não confirmadas; não cria destino novo.
- Repetir detalhes de direct, fanout e topic: risco de anti-repetição; o node só precisa lembrar que vários bindings compatíveis podem gerar múltiplos destinos.

## Limites e Fora de Escopo

- Este node explica a decisão entre cópias independentes em filas separadas e concorrência entre consumers equivalentes na mesma fila.
- Este node menciona prefetch e consumer capacity apenas para explicar distribuição observada dentro de competing consumers.
- Este node não ensina tuning de prefetch, throughput, sizing, single active consumer, ordering, DLX, AE, mandatory, confirms, policies, permissions, E2E, federation ou exchanges especializadas.
- Este node não ensina comandos de declaração de exchange, fila ou binding.
- Este node não define uma regra universal de "sempre uma fila por serviço"; a decisão depende de papéis de consumo e necessidade de cópia independente.

## Divergências, Versões e Notas Temporais

- RabbitMQ 4.3 documenta consumer prefetch como desvio prático em relação ao AMQP 0-9-1: o `prefetch_count` é aplicado separadamente a cada novo consumer no RabbitMQ, enquanto o sentido AMQP é compartilhado no canal.
- RabbitMQ 4.3 trata consumer capacity como hint; o HTML não deve converter isso em diagnóstico definitivo.
- A documentação de queues ressalva que ordenação observada pode ser afetada por prioridades e requeue. Como ordenação profunda é fora de escopo, o HTML não deve prometer round-robin perfeito nem FIFO absoluto para todos os cenários.

## Ordem de Introdução Conceitual

1. Situação concreta: uma publicação `pedido.criado` precisa chegar a e-mail, auditoria e analytics.
2. Necessidade: cada serviço precisa de sua própria cópia, porque processa por motivo próprio.
3. Nomear "cópia por fila" e depois "broadcast".
4. Contraste: três workers do mesmo serviço não precisam de três cópias; precisam dividir trabalho.
5. Nomear "consumidores competindo" e "grupo de consumidores".
6. Mostrar que fanout cria cópias por fila, não por consumer.
7. Mostrar que direct/topic também podem atingir múltiplas filas por bindings compatíveis, sem reensinar tipos clássicos.
8. Introduzir `prefetch` como janela de entregas não confirmadas.
9. Introduzir consumer capacity como sinal de capacidade de entrega da fila.
10. Fechar com pergunta decisória: todos precisam ver ou apenas um equivalente precisa executar?

## Insumos para o Ledger Editorial

- Conceitos permitidos no HTML: cópia por fila, broadcast, fila, exchange, binding, consumer, consumers equivalentes, consumidores competindo, grupo de consumidores, prefetch, entregas não confirmadas, consumer capacity, direct, topic, fanout.
- Conceitos permitidos só no dump: AMQP 0-9-1, `basic.qos`, `basic.ack`, `basic.return`, confirm mode, streams, super streams.
- Conceitos reservados a nodes futuros: unroutable, `mandatory`, Alternate Exchange, Dead Letter Exchange, policies, x-arguments, permissões, publisher confirms, exchange-to-exchange bindings, single active consumer, quorum queue delivery limit, hash exchange.
- Títulos de fontes com termos sensíveis:
  - "Consumer Acknowledgements and Publisher Confirms" pode expor publisher confirms; no HTML, se usada, a referência deve aparecer como "Guia oficial de acknowledgements e prefetch".
  - "Consumer Prefetch" pode aparecer após preparar `prefetch`.

## Candidatos de Narrativa para o HTML

- Narrativa dominante escolhida: contraste arquitetural guiado por situação concreta.
- Situação de abertura: um evento de pedido criado precisa alimentar e-mail, auditoria e analytics; isso parece "três consumidores", mas a pergunta correta é se cada papel precisa de cópia própria.
- Transformação acompanhada: a publicação sai da exchange e o desenho muda conforme a necessidade: múltiplas filas para múltiplos papéis, uma fila para workers equivalentes.
- Exemplo condutor: `pedido.criado` para três serviços e `relatorio.gerar` para três workers.
- Momento de nomeação de conceitos:
  - "cópia por fila" depois de mostrar múltiplas filas.
  - "broadcast" depois de explicar por que cada serviço precisa processar o mesmo evento.
  - "consumidores competindo" depois de mostrar uma fila com workers equivalentes.
  - `prefetch` depois de explicar entregas em andamento.
  - "consumer capacity" depois de mostrar fila que consegue ou não entregar imediatamente.
- Risco de tom corretivo: alto, porque o node nasce de uma confusão comum. Mitigação: abrir por situação positiva, não por lista de erros; usar correções apenas depois dos modelos.
- Fechamento narrativo: a pergunta decisória é se a unidade de independência é o serviço interessado no evento ou o worker equivalente que divide trabalho.
