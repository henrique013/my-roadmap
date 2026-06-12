# Research dump - Modelo AMQP e papel da exchange

## Metadados do Node

- Roadmap de origem: `rabbitmq-exchanges`
- Tema humano do roadmap: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: `basico`
- Node ID: `basico/01-modelo-amqp-e-papel-da-exchange`
- Slug do node: `01-modelo-amqp-e-papel-da-exchange`
- Label do node: Modelo AMQP e papel da exchange
- Posição local: 1 de 6
- Node anterior no nível: nenhum; este é o primeiro node do nível.
- Próximo node no nível: `basico/02-exchange-padrao-e-publicacao-direta-aparente` - Exchange padrão e publicação direta aparente
- Data da pesquisa: 2026-06-08
- Observações temporais: a documentação consultada de RabbitMQ está na série 4.3 em 2026-06-08. A especificação AMQP 0-9-1 é estável e anterior; ela é usada para o modelo conceitual do protocolo, enquanto a documentação RabbitMQ cobre a implementação atual.

## Contrato Extraído do Roadmap

- Papel do node na corrente: cria o modelo mental central em que produtores publicam em exchanges, exchanges roteiam por bindings, filas armazenam e consumidores recebem das filas.
- Papel do nível no roadmap tri-level: estabilizar os conceitos básicos antes de escolher tipos de exchange, políticas, falhas de roteamento ou governança.
- Pré-requisitos herdados:
  - Noção de mensagem, produtor, consumidor e comunicação assíncrona.
- O que introduz pela primeira vez:
  - Exchange como entidade de roteamento.
  - Fluxo `publisher -> exchange -> binding -> fila -> consumer`.
  - Diferença entre roteamento e armazenamento.
- O que deve cobrir:
  - Explicar por que a exchange é o ponto de publicação no AMQP 0-9-1.
  - Mostrar que uma mensagem pode ir para zero, uma ou várias filas conforme o roteamento.
  - Diferenciar broker, publisher, exchange, queue, binding e consumer sem ainda entrar em tipos específicos.
  - Deixar explícito que a exchange não é o local onde consumidores se registram.
- O que não deve cobrir:
  - Não detalhar direct, fanout, topic e headers; isso fica em nodes posteriores.
  - Não entrar em DLX, AE, confirms ou operação de produção.
  - Não transformar o fluxo em roteiro de comandos.
- Perguntas do node:
  - Qual problema a exchange resolve entre produtores e consumidores?
  - Por que dizer que a exchange armazena mensagens é conceitualmente errado?
  - Como uma única publicação pode virar várias cópias em filas diferentes?
- Vocabulário conceitual:
  - `publisher`
  - `producer`
  - `broker`
  - `exchange`
  - `queue`
  - `binding`
  - `consumer`
  - `message copy`
- Exemplos e diagramas permitidos:
  - Diagrama HTML/CSS do caminho `publisher -> exchange -> bindings -> queues -> consumers`.
  - Cenário conceitual de eventos de pedido consumidos por faturamento e notificação em filas separadas.
- Armadilhas:
  - Confundir exchange com fila.
  - Achar que consumidor assina exchange diretamente.
  - Achar que existe sempre uma única fila por publicação.
- Critério de domínio: consegue desenhar o fluxo de uma mensagem e explicar onde ocorre roteamento, onde ocorre armazenamento e onde ocorre consumo.
- Handoff: com esse fluxo claro, o próximo node apresenta a exchange padrão, que cria a aparência de publicação direta em fila.
- Referências específicas herdadas do contrato: F1, F2, F16.

## Matriz Anti-Repetição Aplicável

- Conceito central introduzido aqui: exchange como roteador, não armazenamento.
- Reuso permitido depois:
  - `basico/06-filas-consumidores-e-entrega`: contraste curto com filas que armazenam mensagens.
  - `avancado/05-governanca-e-limites-de-complexidade`: critério para detectar topologias pensadas como fila mental.
- Reuso bloqueado:
  - `intermediario/04-dead-letter-exchanges-e-retry-conceitual`: não deve redefinir exchange; deve herdar o conceito deste node.
- Fronteira com node 02: este node pode dizer que existe um próximo caso em que a publicação parece ir direto para uma fila, mas não deve explicar a exchange padrão, nome vazio, `amq.default` ou publicação direta aparente.
- Fronteira com node 03: este node pode usar binding como regra de ligação, mas não deve ensinar o vocabulário de chaves de roteamento nem separar chave da publicação e regra do binding.
- Fronteira com node 04 e 05: tipos específicos de exchange e critérios por headers ficam fora.
- Fronteira com intermediário: mensagens sem rota, alternate exchange, dead-letter, policies e confirms ficam fora.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: define exchange como entidade em que publishers publicam mensagens e como mecanismo que roteia para queues, streams ou outras exchanges usando tipo da exchange e propriedades de binding.  
Tópicos cobertos: exchange, roteamento, destino, binding, tipos de exchange como fronteira.  
Limites da fonte: a página cobre muitos temas futuros; neste node só entram definição de exchange, propósito de roteamento e noção geral de binding.

ID: F2  
URL: https://www.rabbitmq.com/tutorials/amqp-concepts  
Tipo: guia oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: descreve o modelo AMQP 0-9-1 em visão ampla: mensagens são publicadas em exchanges, distribuídas como cópias para filas por bindings e depois entregues ou obtidas por consumidores.  
Tópicos cobertos: broker, publisher, producer, exchange, queue, binding, consumer, cópia de mensagem.  
Limites da fonte: é guia didático amplo; detalhes operacionais e tipos específicos são deliberadamente excluídos deste node.

ID: F3  
URL: https://www.rabbitmq.com/assets/files/amqp0-9-1-43a54a005e97180a4fbe6e567a125d84.pdf  
Tipo: especificação  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: AMQP 0-9-1, documento de 2006-2008 publicado pelo RabbitMQ  
Motivo de uso: fonte primária do modelo que separa exchange, message queue, binding e consumer.  
Tópicos cobertos: exchange recebe mensagens de produtores e roteia para filas; fila armazena e entrega; binding relaciona exchange e fila; consumer recebe mensagens de uma fila.  
Limites da fonte: não substitui a documentação RabbitMQ para detalhes de implementação atual.

ID: F4  
URL: https://www.rabbitmq.com/docs/queues  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta a fronteira: fila é coleção ordenada onde mensagens entram e de onde são entregues a consumidores.  
Tópicos cobertos: queue como estrutura de armazenamento e entrega.  
Limites da fonte: detalhes de propriedades de fila ficam para nodes posteriores; aqui entra apenas o contraste com exchange.

ID: F5  
URL: https://www.rabbitmq.com/docs/consumers  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta que a entrega carrega metadados como exchange que roteou a mensagem e que o consumer é associado à entrega a partir de fila, não à assinatura direta em exchange.  
Tópicos cobertos: consumer, metadados de entrega, relação com fila.  
Limites da fonte: acknowledgements, polling e single active consumer ficam fora do HTML deste node.

## Síntese por Fonte

F1 permite afirmar que, em AMQP 0-9-1, publishers publicam em exchanges e que a finalidade da exchange é rotear mensagens para destinos como queues, streams ou outras exchanges. Para este node, a parte útil é a separação entre publicar no roteador e armazenar na fila; os tipos específicos são mantidos como fronteira.

F2 permite construir a explicação didática do caminho: publisher/produtor envia para exchange; exchange distribui cópias para filas usando bindings; depois o broker entrega para consumidores inscritos nas filas ou consumidores buscam mensagens. Também sustenta que a exchange pode rotear para zero ou mais filas.

F3 confirma o modelo base do protocolo: exchange recebe de produtores e roteia para message queues; message queue armazena até que consumidores processem com segurança; binding define a relação e os critérios que conduzem mensagens para filas; consumer é a entidade ligada à recepção a partir da fila.

F4 sustenta o contraste com exchange: fila é uma coleção ordenada de mensagens e é o ponto de enfileiramento e desenfileiramento. Este node não precisa entrar em ordering avançado, prioridades ou requeue.

F5 sustenta o detalhe de que a mensagem entregue ao consumidor carrega metadados de roteamento, incluindo a exchange que a roteou. Esse fato ajuda a mostrar que a exchange participa antes da entrega ao consumidor, mas não é onde o consumidor se registra.

## Afirmações Técnicas Importantes

Afirmação: no AMQP 0-9-1, o produtor publica a mensagem em uma exchange, não diretamente no consumidor.  
Base: F1, F2, F3  
Condição ou limite: o próximo node explicará o caso em que a publicação parece usar o nome de uma fila; aqui essa aparência não deve ser detalhada.  
Impacto didático: fixa o ponto inicial do fluxo sem abrir exceções cedo demais.

Afirmação: a exchange roteia; ela não é o armazenamento durável ou temporário usado pelos consumidores.  
Base: F1, F3, F4  
Condição ou limite: RabbitMQ também pode rotear para streams ou outras exchanges, mas este roadmap mantém o foco em filas AMQP 0-9-1.  
Impacto didático: previne a confusão central entre exchange e queue.

Afirmação: uma publicação pode resultar em zero, uma ou várias filas recebendo cópias, conforme as regras existentes.  
Base: F2, F1  
Condição ou limite: o comportamento detalhado da ausência de rota e as opções de retorno ou alternate exchange ficam para nodes intermediários.  
Impacto didático: evita a suposição de que publicar sempre equivale a escolher uma única fila.

Afirmação: binding é a relação que coloca uma fila no alcance de uma exchange segundo critérios de roteamento.  
Base: F1, F2, F3  
Condição ou limite: o node 03 detalhará o vocabulário de chave e regra; este node usa binding apenas como regra de ligação no fluxo.
Impacto didático: dá ao leitor peça suficiente para entender por que uma exchange não decide sozinha para onde enviar.

Afirmação: consumidores recebem mensagens a partir de filas; eles não assinam uma exchange como destino final da entrega.  
Base: F2, F3, F5  
Condição ou limite: mecanismos de entrega, confirmação e distribuição entre vários consumidores serão tratados depois.  
Impacto didático: separa roteamento, armazenamento e consumo.

## Conceitos Essenciais

Conceito: mensagem  
Explicação simples: unidade enviada pelo produtor e depois armazenada e entregue por RabbitMQ.  
Necessidade no node: é o objeto que atravessa o caminho conceitual.  
Relação com conceitos anteriores: pressuposto básico de mensageria.  
Relação com conceitos futuros: será associada a metadados, chaves, headers e confirmações em nodes posteriores.  
Risco de confusão: achar que a exchange transforma ou processa o conteúdo da mensagem.  
Fonte base: F2

Conceito: publisher / producer  
Explicação simples: aplicação que publica mensagens no broker.  
Necessidade no node: é o início do caminho.  
Relação com conceitos anteriores: corresponde à noção geral de produtor.  
Relação com conceitos futuros: publisher confirms ficam fora.  
Risco de confusão: supor que o producer escolhe diretamente o consumidor.  
Fonte base: F2, F3

Conceito: broker  
Explicação simples: serviço RabbitMQ que recebe publicações, aplica topologia e entrega mensagens.  
Necessidade no node: é o ambiente onde exchange, fila e binding existem.  
Relação com conceitos anteriores: middleware de mensageria.  
Relação com conceitos futuros: vhost, permissões e governança ficam depois.  
Risco de confusão: tratar broker como sinônimo de exchange.  
Fonte base: F2

Conceito: exchange  
Explicação simples: entidade de roteamento onde a publicação chega primeiro.  
Necessidade no node: é o conceito central.  
Relação com conceitos anteriores: resolve o acoplamento entre produtor e destino final.  
Relação com conceitos futuros: tipos de exchange e exchange padrão ficam depois.  
Risco de confusão: pensar que armazena mensagens para consumidores.  
Fonte base: F1, F2, F3

Conceito: fila / queue  
Explicação simples: estrutura que guarda mensagens até a entrega a consumidores.  
Necessidade no node: contraste com exchange.  
Relação com conceitos anteriores: forma concreta de armazenamento assíncrono.  
Relação com conceitos futuros: ordering, consumo concorrente e acknowledgements ficam depois.  
Risco de confusão: achar que uma exchange se comporta como fila.  
Fonte base: F3, F4

Conceito: binding  
Explicação simples: ligação que cria uma regra para a exchange alcançar uma fila.  
Necessidade no node: explica por que a mesma exchange pode levar a diferentes filas.  
Relação com conceitos anteriores: não pressupõe conhecimento de chaves.  
Relação com conceitos futuros: node 03 aprofunda binding, regra e critério.  
Risco de confusão: antecipar detalhes de key e tipo de exchange.  
Fonte base: F1, F2, F3

Conceito: consumer  
Explicação simples: aplicação ou assinatura que recebe mensagens a partir de uma fila.  
Necessidade no node: fecha o caminho sem invadir entrega avançada.  
Relação com conceitos anteriores: noção geral de consumidor.  
Relação com conceitos futuros: competing consumers e acknowledgements ficam depois.  
Risco de confusão: achar que consumidor se registra na exchange.  
Fonte base: F2, F3, F5

Conceito: cópia de mensagem  
Explicação simples: uma publicação pode produzir cópias em filas diferentes quando mais de uma fila é alcançada pelas regras.  
Necessidade no node: mostra por que uma publicação não precisa equivaler a um único destino.  
Relação com conceitos anteriores: complementa a ideia de mensagem.  
Relação com conceitos futuros: broadcast e múltiplos consumidores serão separados depois.  
Risco de confusão: confundir múltiplas filas com múltiplos consumidores na mesma fila.  
Fonte base: F2

## Relações Causais e Estruturais

- Se o publisher publica em uma exchange, então o primeiro problema do broker é roteamento, não entrega final. Condição: existe uma topologia com exchange e bindings declarados. Base: F1, F2.
- Se uma exchange tem bindings que alcançam duas filas, então a mesma publicação pode resultar em duas filas com cópias independentes. Condição: a regra de roteamento aplicável escolhe ambas as filas. Base: F2; detalhes de tipo ficam fora.
- Se uma exchange não encontra destino aplicável, então o resultado não é "guardar para depois" dentro da exchange. Condição: comportamento concreto de retorno, descarte ou fallback será estudado no intermediário. Base: F1, F2.
- Se uma fila recebe a mensagem, então o armazenamento e a entrega passam a ser responsabilidade da fila. Condição: simplificação conceitual; propriedades de fila ficam para node 06. Base: F3, F4.
- Se um consumer aparece na arquitetura, ele recebe da fila, não da exchange. Condição: sem detalhar pull API, acknowledgements ou exclusividade. Base: F2, F3, F5.

## Exemplos Técnicos Possíveis

Exemplo: evento `pedido.criado` publicado por uma aplicação de pedidos, roteado para filas de faturamento e notificação.  
Mostra: uma publicação chegando em uma exchange e virando duas cópias em filas independentes.  
Conceitos introduzidos: publisher, exchange, binding, queue, consumer, cópia.  
Risco de escopo: o nome do evento pode sugerir regras de chave reservadas ao node 03.  
Como manter mínimo: tratar o nome como rótulo da mensagem, não como chave de roteamento.

Exemplo: publicação sem fila alcançada.  
Mostra: zero destino não significa armazenamento dentro da exchange.  
Conceitos introduzidos: fronteira entre roteamento e armazenamento.  
Risco de escopo: pode puxar mandatory, alternate exchange e unroutable.  
Como manter mínimo: dizer apenas que a exchange não vira fila; guardar alternativas para depois.

Exemplo: uma fila com consumer de faturamento e outra com consumer de notificação.  
Mostra: consumidores ficam depois das filas.  
Conceitos introduzidos: consumer como leitor/assinatura de fila.  
Risco de escopo: concorrência entre consumidores da mesma fila é node 06.  
Como manter mínimo: usar um consumer por fila no desenho.

## Obrigações de Concretização Didática

Conceito ou relação: caminho publisher -> exchange -> binding -> filas -> consumers.  
Tipo de demanda: ordem e topologia.  
Primitiva visual escolhida: componente HTML/CSS.  
Justificativa da primitiva: a relação é espacial e sequencial; cards conectados deixam claro onde cada responsabilidade muda sem usar ASCII.  
Exemplo candidato: publicação de pedido que alcança filas de faturamento e notificação.  
Fonte: F1, F2, F3.  
Por que a prosa pode não bastar: a diferença entre roteamento e armazenamento tende a virar abstração verbal; a pessoa precisa ver o ponto em que a mensagem deixa a exchange e passa para filas.  
Risco de virar laboratório ou excesso: baixo se não houver comandos nem configuração.  
Como manter conceitual e mínimo: não incluir declarações de exchange, nomes de chaves, comandos ou API.  
Fronteira com nodes futuros: não explicar tipos de exchange nem chaves.

Conceito ou relação: zero, uma ou várias filas alcançadas por uma publicação.  
Tipo de demanda: estado e contraste.  
Primitiva visual escolhida: tabela curta.  
Justificativa da primitiva: comparação de três resultados possíveis fica mais clara em tabela do que em parágrafos repetidos.  
Exemplo candidato: sem fila, fila única, duas filas.  
Fonte: F2, F1.  
Por que a prosa pode não bastar: sem contraste explícito, o leitor pode manter a suposição "publicação igual a uma fila".  
Risco de virar laboratório ou excesso: médio se começar a explicar parâmetros de publicação; evitar esses parâmetros.  
Como manter conceitual e mínimo: usar linguagem de resultado observável, sem opções operacionais.  
Fronteira com nodes futuros: mensagens sem rota e alternate exchange ficam no intermediário.

Conceito ou relação: troca de responsabilidade entre exchange, fila e consumer.  
Tipo de demanda: fronteira.  
Primitiva visual escolhida: cards de responsabilidade.  
Justificativa da primitiva: cada card pode carregar uma responsabilidade principal e impedir que o leitor misture papéis.  
Exemplo candidato: exchange decide destino, fila segura a mensagem, consumer processa a partir da fila.  
Fonte: F1, F3, F4, F5.  
Por que a prosa pode não bastar: a palavra "entrega" pode parecer cobrir roteamento, armazenamento e consumo ao mesmo tempo.  
Risco de virar laboratório ou excesso: baixo.  
Como manter conceitual e mínimo: não explicar ordering avançado nem acknowledgements.  
Fronteira com nodes futuros: detalhes de fila e consumidor ficam no node 06.

## Riscos, Armadilhas e Erros Comuns

- Confundir exchange com fila. Base: contrato do roadmap, F1, F3, F4.
- Achar que a exchange segura mensagens para consumidores offline. Base: inferência de F1/F3/F4; a fila, não a exchange, é o armazenamento relevante neste recorte.
- Achar que consumidor assina exchange diretamente. Base: F2, F3, F5.
- Achar que sempre há exatamente uma fila por publicação. Base: F2.
- Antecipar detalhes de `routing key` ou tipos específicos antes de estabilizar o papel da exchange. Base: matriz anti-repetição do roadmap.

## Limites e Fora de Escopo

Este node explica:

- Por que a exchange existe entre produtor e filas.
- Onde ocorre roteamento, armazenamento e consumo.
- Como uma publicação pode alcançar zero, uma ou várias filas.
- Por que consumidores recebem de filas, não de exchanges.

Este node apenas menciona como fronteira:

- O próximo node sobre a exchange padrão e a aparência de publicação direta.
- A existência de regras de roteamento mais detalhadas que serão nomeadas depois.

Fica para outro node:

- Exchange padrão, nome vazio e `amq.default`: node 02.
- `routing key`, `binding key` e destinos: node 03.
- Direct, fanout e topic: node 04.
- Headers exchange: node 05.
- Filas, consumidores, acknowledgements e concorrência: node 06.
- Mandatory, alternate exchange, DLX, confirms e policies: intermediário.

Não pertence ao roadmap neste ponto:

- Tutorial de linguagem, comando, setup local, UI de management ou projeto prático.

## Divergências, Versões e Notas Temporais

- Tema temporalmente estável: o modelo básico AMQP 0-9-1 de exchange, queue, binding e consumer é estável.
- Versão RabbitMQ: as páginas oficiais consultadas estão na série 4.3 em 2026-06-08.
- Diferença fonte/especificação: a especificação usa `message queue` como termo formal; o HTML pode usar `fila` e `queue` como equivalentes preparados.
- Detalhe conscientemente não expandido: a documentação atual lembra que exchanges podem rotear para streams ou outras exchanges, mas o contrato do roadmap limita o básico a filas AMQP 0-9-1.

## Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| Exchange como ponto de publicação | F1, F2, F3 | Fonte primária e documentação oficial concordam. |
| Exchange como roteador, não armazenamento | F1, F3, F4 | F4 dá a fronteira positiva da fila. |
| Binding como ligação entre exchange e fila | F1, F2, F3 | Detalhe de chaves fica para node 03. |
| Zero, uma ou várias filas | F2, F1 | Sem detalhar comportamento de unroutable. |
| Consumer recebe de fila | F2, F3, F5 | Sem entrar em acknowledgements. |
| Cópias independentes em filas diferentes | F2 | Usado como modelo conceitual mínimo. |

## Lacunas Pesquisadas e Resolvidas

Lacuna: é correto dizer que exchange armazena mensagens por algum tempo?  
Busca feita: documentação oficial de exchanges, queues e especificação AMQP 0-9-1.  
Fonte que resolveu: F1, F3, F4.  
Decisão: o HTML afirma que a exchange é roteador e que a fila é o armazenamento no recorte deste node.

Lacuna: pode haver zero filas alcançadas por uma publicação?  
Busca feita: guia oficial AMQP concepts e documentação de exchanges.  
Fonte que resolveu: F2.  
Decisão: o HTML mostra zero/uma/várias filas como resultado de roteamento, sem explicar fallback ou parâmetros operacionais.

Lacuna: consumidor se conecta a exchange ou fila?  
Busca feita: guia AMQP, especificação e documentação de consumers.  
Fonte que resolveu: F2, F3, F5.  
Decisão: o HTML declara que consumidor recebe a partir da fila e que exchange fica antes da etapa de entrega.

## Lacunas Remanescentes

Não há lacuna relevante para este node. Os detalhes deliberadamente ausentes são fronteiras de escopo, não incertezas: tipos de exchange, chaves de roteamento, exchange padrão, mensagens sem rota e confiabilidade serão cobertos depois.

## Ordem de Introdução Conceitual

Conceito: mensagem  
Necessidade: objeto que atravessa o fluxo.  
Explicação antes do nome: uma aplicação precisa enviar um fato ou evento para outras partes do sistema.  
Nomeação: mensagem.  
Depende de: noção de comunicação assíncrona.  
Pode usar depois para: mostrar publicação, cópia e armazenamento.  
Não entrar ainda em: propriedades, headers, delivery mode.  
Visual possível: card inicial do fluxo.  
Fonte base: F2.

Conceito: publisher / producer  
Necessidade: origem da publicação.  
Explicação antes do nome: a aplicação que coloca a mensagem no broker.  
Nomeação: publisher, também chamado producer.  
Depende de: mensagem.  
Pode usar depois para: publicar em exchange.  
Não entrar ainda em: confirms.  
Visual possível: card "publisher".  
Fonte base: F2, F3.

Conceito: broker  
Necessidade: ambiente que hospeda exchange, fila e binding.  
Explicação antes do nome: serviço intermediário que recebe e encaminha mensagens.  
Nomeação: broker RabbitMQ.  
Depende de: publisher e mensagem.  
Pode usar depois para: localizar exchange e fila como entidades do broker.  
Não entrar ainda em: vhost, permissões, cluster.  
Visual possível: título ou moldura do fluxo.  
Fonte base: F2.

Conceito: exchange  
Necessidade: resolver o desacoplamento entre produtor e filas.  
Explicação antes do nome: em vez de escolher diretamente um destino final, a publicação entra em um ponto que decide para quais filas seguir.  
Nomeação: exchange.  
Depende de: publisher, mensagem, broker.  
Pode usar depois para: explicar roteamento.  
Não entrar ainda em: tipos específicos, default exchange.  
Visual possível: card central do fluxo.  
Fonte base: F1, F2, F3.

Conceito: binding  
Necessidade: explicar como a exchange sabe que uma fila está no seu alcance.  
Explicação antes do nome: uma ligação configurada entre exchange e fila cria uma regra de roteamento.  
Nomeação: binding.  
Depende de: exchange e fila.  
Pode usar depois para: mostrar uma ou várias filas alcançadas.  
Não entrar ainda em: routing key e binding key.  
Visual possível: conectores entre exchange e filas.  
Fonte base: F1, F2, F3.

Conceito: fila / queue  
Necessidade: separar armazenamento de roteamento.  
Explicação antes do nome: depois que uma regra escolhe um destino, a mensagem precisa ficar em uma estrutura que possa entregá-la ao consumidor.  
Nomeação: fila / queue.  
Depende de: exchange e binding.  
Pode usar depois para: armazenamento e entrega a consumidores.  
Não entrar ainda em: concorrência, ack, ready/delivered.  
Visual possível: dois cards de fila.  
Fonte base: F3, F4.

Conceito: consumer  
Necessidade: fechar o caminho da mensagem.  
Explicação antes do nome: a aplicação que recebe mensagens a partir de uma fila.  
Nomeação: consumer ou consumidor.  
Depende de: fila.  
Pode usar depois para: separar consumo de publicação.  
Não entrar ainda em: acknowledgements, competing consumers.  
Visual possível: card após cada fila.  
Fonte base: F2, F3, F5.

Conceito: cópia da mensagem  
Necessidade: explicar várias filas recebendo a mesma publicação.  
Explicação antes do nome: quando mais de uma fila é alcançada, cada fila recebe sua própria instância para consumo independente.  
Nomeação: cópia.  
Depende de: binding e fila.  
Pode usar depois para: broadcast e múltiplos destinos em nodes futuros.  
Não entrar ainda em: fanout ou competing consumers.  
Visual possível: tabela de resultado.  
Fonte base: F2.

## Insumos para o Ledger Editorial

Conceitos que podem aparecer no HTML:

- Mensagem: depois de uma necessidade de comunicação assíncrona; permitido em título, lead, corpo, tabela, visual e referências.
- Publisher / producer: depois de apresentar a aplicação que publica; aliases `publisher`, `producer`, `produtor`, `aplicação publicadora`.
- Broker: depois de explicar o serviço intermediário; aliases `RabbitMQ`, `broker RabbitMQ`, `servidor RabbitMQ` quando usado como serviço.
- Exchange: depois de explicar que a publicação entra em um ponto de roteamento; aliases `exchange`, `roteador`, `ponto de publicação`, `entidade de roteamento`.
- Queue / fila: depois de separar armazenamento; aliases `queue`, `fila`, `fila de mensagens`.
- Binding: depois de explicar a ligação entre exchange e fila; aliases `binding`, `ligação`, `regra de ligação`, `regra de roteamento` em sentido amplo.
- Consumer / consumidor: depois de explicar recepção a partir da fila; aliases `consumer`, `consumidor`, `aplicação consumidora`.
- Cópia da mensagem: depois de apresentar múltiplas filas; aliases `cópia`, `cópias independentes`, `message copy`.
- Roteamento: depois de exchange; aliases `rotear`, `direcionar`, `encaminhar conforme regras`.
- Armazenamento: depois de fila; aliases `guardar`, `segurar`, `manter até entrega`.

Conceitos permitidos só no dump:

- `routing key`: pertence ao node 03.
- `binding key`: pertence ao node 03.
- `mandatory`: pertence ao intermediário.
- `alternate exchange`: pertence ao intermediário.
- `dead-letter exchange`: pertence ao intermediário.
- `publisher confirms`: pertence ao intermediário.
- `acknowledgement`: pertence ao node 06 e intermediário; não deve aparecer no HTML deste node.

Conceitos reservados a nodes futuros:

- Exchange padrão / default exchange: node 02. Menção permitida apenas no contexto do próximo node e no fechamento como handoff.
- Direct, fanout, topic: node 04. Nenhuma menção visível neste HTML.
- Headers exchange: node 05. Nenhuma menção visível neste HTML.
- Competing consumers e acknowledgements: node 06. Nenhuma explicação visível neste HTML.
- DLX, AE, confirms e policies: intermediário. Nenhuma menção visível neste HTML.

Títulos de fontes que carregam vocabulário técnico:

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Exchanges | Sim | `RabbitMQ - Exchanges` |
| F2 | AMQP 0-9-1 Model | Sim | `RabbitMQ - AMQP 0-9-1 Model Explained` |
| F3 | Advanced Message Queuing Protocol Specification | Sim | `AMQP 0-9-1 specification` |
| F4 | Queues | Sim | `RabbitMQ - Queues` |
| F5 | Consumers | Sim | `RabbitMQ - Consumers` |

## Candidatos de Narrativa para o HTML

Pergunta-motor possível:
- Quando uma aplicação publica uma mensagem, por que ela não deve escolher diretamente o consumidor?

Situação de abertura possível:
- Uma aplicação de pedidos publica um evento. Faturamento e notificação podem precisar reagir, mas o produtor não deveria carregar a lista de quem consome.

Transformação acompanhada:
- A mensagem sai do publisher, entra no broker por uma exchange, encontra bindings, aparece em zero/uma/várias filas e só então consumidores recebem a partir das filas.

Narrativa dominante:
- Topológica com construção incremental.

Por que esta narrativa combina com o node:
- O node existe para separar papéis e fronteiras de responsabilidade; a topologia mostra melhor do que uma definição isolada.

Exemplo condutor possível:
- Evento de pedido que pode alimentar faturamento e notificação em filas separadas.

Momento de nomeação dos conceitos:
- Nomear exchange depois de estabelecer a necessidade de não acoplar produtor a consumidores.
- Nomear binding depois de mostrar que a exchange precisa de regra para alcançar filas.
- Nomear queue depois de mostrar que roteamento não é armazenamento.
- Nomear consumer no fim do caminho, depois da fila.

Abstrações que precisam virar visual:
- Caminho da mensagem.
- Zero/uma/várias filas.
- Responsabilidades de exchange/fila/consumer.

Contrastes realmente necessários:
- Exchange roteia; fila armazena.
- Consumidor recebe de fila; não da exchange.
- Publicação não implica destino único.

Riscos, limites e armadilhas que devem ficar no bastidor:
- Lista extensa de erros comuns.
- Detalhes de mensagens sem rota.
- Tipos específicos de exchange.

Riscos de virar fórmula:
- Transformar o capítulo em sequência fixa de definições. Mitigação: usar uma situação de publicação e retornar a ela em cada parte.

Risco de tom corretivo:
- Abrir dizendo apenas "exchange não é fila". Mitigação: primeiro mostrar por que o produtor precisa de um ponto de roteamento; o contraste vem depois.

## Validação do Dump

- Contrato do roadmap extraído: sim.
- Matriz anti-repetição aplicada: sim.
- Fontes primárias priorizadas: sim.
- Afirmações importantes com fonte ou inferência declarada: sim.
- Conceitos essenciais com dependências explícitas: sim.
- Relações causais e estruturais claras: sim.
- Riscos, limites e divergências registrados: sim.
- Lacunas relevantes resolvidas ou declaradas: sim.
- Ordem de introdução conceitual existe: sim.
- Insumos para o Ledger Editorial existem: sim.
- Obrigações de Concretização Didática existem e registram demandas reais: sim.
- Conceitos classificados para HTML, dump e nodes futuros: sim.
- Aliases e títulos de fontes registrados: sim.
- Candidatos de narrativa existem: sim.
- Dump não é outline do HTML: sim.
