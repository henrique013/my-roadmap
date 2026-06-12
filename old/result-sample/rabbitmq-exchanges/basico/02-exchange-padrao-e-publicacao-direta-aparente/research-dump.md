# Research dump - Exchange padrão e publicação direta aparente

## Metadados do Node

- Roadmap de origem: `rabbitmq-exchanges`
- Tema humano do roadmap: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: `basico`
- Node ID: `basico/02-exchange-padrao-e-publicacao-direta-aparente`
- Slug do node: `02-exchange-padrao-e-publicacao-direta-aparente`
- Label do node: Exchange padrão e publicação direta aparente
- Posição local: 2 de 6
- Node anterior no nível: `basico/01-modelo-amqp-e-papel-da-exchange` - Modelo AMQP e papel da exchange
- Próximo node no nível: `basico/03-bindings-routing-key-e-destinos` - Bindings, routing key e destinos
- Data da pesquisa: 2026-06-08
- Observações temporais: a documentação oficial consultada está na série RabbitMQ 4.3 em 2026-06-08. O comportamento da default exchange também aparece na especificação AMQP 0-9-1, que é estável e anterior à documentação atual.

## Contrato Extraído do Roadmap

- Papel do node na corrente: remove a principal ambiguidade inicial: publicar com exchange vazia parece publicar em uma fila, mas ainda usa uma direct exchange especial.
- Papel do nível no roadmap tri-level: estabilizar fundamentos, vocabulário indispensável e modelos mentais antes de detalhar bindings, tipos de exchange, filas e decisões intermediárias.
- Pré-requisitos herdados:
  - Entender o fluxo básico `publisher -> exchange -> fila`.
- O que introduz pela primeira vez:
  - Default exchange.
  - Nome vazio da exchange em AMQP 0-9-1.
  - Binding automático pelo nome da fila.
- O que deve cobrir:
  - Explicar que a default exchange sempre existe e usa nome vazio na publicação AMQP 0-9-1.
  - Mostrar o binding automático de cada fila à default exchange usando o nome da fila como routing key.
  - Comparar uso simples da default exchange com uma direct exchange própria para topologias explícitas.
  - Registrar que a default exchange não deve ser tratada como exchange customizada para bindings manuais.
- O que não deve cobrir:
  - Não reensinar direct exchange comum em profundidade; isso fica no node de tipos.
  - Não apresentar a default exchange como solução padrão para topologias de domínio.
  - Não discutir permissões e governance ainda.
- Perguntas do node:
  - Por que `exchange=""` não significa ausência de exchange?
  - Quando uma direct exchange própria é mais clara do que usar a default exchange?
  - O que torna `amq.default` especial em relação a exchanges declaradas pela aplicação?
- Vocabulário conceitual:
  - `default exchange`
  - `amq.default`
  - `empty string exchange name`
  - `routing key` como nome da fila
  - `pre-declared exchange`
- Exemplos e diagramas permitidos:
  - Comparação visual entre publicação na default exchange e publicação em uma exchange `orders.direct`.
  - Cenário conceitual de fila `task_queue` recebendo pela routing key igual ao nome da fila.
- Armadilhas:
  - Dizer que RabbitMQ permite publicar diretamente no consumidor.
  - Usar a default exchange como se fosse uma exchange de domínio com bindings arbitrários.
  - Confundir o nome de permissão `amq.default` com o nome usado na publicação AMQP 0-9-1.
- Critério de domínio: consegue explicar por que a publicação direta em fila é uma conveniência da default exchange, não uma exceção ao modelo de exchanges.
- Handoff: depois da exchange padrão, o próximo node detalha bindings e routing keys como regras que fazem o roteamento acontecer.
- Referências específicas herdadas do contrato: F1 e F2 do roadmap, expandidas neste dump.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto no node anterior:
  - Produtores publicam em exchanges.
  - Exchanges roteiam e não armazenam mensagens como filas.
  - Filas armazenam mensagens e consumidores recebem a partir de filas.
  - O exemplo condutor do node 01 usou `pedido.criado`, faturamento e notificação; este node não deve repetir esse exemplo.
- Conteúdo que este node adiciona:
  - A default exchange é uma direct exchange especial e pré-declarada.
  - O nome de publicação em AMQP 0-9-1 é a string vazia `""`.
  - Cada fila declarada é automaticamente ligada à default exchange usando seu próprio nome como routing key.
  - A aparência de publicar direto na fila é uma conveniência, não um bypass do modelo de exchanges.
- Conteúdo reservado a nodes futuros:
  - `basico/03-bindings-routing-key-e-destinos`: aprofundar binding, routing key, binding key, source, destination e tabela de roteamento vazia.
  - `basico/04-direct-fanout-e-topic`: ensinar direct exchange comum e comparação detalhada com fanout/topic.
  - `intermediario/01-contrato-de-topologia-e-roteamento`: transformar a comparação com direct exchange própria em critério arquitetural de contrato.
  - `intermediario/05-policies-x-arguments-e-permissoes`: discutir permissões, `amq.default` em checks de permissão e governança.
  - `intermediario/03-unroutable-mandatory-e-alternate-exchange`: tratar mensagens sem rota, `mandatory` e alternate exchange.
- Fronteiras:
  - Pode dizer que `amq.default` aparece como nome alternativo em certos contextos, mas o HTML não deve discutir permissões.
  - Pode usar routing key como campo necessário para explicar o endereçamento por nome de fila, mas não deve transformar o node em aula completa de binding key ou padrões de roteamento.
  - Pode comparar com uma direct exchange própria, mas sem ensinar todos os casos de direct exchange.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: define exchanges, default exchange, nome vazio para AMQP 0-9-1, binding automático por nome de fila, ressalva sobre `amq.default` em outros contextos e recomendação de usar uma direct exchange separada quando a aplicação precisar de topologia customizada.  
Tópicos cobertos: exchange como ponto de publicação, default exchange, nome vazio, binding automático, limite de uso como exchange regular.  
Limites da fonte: também cobre tipos e bindings em profundidade; este node usa apenas a parte necessária para a default exchange.

ID: F2  
URL: https://www.rabbitmq.com/tutorials/amqp-concepts  
Tipo: guia oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: explica o modelo AMQP 0-9-1 e afirma que a default exchange faz parecer possível entregar diretamente a filas, embora uma exchange ainda esteja envolvida.  
Tópicos cobertos: modelo AMQP, exchanges, default exchange, binding automático, bind/unbind bloqueado na default exchange, direct exchange.  
Limites da fonte: é guia conceitual amplo; detalhes de operação e erros ficam fora do HTML.

ID: F3  
URL: https://www.rabbitmq.com/assets/files/amqp0-9-1-43a54a005e97180a4fbe6e567a125d84.pdf  
Tipo: especificação  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: AMQP 0-9-1, documento de 2006-2008 publicado pelo RabbitMQ  
Motivo de uso: fonte primária para o modelo em que producer publica em exchange, direct exchange roteia por routing key, a default exchange é direct e todas as filas são automaticamente ligadas à exchange sem nome usando o nome da fila.  
Tópicos cobertos: producer, exchange, message queue, direct exchange, default exchange, binding automático.  
Limites da fonte: não substitui a documentação RabbitMQ atual para nomes e ressalvas operacionais da implementação.

ID: F4  
URL: https://www.rabbitmq.com/docs/publishers  
Tipo: documentação oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta que, em AMQP 0-9-1, a publicação acontece em uma exchange em um channel, e que mensagens roteadas com sucesso são armazenadas em filas.  
Tópicos cobertos: publicação AMQP 0-9-1 em exchanges e fronteira entre publicar, rotear e armazenar.  
Limites da fonte: a página cobre erros de publisher, `mandatory` e confirms; esses pontos ficam apenas como limite no dump.

ID: F5  
URL: https://www.rabbitmq.com/tutorials/tutorial-one-python  
Tipo: tutorial oficial  
Data consultada: 2026-06-08  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: mostra a forma didática clássica de publicar na default exchange usando `exchange=''` e `routing_key` igual ao nome da fila.  
Tópicos cobertos: exemplo mínimo de publicação pela default exchange.  
Limites da fonte: é tutorial com código executável; o HTML deve usar apenas a forma conceitual dos campos, sem virar laboratório ou sequência de comandos.

## Síntese por Fonte

F1 permite afirmar que exchanges são o destino de publicação em AMQP 0-9-1 e que a default exchange é uma direct exchange especial. A fonte é a base principal para dizer que a default exchange sempre existe, usa nome vazio quando é alvo de publicação AMQP 0-9-1, e liga automaticamente cada fila declarada com o nome da fila como routing key. A mesma fonte também sustenta a fronteira: a default exchange não deve ser usada como exchange regular para bindings customizados; para topologia customizada, uma direct exchange separada é mais clara.

F2 permite construir a explicação didática da "publicação direta aparente": publicar com a default exchange e a routing key igual ao nome da fila parece enviar diretamente para a fila, mas tecnicamente a mensagem ainda passa por uma exchange direct especial. F2 também registra que RabbitMQ não permite operações de bind/unbind na default exchange.

F3 confirma que esse comportamento não é apenas convenção de tutorial. A especificação define a direct exchange sem nome público como default exchange para métodos de publicação e exige que todas as message queues sejam automaticamente ligadas a ela usando o nome da fila como routing key.

F4 reforça a continuidade com o node anterior: publishing AMQP 0-9-1 acontece em uma exchange e mensagens roteadas com sucesso são armazenadas em filas. A página também alerta que erros de rota e exchange inexistente existem, mas esses detalhes pertencem ao intermediário.

F5 fornece um recorte concreto para a forma dos campos de publicação: `exchange=''` e `routing_key='hello'`. Como é tutorial executável, o HTML deve transformar isso em leitura conceitual de campos, não em instrução para rodar.

## Afirmações Técnicas Importantes

Afirmação: `exchange=""` em AMQP 0-9-1 não significa ausência de exchange; significa publicar na default exchange, cujo nome de publicação é a string vazia.  
Base: F1, F2, F3  
Condição ou limite: em outros contextos RabbitMQ pode referir a mesma exchange como `amq.default`; o HTML não deve discutir permissões.  
Impacto didático: resolve a ambiguidade que faz a pessoa achar que existe publicação direta real em fila.

Afirmação: a default exchange é uma direct exchange especial e pré-declarada, disponível em cada vhost.  
Base: F1, F3  
Condição ou limite: não é uma exchange declarada pela aplicação.  
Impacto didático: mostra que o comportamento é parte do broker/protocolo, não uma fila com tratamento especial.

Afirmação: ao declarar uma fila, RabbitMQ liga automaticamente essa fila à default exchange usando o nome da fila como routing key.  
Base: F1, F2, F3  
Condição ou limite: o HTML deve usar essa regra sem abrir a aula completa de bindings do próximo node.  
Impacto didático: explica por que uma publicação com routing key igual ao nome da fila encontra a fila.

Afirmação: a publicação na default exchange parece publicação direta em fila porque o nome da fila vira a routing key.  
Base: F2, F5, inferência declarada a partir de F1  
Condição ou limite: a fila precisa existir e estar ligada pela regra automática; este node não deve aprofundar comportamento de mensagens sem rota.  
Impacto didático: dá um modelo positivo para ler código e exemplos simples sem abandonar o modelo de exchanges.

Afirmação: a default exchange não deve ser usada como exchange regular para bindings manuais de topologia de domínio.  
Base: F1, F2  
Condição ou limite: para topologias customizadas, a recomendação é usar uma exchange própria, como uma direct exchange separada quando igualdade exata for suficiente.  
Impacto didático: impede que a conveniência inicial vire desenho arquitetural frágil.

Afirmação: uma direct exchange própria torna explícito o contrato de publicação, enquanto a default exchange acopla a routing key ao nome da fila.  
Base: F1, F2, inferência declarada a partir do contrato do roadmap  
Condição ou limite: a comparação é conceitual; direct exchange comum será ensinada no node 04 e contrato de topologia no intermediário.  
Impacto didático: ajuda a diferenciar uso simples de topologia de domínio sem antecipar nodes futuros.

## Conceitos Essenciais

Conceito: exchange padrão / default exchange  
Explicação simples: exchange direct especial que já existe no broker e serve para o caso em que a publicação usa nome vazio.  
Necessidade no node: é o conceito central que explica a aparente publicação direta em fila.  
Relação com conceitos anteriores: herda o entendimento de que publishers publicam em exchanges e filas armazenam.  
Relação com conceitos futuros: direct exchange comum será detalhada depois; contratos de topologia entram no intermediário.  
Riscos de confusão: achar que nome vazio significa nenhuma exchange ou que ela pode ser customizada como exchange de domínio.  
Fonte base: F1, F2, F3.

Conceito: nome vazio da exchange  
Explicação simples: valor `""` usado no campo de exchange da publicação AMQP 0-9-1 para apontar para a default exchange.  
Necessidade no node: permite ler exemplos e APIs sem concluir que a exchange foi omitida.  
Relação com conceitos anteriores: complementa "publisher publica em exchange".  
Relação com conceitos futuros: `amq.default` e permissões não entram agora.  
Riscos de confusão: trocar o nome vazio da exchange pela routing key vazia.  
Fonte base: F1, F2, F5.

Conceito: binding automático  
Explicação simples: ligação criada pelo broker entre cada fila declarada e a default exchange.  
Necessidade no node: explica por que o nome da fila basta para encontrar a fila.  
Relação com conceitos anteriores: usa binding como ligação já apresentada de forma básica no node 01.  
Relação com conceitos futuros: node 03 aprofunda binding como regra de roteamento.  
Riscos de confusão: achar que a aplicação deve criar ou alterar esse binding manualmente.  
Fonte base: F1, F2, F3.

Conceito: routing key como nome da fila  
Explicação simples: na default exchange, a chave que acompanha a publicação deve bater com o nome da fila desejada.  
Necessidade no node: é a peça que transforma o nome da fila em rota.  
Relação com conceitos anteriores: aprofunda o caminho `publisher -> exchange -> fila` sem abrir todos os tipos de roteamento.  
Relação com conceitos futuros: node 03 separa routing key da publicação e binding key como regra.  
Riscos de confusão: achar que toda routing key deve ser nome de fila em qualquer exchange.  
Fonte base: F1, F2, F3, F5.

Conceito: publicação direta aparente  
Explicação simples: efeito didático em que a API parece enviar para uma fila, mas o broker ainda passa pela default exchange.  
Necessidade no node: é a tensão técnica que dá sentido ao capítulo.  
Relação com conceitos anteriores: resolve a exceção aparente ao modelo AMQP.  
Relação com conceitos futuros: prepara a necessidade de topologias explícitas.  
Riscos de confusão: transformar a conveniência em regra arquitetural.  
Fonte base: F2, F5.

Conceito: direct exchange própria  
Explicação simples: exchange declarada pela aplicação para roteamento explícito por igualdade, em vez de depender do nome da fila como endereço público.  
Necessidade no node: aparece como contraste mínimo com a default exchange.  
Relação com conceitos anteriores: mantém a ideia de exchange como roteador.  
Relação com conceitos futuros: node 04 ensina direct em profundidade; intermediário trata contrato de topologia.  
Riscos de confusão: aprofundar direct agora e repetir o node 04.  
Fonte base: F1, F2.

## Relações Causais e Estruturais

- Se a publicação usa `exchange=""`, então ela mira a default exchange. Condição: publicação AMQP 0-9-1. Base: F1, F2, F3.
- Se a fila `task_queue` foi declarada, RabbitMQ cria automaticamente uma ligação dela com a default exchange usando `task_queue` como routing key. Condição: regra da default exchange; não é binding manual. Base: F1, F2, F3.
- Se o publisher usa `exchange=""` e `routing_key="task_queue"`, a mensagem parece ser enviada para a fila `task_queue`, mas tecnicamente foi publicada na default exchange e roteada pelo binding automático. Condição: fila existente e regra automática válida. Base: F2, F5, inferência de F1.
- Se a topologia precisa representar domínio, contrato ou múltiplos destinos explícitos, depender da default exchange tende a deixar o nome da fila como endereço público. Condição: decisão arquitetural simples; aprofundamento fica no intermediário. Base: F1 e inferência do contrato do roadmap.
- Se a aplicação precisa criar bindings customizados, a default exchange não é o lugar correto. Condição: RabbitMQ não trata a default exchange como exchange regular para esse uso. Base: F1, F2.

## Exemplos Técnicos Possíveis

Exemplo: fila `task_queue` recebendo publicação pela default exchange.  
Mostra: `exchange=""` aponta para a default exchange, enquanto `routing_key="task_queue"` identifica a fila via binding automático.  
Conceitos introduzidos: default exchange, nome vazio, routing key como nome da fila, publicação direta aparente.  
Risco de escopo: virar tutorial de Pika ou comando executável.  
Como manter mínimo: usar snippet conceitual de campos, sem imports, conexão, declaração de fila ou execução.

Exemplo: direct exchange própria `orders.direct` com chave de domínio `orders.created`.  
Mostra: quando o contrato de publicação deve ser explícito e não depender do nome da fila.  
Conceitos introduzidos: contraste entre conveniência simples e topologia explícita.  
Risco de escopo: reensinar direct exchange comum e tipos; manter só comparação de responsabilidade.  
Como manter mínimo: usar tabela ou cards com "endereçamento por fila" versus "contrato explícito".

Exemplo: referência a `amq.default`.  
Mostra: o mesmo objeto pode aparecer com nome de conveniência em alguns contextos, mas a publicação AMQP 0-9-1 usa `""`.  
Conceitos introduzidos: diferença entre nome de publicação e nome operacional.  
Risco de escopo: entrar em permissões/governance, que o contrato proíbe.  
Como manter mínimo: uma nota curta de fronteira, sem explicar regex, write/read/configure ou vhost.

## Obrigações de Concretização Didática

Conceito ou relação: caminho da publicação aparente para `task_queue`.  
Tipo de demanda: ordem e estado.  
Primitiva visual escolhida: componente HTML/CSS.  
Justificativa da primitiva: o leitor precisa ver que `exchange=""` não pula a exchange; a rota passa pela default exchange e pelo binding automático.  
Exemplo candidato: `exchange=""`, `routing_key="task_queue"`, fila `task_queue`.  
Fonte: F1, F2, F3, F5.  
Por que a prosa pode não bastar: a frase "publica direto na fila" é comum e persiste se a rota não for desenhada.  
Risco de virar laboratório ou excesso: médio se a página incluir código cliente completo.  
Como manter conceitual e mínimo: visual de fluxo e snippet de campos, sem programa executável.  
Fronteira com nodes futuros: não explicar todas as propriedades de binding.

Conceito ou relação: diferença entre default exchange e direct exchange própria.  
Tipo de demanda: contraste.  
Primitiva visual escolhida: tabela curta.  
Justificativa da primitiva: a escolha é mais clara quando se compara "endereço igual ao nome da fila" com "contrato de publicação explícito".  
Exemplo candidato: `task_queue` via default exchange versus `orders.direct` com rota de domínio.  
Fonte: F1, F2.  
Por que a prosa pode não bastar: sem contraste, a default exchange pode parecer recomendação geral.  
Risco de virar laboratório ou excesso: alto se listar comandos de declaração e bindings.  
Como manter conceitual e mínimo: comparar intenção, visibilidade e limite, sem ensinar configuração.  
Fronteira com nodes futuros: direct detalhado fica no node 04; contratos ficam no intermediário.

Conceito ou relação: `amq.default` versus nome vazio.  
Tipo de demanda: fronteira.  
Primitiva visual escolhida: callout curto.  
Justificativa da primitiva: é uma ressalva pontual para evitar troca de nomes; tabela ou visual maior daria peso indevido.  
Exemplo candidato: "na publicação AMQP 0-9-1 use `""`; `amq.default` pode aparecer em outros contextos".  
Fonte: F1.  
Por que a prosa pode não bastar: a presença do literal `amq.default` no roadmap pode induzir uso errado como nome de publicação.  
Risco de virar laboratório ou excesso: médio por puxar permissões.  
Como manter conceitual e mínimo: não mencionar configure/write/read nem regras de permissionamento.  
Fronteira com nodes futuros: governança e permissões ficam no intermediário.

## Riscos, Armadilhas e Erros Comuns

- Dizer que RabbitMQ permite publicar diretamente no consumidor. Base: contrato do roadmap, F1, F2.
- Dizer que `exchange=""` é "sem exchange". Base: F1, F2, F3.
- Usar `routing_key=""` quando a intenção é alcançar uma fila pela default exchange. Base: F2, F5.
- Achar que declarar uma fila exige criar manualmente o binding da default exchange. Base: F1, F2, F3.
- Usar a default exchange como topologia de domínio e tornar nomes de fila parte do contrato público do publisher. Base: F1 e inferência do contrato.
- Confundir `amq.default` com o nome que deve ir no campo de exchange ao publicar em AMQP 0-9-1. Base: F1.
- Transformar o contraste com direct exchange própria em aula completa de direct exchange. Base: matriz anti-repetição.

## Limites e Fora de Escopo

Este node explica:

- O que é a default exchange no recorte AMQP 0-9-1.
- Por que o nome de publicação é `""`.
- Como o binding automático por nome de fila cria a aparência de publicação direta.
- Por que a default exchange serve para casos simples, mas não para topologia de domínio com bindings manuais.

Este node apenas menciona como fronteira:

- `amq.default` como nome que pode aparecer fora do campo de publicação.
- Direct exchange própria como alternativa conceitual para topologia explícita.
- Mensagem sem rota quando a fila não existe ou não é alcançada.

Fica para outro node:

- Binding key, source, destination e tabela de roteamento: node 03.
- Direct, fanout e topic em profundidade: node 04.
- Filas, consumers e acknowledgements: node 06.
- `mandatory`, alternate exchange, publisher confirms e mensagens sem rota: intermediário.
- Permissões, policies e governança: intermediário.

Não pertence ao roadmap neste ponto:

- Tutorial de linguagem, comando, setup local, UI de management ou projeto prático.

## Divergências, Versões e Notas Temporais

- Tema temporalmente estável: a default exchange e seu binding automático por nome de fila fazem parte do modelo AMQP 0-9-1 e são descritos tanto pela especificação quanto pela documentação RabbitMQ atual.
- Versão RabbitMQ: as páginas oficiais consultadas estão na série 4.3 em 2026-06-08.
- Diferença de nome: para publicação AMQP 0-9-1, a default exchange usa nome vazio `""`; em outros contextos RabbitMQ pode exibir `amq.default`. O HTML deve tratar isso como fronteira breve.
- Detalhe conscientemente não expandido: mensagens sem rota, erro de exchange inexistente, `mandatory` e alternate exchange existem, mas são nodes intermediários.

## Mapa Fonte -> Tópico

| Tópico | Fontes | Observação |
|---|---|---|
| Exchange como ponto de publicação | F1, F4 | Continuidade com o node 01. |
| Default exchange sempre existente e nome vazio | F1, F2, F3 | Fonte oficial atual e especificação concordam. |
| Binding automático por nome da fila | F1, F2, F3 | Conceito central do node. |
| Publicação direta aparente | F2, F5 | F5 dá forma concreta dos campos, sem virar tutorial. |
| Direct exchange própria como alternativa | F1, F2 | Usado apenas como contraste mínimo. |
| `amq.default` como nome em outros contextos | F1 | Sem discutir permissões. |
| Limite sobre bind/unbind na default exchange | F2 | Usado para reforçar que ela não é exchange regular. |

## Lacunas Pesquisadas e Resolvidas

Lacuna: `exchange=""` significa que a publicação não passa por exchange?  
Busca feita: documentação oficial de exchanges, guia AMQP concepts e especificação AMQP 0-9-1.  
Fonte que resolveu: F1, F2, F3.  
Decisão: o HTML afirma que `""` é o nome de publicação da default exchange.

Lacuna: o binding automático é comportamento RabbitMQ ou exigência AMQP 0-9-1?  
Busca feita: documentação oficial atual e especificação.  
Fonte que resolveu: F1, F2, F3.  
Decisão: o dump registra que a especificação exige a ligação automática à exchange sem nome, e o HTML usa a documentação RabbitMQ atual como linguagem principal.

Lacuna: é correto ensinar `amq.default` como nome de publicação?  
Busca feita: documentação oficial de exchanges.  
Fonte que resolveu: F1.  
Decisão: o HTML diz que `amq.default` pode aparecer em outros contextos, mas o campo de publicação AMQP 0-9-1 usa `""`.

Lacuna: usar a default exchange para topologia customizada é aceitável?  
Busca feita: documentação oficial de exchanges e AMQP concepts.  
Fonte que resolveu: F1, F2.  
Decisão: o HTML recomenda direct exchange própria quando a intenção é topologia explícita, sem detalhar direct.

## Lacunas Remanescentes

Não há lacuna relevante para este node. Os pontos não aprofundados são fronteiras deliberadas do roadmap: `mandatory`, alternate exchange, permissões, direct exchange em profundidade, contratos de routing key e governança.

## Ordem de Introdução Conceitual

Conceito: publicação no modelo AMQP herdado  
Necessidade: lembrar que o node 01 já estabeleceu o fluxo `publisher -> exchange -> fila`.  
Explicação antes do nome: uma mensagem sai do publisher e entra no broker por uma exchange.  
Nomeação: publicação em exchange.  
Depende de: node 01.  
Pode usar depois para: explicar a exceção aparente do nome vazio.  
Não entrar ainda em: confirms, `mandatory`, erros de publicação.  
Visual possível: frase de ponte no lead.  
Fonte base: F1, F4.

Conceito: exchange padrão / default exchange  
Necessidade: explicar a exchange especial que parece ausente.  
Explicação antes do nome: existe uma exchange que o broker já traz pronta para um caminho simples por nome de fila.  
Nomeação: exchange padrão ou default exchange.  
Depende de: publicação em exchange.  
Pode usar depois para: nome vazio e binding automático.  
Não entrar ainda em: permissões, policies, `amq.default` operacional.  
Visual possível: card central do fluxo.  
Fonte base: F1, F2, F3.

Conceito: nome vazio `""`  
Necessidade: ler o campo de publicação sem concluir que não há exchange.  
Explicação antes do nome: a exchange especial é selecionada por um valor que parece ausência de nome.  
Nomeação: nome vazio da exchange.  
Depende de: default exchange.  
Pode usar depois para: snippet conceitual de campos.  
Não entrar ainda em: nomes por vhost ou permissão.  
Visual possível: snippet de campos.  
Fonte base: F1, F2, F5.

Conceito: routing key como nome da fila  
Necessidade: mostrar como a fila é alcançada.  
Explicação antes do nome: além de escolher a default exchange, a publicação carrega o nome da fila desejada como chave de rota.  
Nomeação: routing key.  
Depende de: nome vazio e fila existente.  
Pode usar depois para: binding automático.  
Não entrar ainda em: binding key, padrões, tipos de exchange.  
Visual possível: snippet de campos e fluxo.  
Fonte base: F1, F2, F3, F5.

Conceito: binding automático  
Necessidade: explicar a ligação que transforma nome da fila em rota.  
Explicação antes do nome: quando a fila é criada, o broker já cria a ligação necessária com a exchange especial.  
Nomeação: binding automático.  
Depende de: routing key como nome da fila.  
Pode usar depois para: explicar publicação direta aparente.  
Não entrar ainda em: bindings manuais, source/destination.  
Visual possível: seta entre default exchange e fila.  
Fonte base: F1, F2, F3.

Conceito: publicação direta aparente  
Necessidade: nomear a impressão enganosa depois que o mecanismo já foi mostrado.  
Explicação antes do nome: o publisher informa o nome da fila, mas ainda publica em uma exchange que roteia.  
Nomeação: publicação direta aparente.  
Depende de: default exchange, nome vazio, routing key, binding automático.  
Pode usar depois para: critério de domínio.  
Não entrar ainda em: comandos ou fila inexistente em profundidade.  
Visual possível: callout de leitura correta.  
Fonte base: F2, F5.

Conceito: direct exchange própria  
Necessidade: comparar conveniência simples com topologia explícita.  
Explicação antes do nome: quando o endereço público não deve ser o nome da fila, a aplicação usa uma exchange declarada com um contrato de rota próprio.  
Nomeação: direct exchange própria.  
Depende de: default exchange e routing key como nome da fila.  
Pode usar depois para: tabela de comparação.  
Não entrar ainda em: fanout, topic, binding key detalhada.  
Visual possível: tabela curta.  
Fonte base: F1, F2.

Conceito: `amq.default`  
Necessidade: evitar troca entre nome operacional e nome de publicação.  
Explicação antes do nome: a mesma exchange pode aparecer com outro identificador em contextos de administração, mas isso não muda o campo da publicação AMQP 0-9-1.  
Nomeação: `amq.default`.  
Depende de: nome vazio.  
Pode usar depois para: nota de fronteira.  
Não entrar ainda em: permissões, governance, vhost.  
Visual possível: callout curto.  
Fonte base: F1.

## Insumos para o Ledger Editorial

Conceitos que podem aparecer no HTML:

- Exchange padrão / default exchange: permitido em título e H1 por ser o label do node; no corpo, explicar como exchange especial antes de depender do termo.
- Nome vazio: aliases `""`, string vazia, empty string exchange name; precisa aparecer depois de default exchange.
- Routing key como nome da fila: aliases `routing_key`, `routing key`, chave de roteamento; permitido apenas como campo necessário para a default exchange.
- Binding automático: aliases ligação automática, vínculo automático, regra automática; permitido após routing key.
- Publicação direta aparente: aliases parece publicar direto, aparência de envio direto, conveniência de envio para fila; permitido depois do mecanismo.
- Direct exchange própria: permitido como contraste curto; não aprofundar direct.
- `amq.default`: permitido apenas em nota curta sobre nome fora do campo de publicação.
- Fila `task_queue`: exemplo condutor permitido.

Conceitos permitidos só no dump:

- `mandatory`: pertence ao intermediário.
- `basic.return`: pertence ao intermediário.
- Alternate Exchange / AE: pertence ao intermediário.
- Publisher confirms: pertence ao intermediário.
- Permissões `configure`, `write`, `read`: pertencem ao intermediário.
- Binding key detalhada: pertence ao node 03.
- Direct/fanout/topic como tipos comparados: pertence ao node 04.

Conceitos reservados a nodes futuros:

- Binding key, source exchange, destination queue, destination exchange: node 03. Menção no HTML atual deve ser evitada ou ficar como "ligação automática", sem detalhar.
- Direct exchange comum em profundidade: node 04. Menção permitida apenas no contraste de alternativa.
- Contrato de routing key e ownership: intermediário/01. Menção permitida como "topologia explícita", sem desenho arquitetural completo.
- Permissões e governance: intermediário/05. Nenhuma explicação visível.
- Mensagens sem rota, `mandatory`, AE: intermediário/03. Nenhuma explicação visível.

Títulos de fontes que carregam vocabulário técnico:

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Exchanges | Sim | `RabbitMQ - Exchanges` |
| F2 | AMQP 0-9-1 Model | Sim | `RabbitMQ - AMQP 0-9-1 Model Explained` |
| F3 | Advanced Message Queuing Protocol Specification | Sim | `AMQP 0-9-1 specification` |
| F4 | Publishers | Sim, se publicação já preparada | `RabbitMQ - Publishers` |
| F5 | Hello world tutorial | Sim, se usado como fonte de forma dos campos | `RabbitMQ - Hello World tutorial` |

## Candidatos de Narrativa para o HTML

Pergunta-motor possível:
- Como uma API consegue parecer que envia para a fila `task_queue` se o modelo AMQP diz que o publisher publica em uma exchange?

Situação de abertura possível:
- O leitor encontra um snippet com `exchange=""` e `routing_key="task_queue"` e conclui que a exchange sumiu. O node acompanha esse par de campos até mostrar a exchange que ficou implícita.

Transformação acompanhada:
- A publicação começa com dois campos, passa pela default exchange, encontra o binding automático criado quando a fila nasceu e chega à fila `task_queue`.

Narrativa dominante:
- Construção incremental com contraste pontual.

Por que esta narrativa combina com o node:
- O node existe para corrigir uma exceção aparente sem começar por negações. A melhor ordem é mostrar os campos, revelar a exchange especial e só depois nomear a aparência direta.

Exemplo condutor escolhido:
- Fila `task_queue`, diferente do exemplo de pedidos/faturamento/notificação do node 01.

Momento de nomeação dos conceitos:
- Nomear default exchange depois de retomar que a publicação precisa de uma exchange.
- Nomear nome vazio depois de mostrar que a exchange existe mas é selecionada por `""`.
- Nomear routing key como nome da fila depois de apresentar a fila desejada.
- Nomear binding automático depois de mostrar a ligação criada pelo broker.
- Nomear publicação direta aparente depois de o fluxo estar completo.

Abstrações que precisam virar visual:
- Fluxo da publicação pela default exchange.
- Comparação entre default exchange e direct exchange própria.
- Nota breve sobre `amq.default` versus `""`.

Contrastes realmente necessários:
- Nome vazio não é ausência de exchange.
- Default exchange é conveniência simples, não topologia de domínio.
- `amq.default` não é o nome usado no campo de publicação AMQP 0-9-1.

Riscos, limites e armadilhas que devem ficar no bastidor:
- Lista completa de erros de publisher.
- Permissões.
- Declaração de fila e comandos de execução.
- Direct exchange em profundidade.

Risco de tom corretivo:
- Começar com "não publique direto na fila" deixaria a página defensiva. Melhor acompanhar o par de campos e mostrar como ele funciona.

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
