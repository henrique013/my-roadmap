# Research dump - Unroutable, mandatory e Alternate Exchange

## Metadados do Node

- Roadmap de origem: Exchanges no RabbitMQ
- Caminho do `roadmap.html`: `.tmp/roadmaps/rabbitmq-exchanges/roadmap.html`
- Nível do node: intermediario
- `node_id`: `intermediario/03-unroutable-mandatory-e-alternate-exchange`
- Slug do node: `03-unroutable-mandatory-e-alternate-exchange`
- Label do node: Unroutable, mandatory e Alternate Exchange
- Posição numérica local no nível: 03 de 07
- Node anterior e próximo do mesmo nível para incrementalidade: anterior `intermediario/02-broadcast-vs-consumidores-competindo`; próximo `intermediario/04-dead-letter-exchanges-e-retry-conceitual`
- Node anterior e próximo na sequência global do roadmap: anterior `intermediario/02-broadcast-vs-consumidores-competindo`; próximo `intermediario/04-dead-letter-exchanges-e-retry-conceitual`
- Data da pesquisa: 2026-06-10
- Observações temporais: documentação oficial consultada na série RabbitMQ 4.3. O recorte técnico é AMQP 0-9-1 em RabbitMQ, com a referência de protocolo AMQP 0-9-1 usada para `basic.publish`, `mandatory` e `basic.return`.

## Contrato Extraído do Roadmap

- Papel do node na corrente: cobre o que acontece quando a exchange não encontra binding compatível e como publishers e AEs lidam com esse caso.
- Papel do nível no roadmap tri-level: arquitetura, relações, decisões e trade-offs.
- Pré-requisitos herdados:
  - Entender bindings e contrato de routing.
  - Entender o node anterior: a decisão entre múltiplas filas e múltiplos consumers já separou cópia por fila de competição dentro de uma fila.
- Introduz pela primeira vez:
  - Unroutable message.
  - `mandatory` flag.
  - `basic.return`.
  - Alternate Exchange.
  - Fallback de roteamento.
- Deve cobrir:
  - Explicar descarte padrão ou republish para AE quando `mandatory=false` e não há rota.
  - Explicar retorno ao publisher quando `mandatory=true` e há handler de retorno.
  - Comparar mandatory com AE: sinal ao publisher versus roteamento alternativo.
  - Mostrar usos de AE para migração de routing keys, coleta de órfãs e semântica fallback.
- Não deve cobrir:
  - Não confundir AE com DLX; DLX fica no próximo node.
  - Não afirmar que mandatory garante entrega ao consumidor.
  - Não tratar AE como solução para falha de processamento dentro da fila.
- Perguntas do node:
  - O que acontece com uma mensagem sem binding compatível?
  - Quando AE é melhor que depender só de retorno ao publisher?
  - Por que mandatory não prova que o consumer processou a mensagem?
- Vocabulário conceitual:
  - unroutable
  - `mandatory`
  - `basic.return`
  - alternate exchange
  - fallback routing
  - routing miss
- Exemplos e diagramas permitidos:
  - Cenário conceitual de migração de `orders.created.v1` para `orders.created.v2` com AE capturando órfãs.
  - Tabela comparando descarte, retorno e AE.
- Armadilhas:
  - Usar AE para mensagens rejeitadas pelo consumer.
  - Não configurar handler de retorno ao usar mandatory.
  - Ignorar métricas de unroutable e descobrir perda tarde demais.
- Critério de domínio: consegue explicar os três destinos possíveis de uma publicação sem rota: descarte, retorno ao publisher ou roteamento para AE configurada.
- Handoff: com falha de roteamento inicial clara, o próximo node trata mensagens que saem de filas por eventos posteriores.
- Referências específicas do contrato:
  - F3 `https://www.rabbitmq.com/docs/publishers`: regras de publicação sem rota e `mandatory`.
  - F8 `https://www.rabbitmq.com/docs/ae`: definição e configuração de Alternate Exchanges.
  - F1 `https://www.rabbitmq.com/docs/exchanges`: exchange como roteador e tipos de exchange.

## Matriz Anti-Repetição Aplicável

- Conteúdo já coberto:
  - `basico/01-modelo-amqp-e-papel-da-exchange`: exchange como roteador, não armazenamento.
  - `basico/03-bindings-routing-key-e-destinos`: binding liga exchange a destino e routing key participa da decisão.
  - `basico/04-direct-fanout-e-topic`: tipos clássicos de exchange e roteamento por tipo.
  - `intermediario/01-contrato-de-topologia-e-roteamento`: contrato de publicação separa producer, topologia e consumidores.
  - `intermediario/02-broadcast-vs-consumidores-competindo`: múltiplas filas criam cópias independentes; múltiplos consumers na mesma fila dividem trabalho.
- Conteúdo que pode ser reutilizado:
  - A exchange recebe publicação e tenta rotear para destinos ligados por bindings.
  - Routing key já é vocabulário conhecido.
  - O publisher publica contra um contrato de exchange e routing, não contra uma lista de filas no código.
- Conteúdo reservado a nodes futuros:
  - `intermediario/04-dead-letter-exchanges-e-retry-conceitual`: mensagens que já estavam em filas e saem por rejeição, expiração, limite ou retry.
  - `intermediario/05-policies-x-arguments-e-permissoes`: governança de políticas, argumentos opcionais e permissões.
  - `intermediario/07-publisher-confirms-e-confiabilidade`: aceite pelo broker, persistência e confirms em profundidade.
  - `avancado/01-diagnostico-de-roteamento-e-observabilidade`: investigação operacional ampla com métricas.
- Exemplos que não devem ser repetidos:
  - Não refazer o contraste principal do node anterior entre e-mail/auditoria/analytics versus workers equivalentes.
  - Não repetir aula de direct, fanout e topic.
  - Não usar processamento falho dentro da fila como exemplo condutor; isso pertence ao próximo node.
- Definições que podem ser tratadas como pré-requisito:
  - Binding é a relação que conecta exchange a destino.
  - Routing key já é linguagem compartilhada no contrato de publicação.
  - Fila é o ponto de acúmulo para entrega posterior ao consumidor.
- Termos que ainda precisam ser introduzidos no HTML:
  - Sem rota.
  - Mensagem sem rota.
  - `mandatory`.
  - Retorno ao publisher.
  - `basic.return`.
  - Alternate Exchange.
  - Roteamento de fallback.

## Fontes Pesquisadas

ID: F1  
URL: https://www.rabbitmq.com/docs/publishers  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta o comportamento de publicações em AMQP 0-9-1 quando uma mensagem não pode ser roteada, incluindo descarte, Alternate Exchange e retorno ao publisher com `mandatory=true`.  
Tópicos cobertos: publicação em exchanges, erro ao publicar em exchange inexistente, mensagens sem rota, `mandatory`, Alternate Exchange, métricas e troubleshooting de routing.  
Limites da fonte: foca publishers; processamento por consumidores e mensagens que saem de filas usam fontes próprias.

ID: F2  
URL: https://www.rabbitmq.com/docs/ae  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta como Alternate Exchanges são definidas e como mensagens não roteadas por uma exchange configurada com AE são republicadas para a AE.  
Tópicos cobertos: definição de AE por policy ou argumento de exchange, permissões, funcionamento encadeado de AE, relação com `mandatory`.  
Limites da fonte: traz exemplos de comando e código, mas o HTML usa apenas leitura conceitual e não transforma o node em roteiro operacional.

ID: F3  
URL: https://www.rabbitmq.com/docs/exchanges  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta que exchanges são onde AMQP 0-9-1 publishers publicam e que o tipo da exchange e as propriedades de binding implementam a lógica de roteamento.  
Tópicos cobertos: papel das exchanges, destinos de roteamento, tipos de exchange, direct, fanout, topic e exchange padrão.  
Limites da fonte: não detalha `basic.return`; para esse comportamento usa-se a página de publishers e a referência AMQP.

ID: F4  
URL: https://raw.githubusercontent.com/rabbitmq/amqp-0.9.1-spec/main/docs/amqp-0-9-1-reference.md  
Tipo: especificação/referência AMQP 0-9-1 arquivada pelo RabbitMQ  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: AMQP 0-9-1; arquivo no repositório `rabbitmq/amqp-0.9.1-spec`  
Motivo de uso: sustenta a semântica protocolar de `basic.publish`, `mandatory` e `basic.return`.  
Tópicos cobertos: publicar em exchange, routing key, `mandatory`, retorno por Return method.  
Limites da fonte: é referência de protocolo; extensões e comportamento específico do RabbitMQ são confirmados na documentação RabbitMQ 4.3.

ID: F5  
URL: https://www.rabbitmq.com/docs/confirms  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta a fronteira entre confirmação ao publisher, acknowledgements de consumidores e processamento.  
Tópicos cobertos: publisher confirms, consumer acknowledgements, independência entre os mecanismos, entrega e processamento do consumidor.  
Limites da fonte: publisher confirms em profundidade são reservados para `intermediario/07-publisher-confirms-e-confiabilidade`.

ID: F6  
URL: https://www.rabbitmq.com/docs/dlx  
Tipo: documentação oficial RabbitMQ 4.3  
Data consultada: 2026-06-10  
Versão ou data da fonte, quando relevante: RabbitMQ 4.3  
Motivo de uso: sustenta a fronteira com o próximo node: dead-lettering acontece a partir de eventos em filas, não na tentativa inicial de roteamento pela exchange principal.  
Tópicos cobertos: eventos que dead-letter mensagens, configuração de DLX, roteamento de mensagens dead-lettered.  
Limites da fonte: usada apenas como fronteira; o node atual não ensina DLX nem retry.

## Síntese por Fonte

- F1 permite afirmar que, em AMQP 0-9-1, uma mensagem publicada em uma exchange que não consegue ser roteada para nenhuma fila pode seguir dois caminhos principais na documentação de publishers: se `mandatory=false`, o padrão é descarte ou republish para uma Alternate Exchange configurada; se `mandatory=true`, a mensagem é retornada ao publisher e o publisher precisa ter handler para lidar com esse retorno.
- F2 permite afirmar que uma Alternate Exchange é uma exchange configurada como rota alternativa para publicações que a exchange original não conseguiu rotear. A documentação também informa que policy é a forma recomendada de definir AE, enquanto argumento de declaração é permitido, mas desencorajado como acoplamento rígido.
- F3 permite afirmar que a falha discutida neste node acontece no momento em que a exchange tenta aplicar sua lógica de roteamento, que depende de tipo de exchange e bindings. A fonte reforça que não é problema de consumers competindo.
- F4 permite afirmar que `mandatory` é um campo de `basic.publish` e que, quando setado, orienta o servidor a retornar uma mensagem sem rota por meio do Return method; quando zero, a referência de protocolo descreve descarte silencioso.
- F5 permite afirmar que retorno de publicação, publisher confirms e acknowledgements de consumidor não são a mesma coisa. Uma publicação roteada ou retornada ainda não prova que uma aplicação consumidora processou a mensagem.
- F6 permite estabelecer fronteira: dead-lettering envolve mensagens que saem de uma fila por rejeição, expiração, limite ou outros eventos posteriores; isso não é o mesmo que a exchange inicial não encontrar rota.

## Afirmações Técnicas Importantes

Afirmação: No recorte AMQP 0-9-1, publishers publicam em exchanges; a exchange usa seu tipo e seus bindings para tentar rotear a mensagem para filas, streams ou outras exchanges.  
Base: F3  
Condição ou limite: o roadmap usa AMQP 0-9-1 e RabbitMQ 4.3; outros protocolos têm destinos e retornos diferentes.  
Impacto didático: prepara o ponto exato onde a mensagem pode ficar sem rota.

Afirmação: Uma mensagem sem rota é uma publicação para a qual a exchange alvo não encontra nenhum destino compatível com a regra de roteamento vigente.  
Base: F1, F3, F4; inferência declarada a partir de exchanges como roteadores e da referência de `mandatory` para mensagens que não podem ser roteadas a uma fila.  
Condição ou limite: publicar em uma exchange inexistente é outro erro; não é o mesmo caso de exchange existente sem destino compatível.  
Impacto didático: separa erro de topologia inexistente de routing miss.

Afirmação: Com `mandatory=false`, que é o padrão descrito pela documentação RabbitMQ, uma publicação sem rota é descartada ou republicada para uma Alternate Exchange configurada.  
Base: F1, F2, F4  
Condição ou limite: F4 descreve descarte quando a flag é zero; F1 e F2 acrescentam o comportamento RabbitMQ com AE configurada.  
Impacto didático: mostra o caminho silencioso e o caminho de fallback antes de discutir retorno ao publisher.

Afirmação: Com `mandatory=true`, uma publicação sem rota é retornada ao publisher, mas o publisher precisa ter handler de retorno para observar e agir sobre isso.  
Base: F1, F4  
Condição ou limite: o retorno sinaliza falha de roteamento, não processamento por consumidor.  
Impacto didático: evita a armadilha de tratar `mandatory` como garantia de entrega final.

Afirmação: Uma Alternate Exchange resolve o problema pelo lado da topologia: a mensagem continua sendo roteada, agora pela exchange alternativa, e por isso conta como roteada para o propósito de `mandatory`.  
Base: F2  
Condição ou limite: se a AE não existir ou não conseguir rotear, a cadeia pode terminar sem destino; a documentação menciona warning quando AE configurada não existe e encadeamento até sucesso, fim da cadeia ou ciclo.  
Impacto didático: diferencia sinal ao publisher de fallback operacional.

Afirmação: AE e mensagens dead-lettered pertencem a momentos diferentes do fluxo. AE atua quando a exchange inicial não encontra rota; dead-lettering atua depois, quando uma mensagem já está em uma fila e sai por rejeição, expiração, limite ou caso equivalente.  
Base: F2, F6  
Condição ou limite: o HTML deve usar essa fronteira como aviso curto, sem ensinar DLX.  
Impacto didático: preserva a progressão para o próximo node.

Afirmação: Métricas e inspeção de bindings ajudam a detectar publicações sem rota, mas o node atual não deve virar tutorial de diagnóstico.  
Base: F1  
Condição ou limite: diagnóstico aprofundado fica para `avancado/01-diagnostico-de-roteamento-e-observabilidade`.  
Impacto didático: permite mencionar que perda silenciosa precisa aparecer em telemetria, sem abrir outro tema.

## Conceitos Essenciais

### Mensagem sem rota

- Nome técnico: unroutable message.
- Explicação em linguagem simples: uma publicação chega à exchange, mas nenhuma relação de routing aponta para uma fila, stream ou exchange destino compatível.
- Por que é necessária: é o centro do node; sem esse estado, `mandatory` e AE parecem opções abstratas.
- Relação com conceitos anteriores: depende de exchange, binding e routing key já apresentados.
- Relação com conceitos futuros: prepara diagnóstico de routing, mas não entra em observabilidade avançada.
- Riscos de confusão: confundir com consumer lento, fila cheia ou processamento rejeitado.
- Fonte base: F1, F3, F4.

### `mandatory`

- Nome técnico: `mandatory` flag.
- Explicação em linguagem simples: uma opção de publicação que pede ao broker para devolver ao publisher uma mensagem que não encontrou rota.
- Por que é necessária: define quando o publisher recebe sinal direto da falha de roteamento.
- Relação com conceitos anteriores: usa routing key e exchange do contrato de publicação.
- Relação com conceitos futuros: não substitui publisher confirms nem acknowledgements de consumidor.
- Riscos de confusão: achar que `mandatory=true` prova que o consumidor processou a mensagem.
- Fonte base: F1, F4, F5.

### Retorno ao publisher

- Nome técnico: `basic.return`.
- Explicação em linguagem simples: o broker envia a mensagem de volta ao publisher junto com motivo e metadados de rota quando `mandatory` pediu retorno.
- Por que é necessária: mostra o mecanismo observável que transforma falha de routing em sinal para a aplicação publicadora.
- Relação com conceitos anteriores: acontece na publicação, antes do consumo.
- Relação com conceitos futuros: não é publisher confirm; confirms ficam para node posterior.
- Riscos de confusão: configurar `mandatory` mas não registrar handler de retorno.
- Fonte base: F1, F4.

### Alternate Exchange

- Nome técnico: Alternate Exchange.
- Explicação em linguagem simples: exchange alternativa configurada para receber mensagens que a exchange principal não conseguiu rotear.
- Por que é necessária: oferece fallback topológico para capturar órfãs, migração de routing keys e rotas genéricas.
- Relação com conceitos anteriores: continua usando exchange, binding e filas; não inventa novo tipo de destino.
- Relação com conceitos futuros: a governança de policies e x-arguments fica para node posterior.
- Riscos de confusão: usar AE como se corrigisse rejeição de consumidor ou falha dentro da fila.
- Fonte base: F2.

### Roteamento de fallback

- Nome técnico: fallback routing.
- Explicação em linguagem simples: quando a rota normal falha, uma rota alternativa recebe a mensagem para análise, migração ou tratamento genérico.
- Por que é necessária: organiza os usos arquiteturais de AE sem reduzir tudo a "evitar descarte".
- Relação com conceitos anteriores: depende de contrato de routing e de topologia explícita.
- Relação com conceitos futuros: pode gerar sinais para diagnóstico avançado, mas não é observabilidade completa.
- Riscos de confusão: deixar fallback amplo demais e esconder erro de contrato por muito tempo.
- Fonte base: F1, F2.

## Relações Causais e Estruturais

- Relação: exchange existente + routing key sem binding compatível -> publicação sem rota.
  - Condição: a exchange existe e aceita a publicação; o problema está na ausência de destino compatível.
  - Base: F1, F3, F4.
- Relação: publicação sem rota + `mandatory=false` + sem AE configurada -> descarte silencioso do ponto de vista do publisher.
  - Condição: sem rota alternativa configurada; métricas podem denunciar o padrão de perda.
  - Base: F1, F4.
- Relação: publicação sem rota + `mandatory=true` -> retorno ao publisher, desde que a aplicação trate o retorno.
  - Condição: o handler de retorno é responsabilidade do publisher ou da biblioteca/integração usada.
  - Base: F1, F4.
- Relação: publicação sem rota + AE configurada -> republish para a AE.
  - Condição: a AE precisa existir e também precisa ter rota útil; caso contrário, a cadeia pode terminar sem destino.
  - Base: F2.
- Relação: mensagem roteada para AE -> conta como roteada para o propósito de `mandatory`.
  - Condição: a fonte oficial afirma que o comportamento de AE pertence ao roteamento e que a mensagem permanece inalterada.
  - Base: F2.
- Relação: publicação retornada ou roteada -> não prova processamento por consumidor.
  - Condição: acknowledgements de consumidor são mecanismo separado.
  - Base: F5.

## Exemplos Técnicos Possíveis

### Migração de routing key de pedidos

- Exemplo: um producer começa a emitir `orders.created.v2`, mas parte da topologia ainda está ligada a `orders.created.v1`. Durante a transição, publicações com a key nova podem não encontrar binding na exchange principal.
- Mostra: routing miss, descarte, retorno com `mandatory`, e AE como caixa de órfãs controlada.
- Conceitos que ajuda a introduzir: mensagem sem rota, `mandatory`, retorno ao publisher, AE, fallback.
- Riscos de escopo: pode virar guia de versionamento de eventos; manter no nível de routing key e binding.
- Por que não vira laboratório: não exige comandos nem criação real de exchanges; é um fluxo conceitual.

### Coleta de órfãs de roteamento

- Exemplo: uma exchange de domínio envia qualquer publicação sem rota para uma fila de inspeção ligada à AE, para que a equipe veja padrões de routing que ficaram fora do contrato esperado.
- Mostra: fallback como observabilidade mínima e não como sucesso de negócio.
- Conceitos que ajuda a introduzir: AE, fallback routing, limite de `mandatory`.
- Riscos de escopo: diagnóstico operacional amplo fica no avançado.
- Por que não vira laboratório: não entra em dashboards, comandos ou tuning.

## Obrigações de Concretização Didática

Conceito ou relação: três caminhos de uma publicação sem rota  
Tipo de demanda: ordem | contraste | fronteira  
Primitiva visual escolhida: componente HTML/CSS  
Justificativa da primitiva: a pessoa precisa ver a decisão acontecer depois da tentativa de roteamento, não apenas ler três bullets.  
Exemplo candidato: exchange de pedidos tenta rotear `orders.created.v2`; sem binding compatível, a publicação pode ser descartada, retornada ou enviada para AE.  
Fonte: F1, F2, F4  
Por que a prosa pode não bastar: os caminhos são parecidos no texto, mas têm responsabilidades diferentes.  
Risco de virar laboratório ou excesso: não mostrar comando nem código de client.  
Como manter conceitual e mínimo: cards de fluxo com uma frase por caminho.  
Fronteira com nodes futuros: não entrar em confirms, DLX ou diagnóstico avançado.

Conceito ou relação: `mandatory` versus AE  
Tipo de demanda: contraste  
Primitiva visual escolhida: tabela curta  
Justificativa da primitiva: a comparação é central para a decisão arquitetural e cabe em dimensões estáveis: quem observa, o que acontece com a mensagem e risco.  
Exemplo candidato: `mandatory` avisa a aplicação publicadora; AE continua o roteamento para uma área de fallback.  
Fonte: F1, F2, F4  
Por que a prosa pode não bastar: sem comparação lado a lado, o leitor pode tratar ambos como "garantia de entrega".  
Risco de virar laboratório ou excesso: não listar APIs por biblioteca nem comandos.  
Como manter conceitual e mínimo: quatro linhas, sem opções de configuração detalhadas.  
Fronteira com nodes futuros: `publisher confirms` fica apenas como fronteira curta.

Conceito ou relação: forma mínima da publicação conceitual com `mandatory` e fallback  
Tipo de demanda: forma | risco  
Primitiva visual escolhida: snippet conceitual curto com highlight semântico  
Justificativa da primitiva: os nomes `exchange`, `routing_key`, `mandatory` e `alternate-exchange` são campos/argumentos que precisam ser vistos como forma, mas sem virar comando executável.  
Exemplo candidato: pseudo-configuração não executável de uma publicação e uma exchange com fallback.  
Fonte: F1, F2, F4  
Por que a prosa pode não bastar: `mandatory` parece regra global se não aparecer no contexto de publicação, enquanto AE é propriedade da exchange.  
Risco de virar laboratório ou excesso: não usar sintaxe real de biblioteca, `rabbitmqctl` ou `rabbitmqadmin`.  
Como manter conceitual e mínimo: bloco marcado como recorte conceitual, com placeholders de domínio e leitura logo abaixo.  
Fronteira com nodes futuros: não explicar policies, argumentos opcionais ou permissões em profundidade.

## Riscos, Armadilhas e Erros Comuns

- Risco: tratar `mandatory=true` como confirmação de processamento.
  - Base: F1, F4, F5.
  - Correção narrativa: mostrar que o retorno acontece antes do consumo e que acknowledgements de consumidor são outro mecanismo.
- Risco: habilitar `mandatory` mas não registrar handler de retorno.
  - Base: F1.
  - Correção narrativa: explicar que o sinal existe para a aplicação que sabe ouvi-lo.
- Risco: usar AE para mensagens rejeitadas por consumer.
  - Base: F2, F6.
  - Correção narrativa: separar falha de rota inicial de saída posterior da fila.
- Risco: usar AE ampla demais e esconder quebra de contrato.
  - Base: F1, F2; inferência declarada a partir de fallback capturando tudo que a rota principal não aceitou.
  - Correção narrativa: tratar AE como área de fallback observável, não como lixeira invisível.
- Risco: publicar em exchange inexistente e chamar isso de mensagem sem rota.
  - Base: F1, F4.
  - Correção narrativa: separar "exchange não existe" de "exchange existe, mas não encontrou binding compatível".

## Limites e Fora de Escopo

- Este node explica:
  - como uma publicação fica sem rota;
  - o que acontece com `mandatory=false`;
  - o que muda com `mandatory=true`;
  - como uma AE recebe fallback de roteamento;
  - por que AE e `mandatory` resolvem problemas diferentes.
- Este node menciona apenas como fronteira:
  - mensagens que já estavam em fila e saem dela depois;
  - publisher confirms;
  - métricas de unroutable.
- Fica para outro node:
  - dead-lettering, retry e comportamento posterior à fila;
  - policies, x-arguments e permissões;
  - confirms e confiabilidade de publicação;
  - diagnóstico operacional avançado.
- Não pertence ao roadmap atual:
  - laboratório de configuração RabbitMQ;
  - comandos de administração;
  - comparação entre bibliotecas de client.

## Divergências, Versões e Notas Temporais

- A documentação consultada está na série RabbitMQ 4.3, indicada nas páginas oficiais.
- A referência AMQP 0-9-1 está arquivada no repositório oficial `rabbitmq/amqp-0.9.1-spec`; ela serve para semântica protocolar, enquanto comportamento específico do RabbitMQ com AE usa documentação RabbitMQ.
- A página de AE recomenda policy para definir AE e desencoraja argumentos fornecidos por client, mas o aprofundamento de policies é deliberadamente adiado para `intermediario/05-policies-x-arguments-e-permissoes`.
- A página de publishers também fala de publisher confirms, connection recovery e troubleshooting; esses tópicos foram usados apenas como fronteira.

## Ordem de Introdução Conceitual

1. Relembrar a situação: o producer publica em uma exchange com routing key conhecida, e a exchange tenta aplicar bindings.
2. Mostrar a falha concreta: a key nova `orders.created.v2` ainda não tem destino compatível.
3. Nomear "mensagem sem rota" e "routing miss" depois de mostrar a falha.
4. Mostrar o caminho padrão: sem pedido de retorno e sem fallback, a publicação some do caminho de entrega.
5. Nomear `mandatory` como opção de publicação que pede retorno quando não há rota.
6. Nomear `basic.return` como o retorno observável enviado ao publisher.
7. Mostrar AE como recurso da exchange, não da mensagem, que dá uma rota alternativa para o que a rota principal não aceitou.
8. Comparar `mandatory` e AE depois que ambos estão preparados.
9. Fechar a fronteira: isso é falha de rota inicial, não falha de processamento dentro da fila.

## Insumos para o Ledger Editorial

- Conceitos permitidos no HTML:
  - Mensagem sem rota.
  - Routing miss.
  - `mandatory`.
  - Retorno ao publisher.
  - `basic.return`.
  - Alternate Exchange.
  - Roteamento de fallback.
  - Handler de retorno.
  - Métricas de publicações sem rota, apenas como menção curta.
- Conceitos permitidos só no dump:
  - AMQP 1.0, MQTT e STOMP.
  - `immediate` flag.
  - comandos `rabbitmqctl` e `rabbitmqadmin`.
- Conceitos reservados a nodes futuros:
  - Saída posterior da fila por rejeição, expiração ou limite.
  - Policies e x-arguments.
  - Publisher confirms em profundidade.
  - Diagnóstico operacional avançado.
- Títulos de fontes e termos de referência:
  - "Publishers" pode aparecer como "Documentação de publishers".
  - "Alternate Exchanges" pode aparecer depois de AE estar preparada.
  - "Exchanges" é pré-requisito e pode aparecer visível.
  - "AMQP 0-9-1 Complete Reference Guide" pode aparecer como "Referência AMQP 0-9-1".
  - "Consumer Acknowledgements and Publisher Confirms" só deve aparecer como "Documentação sobre confirmações e acknowledgements", com nota curta de fronteira.
  - "Dead Letter Exchanges" deve ficar fora das referências visíveis do HTML; se necessário, aparece apenas no dump.

## Candidatos de Narrativa para o HTML

### Candidato A - A key nova que ninguém reconhece

- Situação de abertura: durante uma migração, o producer passa a publicar `orders.created.v2`, mas a topologia ainda só reconhece a key antiga.
- Transformação acompanhada: a mesma publicação atravessa três desenhos possíveis: sem retorno, com `mandatory`, com AE.
- Narrativa dominante: processo com contraste progressivo.
- Exemplo técnico condutor: evento de pedido com routing key versionada.
- Momento de nomeação: "sem rota" aparece depois de a exchange não achar binding; `mandatory` aparece quando o publisher precisa saber; AE aparece quando a topologia precisa capturar o desvio.
- Risco de tom corretivo: moderado, porque há muitas negações possíveis. Deve abrir mostrando o fluxo antes de avisar o que não é.
- Escolha: usar este candidato.

### Candidato B - Auditoria de publicações órfãs

- Situação de abertura: métricas mostram mensagens sem rota e a equipe precisa descobrir se é erro de publisher ou topologia.
- Transformação acompanhada: diagnóstico de sinais.
- Narrativa dominante: diagnóstico.
- Risco de escopo: invade `avancado/01-diagnostico-de-roteamento-e-observabilidade`.
- Escolha: não usar como dominante; aproveitar só para explicar por que fallback precisa ser observável.

### Candidato C - Contrato de publisher versus contrato de topology

- Situação de abertura: publisher acha que enviou, topologia não recebeu.
- Transformação acompanhada: separação de responsabilidades.
- Narrativa dominante: fronteira conceitual.
- Risco de escopo: pode repetir demais `intermediario/01-contrato-de-topologia-e-roteamento`.
- Escolha: usar como camada de fechamento, não como abertura.

## Projeto Narrativo Escolhido

- Pergunta-motor: o que uma aplicação deve esperar quando publica uma mensagem que a exchange existente não consegue ligar a nenhum destino?
- Situação de abertura: migração de routing key de `orders.created.v1` para `orders.created.v2`.
- Transformação acompanhada: a publicação deixa de ser apenas "enviada" e passa a ter três resultados distintos no ponto de roteamento.
- Narrativa dominante: processo com contraste progressivo.
- Exemplo técnico condutor: evento de pedido com key nova durante migração.
- Visual necessário: fluxo de três caminhos e tabela comparando responsabilidade de `mandatory` e AE.
- Snippet necessário: recorte conceitual para mostrar que `mandatory` vive na publicação e `alternate-exchange` vive na exchange.
- Fechamento desejado: dominar o node significa localizar a falha no ponto certo do fluxo: antes da fila, na decisão de roteamento da exchange.
