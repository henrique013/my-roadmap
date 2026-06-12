# Research dump - Direct, fanout e topic

## Metadados do Node

- Roadmap de origem: `rabbitmq-exchanges`
- Tema humano do roadmap: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: `basico`
- Node ID: `basico/04-direct-fanout-e-topic`
- Slug do node: `04-direct-fanout-e-topic`
- Label do node: Direct, fanout e topic
- Posição local: 4 de 6
- Node anterior no nível para incrementalidade: `basico/03-bindings-routing-key-e-destinos` - Bindings, routing key e destinos
- Próximo node no nível: `basico/05-headers-e-metadados-de-roteamento` - Headers exchange e metadados de roteamento
- Node anterior na sequência global: `basico/03-bindings-routing-key-e-destinos` - Bindings, routing key e destinos
- Próximo node na sequência global: `basico/05-headers-e-metadados-de-roteamento` - Headers exchange e metadados de roteamento
- Data da pesquisa: 2026-06-08
- Observações temporais: a documentação oficial consultada está na série RabbitMQ 4.3 em 2026-06-08. O modelo AMQP 0-9-1 é estável, mas detalhes de produto e tipos disponíveis devem seguir a documentação corrente do RabbitMQ.

## Contrato Extraído do Roadmap

- Papel do node na corrente: apresenta os três tipos que resolvem a maioria dos desenhos: match exato, broadcast e padrões por segmentos.
- Papel do nível no roadmap tri-level: estabilizar fundamentos, vocabulário indispensável e modelos mentais antes de detalhar headers, filas, consumidores e decisões intermediárias.
- Pré-requisitos herdados:
  - Entender binding, routing key e múltiplos destinos.
  - Entender que o node anterior já introduziu binding key como critério registrado na ligação e routing key como dado enviado na publicação.
- O que o node introduz pela primeira vez:
  - Direct exchange.
  - Fanout exchange.
  - Topic exchange.
  - Wildcard `*`.
  - Wildcard `#`.
- O que deve cobrir:
  - Comparar direct como igualdade exata entre routing key e binding key.
  - Explicar fanout como cópia para todos os destinos ligados, ignorando routing key.
  - Explicar topic como match por segmentos separados por ponto, com `*` e `#`.
  - Mostrar quando direct pode fazer multicast se várias filas usam a mesma binding key.
  - Destacar que `#` em topic pode aproximar o comportamento de fanout.
- O que não deve cobrir:
  - Não cobrir headers exchange; fica no próximo node.
  - Não discutir DLX, AE, policies ou plugins.
  - Não aprofundar naming conventions de eventos além dos exemplos conceituais.
- Perguntas do node:
  - Quando direct é suficiente?
  - Por que fanout não é o mesmo que vários consumidores na mesma fila?
  - Quando topic é mais expressivo que direct?
  - Como `#` pode tornar um binding amplo demais?
- Vocabulário conceitual:
  - direct
  - fanout
  - topic
  - routing pattern
  - `*` wildcard
  - `#` wildcard
  - broadcast
  - multicast
- Exemplos e diagramas permitidos:
  - Tabela comparando `orders.created`, `logs.error` e `audit.user.login` em direct/fanout/topic.
  - Cenário de notificação e auditoria recebendo cópias por filas diferentes.
- Armadilhas:
  - Usar fanout quando se queria filtro por categoria.
  - Usar topic sem convenção estável de routing keys.
  - Achar que direct só entrega para uma fila.
  - Usar `#` como curinga genérico sem avaliar volume.
- Critério de domínio: consegue escolher entre direct, fanout e topic a partir da intenção de roteamento e explicar a consequência para cada fila ligada.
- Handoff: depois dos tipos baseados em key textual, o próximo node cobre headers exchange para critérios por atributos.
- Referências específicas herdadas do contrato: F1 e F2 do roadmap, expandidas neste dump com tutoriais oficiais e especificação.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto no node 01:
  - Publisher publica em uma exchange.
  - Exchange roteia e não armazena como destino final.
  - Filas armazenam mensagens e consumidores recebem de filas.
- Conteúdo já coberto no node 02:
  - A default exchange é uma direct exchange especial.
  - `exchange=""` não significa ausência de exchange.
  - A aparente publicação direta em fila é conveniência da default exchange.
- Conteúdo já coberto no node 03:
  - Binding é regra de roteamento entre source exchange e destino.
  - Routing key acompanha a publicação.
  - Binding key é critério registrado no binding.
  - Uma publicação pode chegar a zero, um ou vários destinos.
  - Exchange sem bindings é tabela de roteamento vazia, não fila vazia.
- Conteúdo que este node adiciona:
  - Como três tipos clássicos interpretam a key textual ou ignoram essa key.
  - Direct: igualdade exata entre key enviada e key registrada.
  - Fanout: envio de cópia a todos os destinos ligados.
  - Topic: padrões por segmentos separados por ponto, com `*` e `#`.
  - Multicast em direct quando vários destinos usam a mesma binding key.
  - Risco de ampliar demais uma regra com `#`.
- Conteúdo reservado a nodes futuros:
  - `basico/05-headers-e-metadados-de-roteamento`: critérios por atributos de mensagem, argumentos de binding e `x-match`.
  - `basico/06-filas-consumidores-e-entrega`: competição de consumidores na mesma fila, acks e entrega.
  - `intermediario/01-contrato-de-topologia-e-roteamento`: desenho de contratos de topologia.
  - `intermediario/02-broadcast-vs-consumidores-competindo`: aprofundamento arquitetural da diferença entre cópia para filas diferentes e consumidores competindo na mesma fila.
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: sinais e tratamento de mensagens sem rota.
  - `intermediario/04-dead-letter-exchanges-e-retry-conceitual`: DLX e retry conceitual.
  - `intermediario/05-policies-x-arguments-e-permissoes`: policies, permissões e argumentos mutáveis.
  - `intermediario/06-exchange-to-exchange-bindings`: bindings entre exchanges.
  - `avancado/02-tipos-especializados-e-plugins`: tipos especializados e plugins.
- Exemplos que não devem ser repetidos:
  - Não repetir o exemplo central do node 03 como "tabela de bindings vazia versus preenchida".
  - Usar `orders.created`, `logs.error` e `audit.user.login` apenas como chaves de roteamento conceituais, não como guia de convenção de nomes.
- Termos ainda precisam ser introduzidos neste node:
  - direct exchange, fanout exchange, topic exchange, routing pattern, wildcard `*`, wildcard `#`, broadcast e multicast.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: define tipos de exchange, fanout, topic, direct, uso de routing key e binding pattern, e registra que `#` em topic pode agir como fanout para o binding que usa esse padrão.  
Tópicos cobertos: direct, fanout, topic, routing key, binding key, wildcard `*`, wildcard `#`, routing para queues/streams/exchanges.  
Limites da fonte: também cobre default exchange, headers, E2E, alternate exchanges e propriedades; este node usa apenas os trechos necessários para os três tipos clássicos baseados em chave textual ou cópia ampla.

ID: F2  
URL: https://www.rabbitmq.com/tutorials/amqp-concepts  
Tipo: guia oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: explica o modelo AMQP 0-9-1, incluindo a regra de direct, o comportamento de fanout e topic, e a possibilidade de direct ser usado para multicast.  
Tópicos cobertos: exchanges, tipos clássicos, direct, fanout, topic, unicast, multicast, broadcast, queue bindings.  
Limites da fonte: é guia conceitual amplo; detalhes atuais de produto e tipos adicionais usam F1.

ID: F3  
URL: https://www.rabbitmq.com/tutorials/tutorial-three-javascript  
Tipo: tutorial oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3, tutorial JavaScript para AMQP 0-9-1  
Motivo de uso: oferece exemplo oficial de publish/subscribe com fanout e reforça que fanout publica para todos os destinos conhecidos pela exchange, ignorando uma routing key específica.  
Tópicos cobertos: fanout, publish/subscribe, broadcast para receptores, separação entre produtor, exchange e filas.  
Limites da fonte: usa cliente JavaScript e exemplos operacionais; o HTML usa apenas o conceito, não comandos nem laboratório.

ID: F4  
URL: https://www.rabbitmq.com/tutorials/tutorial-four-javascript  
Tipo: tutorial oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3, tutorial JavaScript para AMQP 0-9-1  
Motivo de uso: explica direct exchange por match exato entre binding key e routing key e mostra que múltiplas filas com a mesma binding key recebem a mensagem.  
Tópicos cobertos: direct, binding key, routing key, match exato, múltiplos bindings com mesma key, seletividade.  
Limites da fonte: usa logging como exemplo operacional; o node adapta a leitura para exemplos conceituais menores.

ID: F5  
URL: https://www.rabbitmq.com/tutorials/tutorial-five-javascript  
Tipo: tutorial oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3, tutorial JavaScript para AMQP 0-9-1  
Motivo de uso: explica topic exchange, routing keys segmentadas por ponto, wildcards `*` e `#`, e o comportamento de topic como fanout ou direct em casos específicos.  
Tópicos cobertos: topic, routing pattern, segmentos, wildcard `*`, wildcard `#`, padrões amplos e ausência de match.  
Limites da fonte: tutorial usa chaves de log e exemplos de animais; o HTML evita repetir esses exemplos como laboratório.

ID: F6  
URL: https://www.rabbitmq.com/resources/specs/amqp0-9.pdf  
Tipo: especificação  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: AMQP 0-9, dezembro de 2006  
Motivo de uso: ancora o vocabulário normativo do protocolo, especialmente routing key de topic como palavras separadas por ponto e padrões `*`/`#`.  
Tópicos cobertos: exchange types, topic routing key, routing pattern, wildcards.  
Limites da fonte: é especificação do protocolo AMQP 0-9; RabbitMQ 4.3 adiciona comportamento e tipos próprios que devem ser conferidos na documentação oficial atual.

## Síntese por Fonte

F1 permite afirmar que o tipo da exchange controla a lógica de roteamento. Para fanout, a routing key da mensagem é ignorada e cada destino ligado recebe uma cópia. Para topic, a routing key é comparada com um padrão de binding dividido por segmentos separados por ponto; `*` cobre exatamente um segmento e `#` cobre zero ou mais segmentos. Para direct, a rota passa por equivalência exata da key do binding.

F2 sustenta a leitura didática dos três tipos: direct costuma servir para roteamento seletivo por key exata, fanout para broadcast, e topic para variações de publish/subscribe com padrões. F2 também registra que direct pode ser multicast quando várias filas estão ligadas à exchange com a mesma key.

F3 reforça o fanout com um cenário de publish/subscribe: várias filas recebem cópias da mesma publicação quando estão ligadas à exchange. A fonte ajuda a separar broadcast por filas diferentes de competição entre consumidores na mesma fila, tema que será aprofundado depois.

F4 dá a forma mais clara para direct: a mensagem vai para filas cuja binding key corresponde exatamente à routing key da mensagem. O tutorial também mostra que se duas filas estiverem ligadas com a mesma key, ambas recebem a mensagem.

F5 sustenta a explicação de topic: a key de roteamento deve seguir palavras separadas por ponto, e as binding keys podem ter `*` e `#`. A fonte também sustenta duas fronteiras úteis: `#` sozinho se aproxima de fanout, e topic sem wildcards se comporta como direct para aquelas bindings.

F6 ancora a regra de segmentos em fonte normativa. A especificação ajuda a evitar inventar semântica para `*` e `#`, mas deve ser combinada com F1 porque o roadmap é sobre RabbitMQ atual.

## Afirmações Técnicas Importantes

Afirmação: direct exchange roteia por igualdade exata entre a key da publicação e a key registrada no binding.  
Base: F1, F2, F4  
Condição ou limite: o destino pode ser mais de uma fila se mais de um binding tiver a mesma key.  
Impacto didático: mostra que direct é simples, mas não necessariamente "um para um".

Afirmação: fanout exchange envia uma cópia para todos os destinos ligados e ignora a routing key da mensagem.  
Base: F1, F2, F3  
Condição ou limite: o node fala de cópia para filas ou destinos ligados; competição entre consumidores dentro da mesma fila fica para outro node.  
Impacto didático: evita usar fanout quando a intenção era filtrar por categoria.

Afirmação: topic exchange compara a routing key da mensagem com padrões de binding compostos por segmentos separados por ponto.  
Base: F1, F5, F6  
Condição ou limite: este node usa exemplos pequenos; não define uma convenção de nomenclatura de eventos.  
Impacto didático: explica por que topic é mais expressivo que direct quando há mais de um eixo de escolha.

Afirmação: em topic, `*` corresponde exatamente a um segmento e `#` corresponde a zero ou mais segmentos.  
Base: F1, F5, F6  
Condição ou limite: uma key que não satisfaz o padrão não encontra aquele binding. O tratamento de mensagens sem rota fica fora do escopo.  
Impacto didático: dá precisão para ler padrões como `audit.*.login` e `logs.#`.

Afirmação: um binding topic com `#` pode ficar amplo a ponto de se aproximar de fanout.  
Base: F1, F5  
Condição ou limite: a aproximação vale para o binding que usa `#`; a exchange topic continua avaliando seus demais bindings.  
Impacto didático: mostra risco real de volume e perda de seletividade sem abrir diagnóstico avançado.

Afirmação: topic sem wildcards nos padrões pode se comportar como direct para aquelas bindings.  
Base: F5, inferência a partir de F1  
Condição ou limite: a comparação é local às bindings sem `*` ou `#`, não uma equivalência global entre tipos.  
Impacto didático: ajuda a explicar topic como expansão de expressividade sobre direct, sem vender topic como substituto automático.

## Conceitos Essenciais

Conceito: direct exchange  
Explicação simples: tipo de exchange que procura bindings cuja key é exatamente igual à routing key da publicação.  
Necessidade no node: é o primeiro contraste depois do node de bindings, porque aplica diretamente o par binding key/routing key.  
Relação com conceitos anteriores: usa binding e routing key já introduzidos no node 03.  
Relação com conceitos futuros: será usado como opção de desenho em contrato de topologia.  
Riscos de confusão: achar que direct sempre entrega para uma única fila.  
Fonte base: F1, F2, F4.

Conceito: fanout exchange  
Explicação simples: tipo de exchange que manda cópia da publicação para todos os destinos ligados, sem consultar a routing key.  
Necessidade no node: cobre broadcast básico e prepara a diferença entre filas múltiplas e consumidores competindo.  
Relação com conceitos anteriores: usa bindings como lista de saídas existentes.  
Relação com conceitos futuros: broadcast versus consumidores competindo será aprofundado no intermediário.  
Riscos de confusão: usar fanout como filtro ou confundir "todos os destinos ligados" com "todos os consumidores do sistema".  
Fonte base: F1, F2, F3.

Conceito: topic exchange  
Explicação simples: tipo de exchange que compara a routing key com padrões segmentados por ponto.  
Necessidade no node: explica quando direct fica estreito demais para escolhas por múltiplos eixos.  
Relação com conceitos anteriores: usa binding key como padrão, não apenas como valor exato.  
Relação com conceitos futuros: contratos de topologia e governança cuidarão de padrões estáveis.  
Riscos de confusão: tratar topic como "qualquer string com ponto" sem contrato estável.  
Fonte base: F1, F5, F6.

Conceito: routing pattern  
Explicação simples: padrão registrado no binding de uma topic exchange para comparar com a routing key da publicação.  
Necessidade no node: diferencia o valor enviado pela publicação do padrão que a topologia aceita.  
Relação com conceitos anteriores: herda binding key e routing key.  
Relação com conceitos futuros: naming conventions profundas ficam fora do básico.  
Riscos de confusão: usar padrões amplos demais ou achar que todos os tipos interpretam a key como padrão.  
Fonte base: F1, F5, F6.

Conceito: wildcard `*`  
Explicação simples: em topic, representa exatamente um segmento entre pontos.  
Necessidade no node: permite explicar padrões seletivos sem enumerar todas as keys.  
Relação com conceitos anteriores: depende de routing key segmentada por ponto.  
Relação com conceitos futuros: governaça de padrões fica para contrato de topologia.  
Riscos de confusão: achar que `*` cobre zero segmentos ou vários segmentos.  
Fonte base: F1, F5, F6.

Conceito: wildcard `#`  
Explicação simples: em topic, representa zero ou mais segmentos.  
Necessidade no node: mostra a força e o risco de padrões amplos.  
Relação com conceitos anteriores: depende de routing key segmentada por ponto.  
Relação com conceitos futuros: diagnóstico de rotas amplas e governança ficam para níveis posteriores.  
Riscos de confusão: usar `#` como curinga genérico sem avaliar volume e perda de seletividade.  
Fonte base: F1, F5, F6.

Conceito: broadcast  
Explicação simples: intenção de enviar cópias da mesma publicação para todos os destinos ligados.  
Necessidade no node: nomeia a consequência do fanout.  
Relação com conceitos anteriores: o node 03 já permitiu múltiplos destinos; fanout transforma isso em regra incondicional.  
Relação com conceitos futuros: comparação com consumidores competindo vem depois.  
Riscos de confusão: confundir broadcast com balanceamento de trabalho entre consumers.  
Fonte base: F2, F3.

Conceito: multicast em direct  
Explicação simples: entrega para mais de uma fila quando várias filas têm bindings com a mesma key exata.  
Necessidade no node: corrige a leitura de que direct é sempre um destino único.  
Relação com conceitos anteriores: usa múltiplos bindings já introduzidos.  
Relação com conceitos futuros: decisões arquiteturais sobre quando fazer isso ficam para o intermediário.  
Riscos de confusão: usar esse ponto para redesenhar topologia em profundidade cedo demais.  
Fonte base: F2, F4.

## Relações Causais e Estruturais

- Binding existente -> tipo da exchange interpreta a regra: o node 03 mostrou a existência da regra; este node mostra que a mesma key pode ser tratada como igualdade, ignorada ou interpretada como padrão.
- Direct -> igualdade exata: se a publicação chega com `orders.created`, apenas bindings com key exatamente igual recebem a rota. Se duas filas têm essa key, as duas recebem cópias.
- Fanout -> todas as saídas: se a exchange tem três destinos ligados, os três recebem cópia da publicação, mesmo que a routing key esteja vazia ou tenha outro valor.
- Topic -> segmentos: `audit.user.login` pode ser lida como três segmentos. Um padrão como `audit.*.login` combina com exatamente um segmento no meio; `audit.#` combina com a família iniciada por `audit`.
- `#` amplo -> perda de filtro: quanto mais cedo e amplo o `#` aparece, mais mensagens atravessam aquele binding, reduzindo a intenção seletiva da topologia.
- Topic sem wildcards -> comportamento próximo a direct: se o padrão é só `orders.created`, a comparação fica exata para aquela binding.
- Fanout versus consumidores competindo: fanout copia para filas distintas; competição entre consumidores na mesma fila é outro mecanismo e será tratado depois.

## Exemplos Técnicos Possíveis

Exemplo: `orders.created` publicado em uma exchange direct.  
Mudança ou contraste mostrado: uma fila com binding key `orders.created` recebe; uma fila com `orders.cancelled` não recebe; duas filas com `orders.created` recebem.  
Conceitos introduzidos: direct, match exato, multicast por bindings iguais.  
Risco de escopo: pode virar guia de domínio de pedidos.  
Como manter conceitual: usar só como key curta e não discutir naming convention.

Exemplo: `logs.error` publicado em fanout.  
Mudança ou contraste mostrado: a key existe, mas a exchange fanout não a usa para filtrar; todas as filas ligadas recebem cópia.  
Conceitos introduzidos: fanout, broadcast, routing key ignorada.  
Risco de escopo: pode virar sistema de logs completo.  
Como manter conceitual: não abrir severity, source nem observabilidade.

Exemplo: `audit.user.login` publicado em topic.  
Mudança ou contraste mostrado: `audit.*.login` combina, `audit.#` combina, `orders.#` não combina.  
Conceitos introduzidos: topic, segmentos, `*`, `#`, padrão amplo.  
Risco de escopo: pode virar convenção de eventos.  
Como manter conceitual: explicar somente a forma da comparação.

Exemplo condutor escolhido para o HTML: uma exchange recebe três publicações conceituais (`orders.created`, `logs.error`, `audit.user.login`) e o leitor observa como direct, fanout e topic tomam decisões diferentes sobre as mesmas ideias de key e binding.  
Motivo: o exemplo não depende de comandos, não vira laboratório e permite comparar forma, estado e consequência.

## Obrigações de Concretização Didática

Conceito ou relação: direct, fanout e topic aplicam decisões diferentes sobre routing key e bindings.  
Tipo de demanda: contraste  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: a pessoa precisa ver os três caminhos lado a lado sem transformar isso em bloco ASCII.  
Exemplo candidato: três painéis com "igualdade exata", "todos os destinos ligados" e "padrão por segmentos".  
Fonte: F1, F2, F3, F4, F5  
Por que a prosa pode não bastar: os três tipos compartilham vocabulário, mas divergem justamente na leitura da key.  
Risco de virar laboratório ou excesso: baixo se não houver comandos ou setup.  
Como manter conceitual e mínimo: usar keys curtas e destinos fictícios.  
Fronteira com nodes futuros: não abrir headers, AE, DLX, policies, E2E ou consumers.

Conceito ou relação: topic interpreta `*` e `#` por segmentos.  
Tipo de demanda: forma  
Primitiva visual escolhida: snippet mínimo + tabela curta  
Justificativa da primitiva: a forma `audit.*.login` e `audit.#` precisa ser vista literalmente.  
Exemplo candidato: keys `audit.user.login`, `audit.org.login`, `audit.user.logout` comparadas com padrões.  
Fonte: F1, F5, F6  
Por que a prosa pode não bastar: sem ver os pontos e curingas, a diferença entre um segmento e vários segmentos fica abstrata.  
Risco de virar laboratório ou excesso: médio se virar catálogo de padrões.  
Como manter conceitual e mínimo: três linhas de snippet e uma tabela de leitura.  
Fronteira com nodes futuros: não transformar em guia de naming convention.

Conceito ou relação: direct pode entregar para mais de uma fila.  
Tipo de demanda: risco/fronteira  
Primitiva visual escolhida: callout + mini-card  
Justificativa da primitiva: a confusão é de cardinalidade; basta mostrar que duas filas podem compartilhar a mesma key.  
Exemplo candidato: `orders.created` para fila de notificação e fila de auditoria.  
Fonte: F2, F4  
Por que a prosa pode não bastar: o termo "direct" sugere um único destino para muitos leitores.  
Risco de virar laboratório ou excesso: baixo se tratado como consequência, não como topologia recomendada.  
Como manter conceitual e mínimo: não discutir ownership nem contrato de domínio.  
Fronteira com nodes futuros: decisão arquitetural fica para intermediário.

## Riscos, Armadilhas e Erros Comuns

- Achar que direct é sempre unicast: F2 e F4 sustentam que múltiplas filas com a mesma key podem receber a publicação. O HTML deve apresentar isso como consequência natural, não como "pegadinha".
- Usar fanout quando se queria filtro: F1 e F3 sustentam que fanout ignora routing key; se a intenção depende de categoria, direct ou topic pode ser mais adequado.
- Confundir fanout com consumidores competindo: F3 sustenta a cópia para vários receptores; o aprofundamento de competição fica fora deste node.
- Usar topic como desculpa para qualquer key textual: F5 e F6 exigem segmentos por ponto e padrões específicos; naming conventions profundas ficam fora do escopo.
- Usar `#` amplo demais: F1 e F5 sustentam que `#` pode combinar qualquer routing key, aproximando o binding de fanout. O HTML deve mostrar a consequência sem abrir diagnóstico.
- Achar que topic substitui direct sempre: F5 permite dizer que topic sem wildcards se comporta como direct, mas isso não torna direct inútil nem topic sempre melhor.

## Limites e Fora de Escopo

- Este node explica:
  - direct como match exato.
  - fanout como cópia para todos os destinos ligados.
  - topic como padrão segmentado por ponto com `*` e `#`.
  - multicast em direct quando bindings iguais apontam para múltiplos destinos.
  - `#` como padrão amplo e potencialmente amplo demais.
- Este node apenas menciona como fronteira:
  - O próximo node tratará critérios por atributos em headers exchange.
  - Consumers competindo e entrega serão tratados no node 06 e no intermediário.
- Este node não cobre:
  - Headers exchange em profundidade.
  - DLX, AE, mandatory, returns, policies, permissions, plugins ou exchange-to-exchange bindings.
  - Naming conventions de eventos, versionamento de routing keys ou contrato arquitetural completo.
  - Comandos, setup, laboratório ou exercício.

## Divergências, Versões e Notas Temporais

- A documentação oficial de RabbitMQ consultada está na versão 4.3 e deve prevalecer para comportamento do produto.
- A especificação AMQP 0-9 é antiga, mas segue útil para o vocabulário de exchange types e routing patterns. Ela não substitui a documentação RabbitMQ 4.3 para extensões e tipos adicionais.
- Não foi encontrada divergência entre F1, F2, F4, F5 e F6 sobre as regras essenciais de direct, fanout, topic, `*` e `#`.
- A fonte F1 menciona destinos queue, stream ou exchange; o HTML deve focar em filas como destino didático e não abrir streams ou E2E.

## Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| Direct como match exato | F1, F2, F4 | F4 dá exemplo didático de binding key igual à routing key. |
| Direct com múltiplos destinos | F2, F4 | Usado para desfazer a leitura "direct = uma fila". |
| Fanout ignora routing key | F1, F2, F3 | Base para broadcast conceitual. |
| Topic por segmentos | F1, F5, F6 | Base para padrões com ponto. |
| `*` e `#` | F1, F5, F6 | F1 e F5 registram exemplos e fronteiras. |
| `#` aproximando fanout | F1, F5 | Deve aparecer como cuidado de amplitude. |
| Topic sem wildcards parecido com direct | F5, inferência F1 | Tratar como comportamento local de bindings, não equivalência global. |

## Lacunas Pesquisadas e Resolvidas

Lacuna: direct entrega sempre para uma fila ou pode entregar para várias?  
Busca feita: documentação oficial e tutorial de routing.  
Fonte que resolveu: F2, F4.  
Decisão: explicar que direct pode fazer multicast quando várias filas usam a mesma binding key.

Lacuna: fanout usa ou ignora routing key?  
Busca feita: documentação oficial de exchanges e tutorial de publish/subscribe.  
Fonte que resolveu: F1, F3.  
Decisão: afirmar que fanout ignora a routing key e entrega cópias a todos os destinos ligados.

Lacuna: `#` cobre uma ou várias palavras?  
Busca feita: documentação RabbitMQ, tutorial topic e especificação.  
Fonte que resolveu: F1, F5, F6.  
Decisão: registrar que `#` cobre zero ou mais segmentos; `*` cobre exatamente um.

Lacuna: `#` sozinho pode ser comparado a fanout?  
Busca feita: documentação de exchanges e tutorial topic.  
Fonte que resolveu: F1, F5.  
Decisão: explicar como aproximação para o binding que usa `#`, sem dizer que topic vira fanout globalmente.

## Lacunas Remanescentes

Não há lacuna remanescente que bloqueie o HTML. A página deve preservar limites de escopo: não detalhar headers, DLX, AE, policies, plugins, consumidores competindo nem naming conventions.

## Ordem de Introdução Conceitual

Conceito: tipo de exchange como regra de decisão  
Necessidade: antes de nomear direct/fanout/topic, a pessoa precisa entender que o binding existe e a diferença está em como a exchange avalia a publicação.  
Explicação antes do nome: "a mesma publicação pode ser comparada por igualdade, enviada a todos os destinos ou testada contra um padrão".  
Nomeação: depois da abertura com as três perguntas de decisão.  
Depende de: binding, routing key e binding key herdados do node 03.  
Pode usar depois para: comparar direct, fanout e topic.

Conceito: direct exchange  
Necessidade: explicar o caso simples em que a key enviada deve bater exatamente com a key registrada.  
Explicação antes do nome: "quando a intenção é uma etiqueta exata, a exchange só precisa perguntar se os dois textos são iguais".  
Nomeação: na primeira seção de comparação.  
Depende de: binding key e routing key.  
Pode usar depois para: mostrar multicast por bindings iguais e contrastar com topic sem wildcards.

Conceito: fanout exchange  
Necessidade: explicar a intenção de cópia para todos os destinos ligados.  
Explicação antes do nome: "às vezes a publicação não precisa escolher; todos os destinos ligados devem receber uma cópia".  
Nomeação: após a necessidade de broadcast.  
Depende de: múltiplos destinos ligados.  
Pode usar depois para: contrastar com filtro por categoria e com `#`.

Conceito: topic exchange  
Necessidade: explicar quando uma key exata é pouco expressiva e a decisão depende de segmentos.  
Explicação antes do nome: "em vez de uma etiqueta única, a key pode carregar partes separadas por ponto".  
Nomeação: antes do visual de segmentos e wildcards.  
Depende de: direct e routing key.  
Pode usar depois para: explicar `*`, `#` e padrões amplos.

Conceito: wildcard `*`  
Necessidade: mostrar como topic aceita um segmento variável sem aceitar qualquer tamanho.  
Explicação antes do nome: "um pedaço da key pode variar, mas precisa ocupar exatamente uma posição".  
Nomeação: na seção de topic.  
Depende de: topic e segmentos por ponto.  
Pode usar depois para: explicar `audit.*.login`.

Conceito: wildcard `#`  
Necessidade: mostrar padrão amplo que cobre zero ou mais segmentos.  
Explicação antes do nome: "às vezes o restante da key pode ter tamanho variável".  
Nomeação: depois de `*`, porque é mais amplo.  
Depende de: topic e segmentos por ponto.  
Pode usar depois para: explicar risco de amplitude e aproximação com fanout.

Conceito: broadcast  
Necessidade: nomear a intenção de todos os destinos ligados receberem cópia.  
Explicação antes do nome: "a publicação não escolhe um destino; ela é copiada para todos os ligados".  
Nomeação: junto de fanout.  
Depende de: fanout e múltiplos destinos.  
Pode usar depois para: separar fanout de consumidores competindo.

Conceito: multicast  
Necessidade: explicar que direct pode entregar para várias filas quando a mesma key aparece em vários bindings.  
Explicação antes do nome: "igualdade exata não limita a quantidade de bindings que podem combinar".  
Nomeação: depois de direct.  
Depende de: direct e múltiplos bindings.  
Pode usar depois para: responder à pergunta "direct é suficiente?".

## Candidatos de Narrativa para o HTML

- Narrativa escolhida: construção incremental por decisão de roteamento. A página abre com uma publicação chegando a uma exchange que já tem bindings e pergunta "qual regra de decisão deve ser aplicada?".
- Narrativa rejeitada: tabela seca de tipos. Falharia porque repetiria definições sem mostrar consequência para cada fila ligada.
- Narrativa rejeitada: sequência de erros comuns. Falharia porque abriria em tom corretivo e não construiria modelo positivo.
- Situação de abertura: três publicações conceituais (`orders.created`, `logs.error`, `audit.user.login`) entram em exchanges com destinos diferentes; a página acompanha como a decisão muda por tipo.
- Transformação acompanhada: a pessoa passa de "binding existe" para "o tipo da exchange decide como ler a key".
- Momento de nomeação: direct depois da igualdade; fanout depois da necessidade de cópia ampla; topic depois da necessidade de padrão por segmentos.
- Risco de tom corretivo: tratar "direct não é só uma fila" como pegadinha. A redação deve apresentar multicast como consequência, não bronca.

## Necessidades Reais de Visualização

- Um quadro comparativo HTML/CSS dos três tipos é necessário para ver contraste de decisão.
- Uma tabela com keys e resultados é necessária para concretizar o match sem virar laboratório.
- Um snippet curto de patterns topic é útil para mostrar `*` e `#` literalmente; deve ter highlight semântico.
- Não há necessidade de ASCII excepcional.

