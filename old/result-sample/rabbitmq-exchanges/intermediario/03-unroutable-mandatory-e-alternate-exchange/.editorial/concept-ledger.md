# Concept ledger

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Level: intermediario
- Node: Unroutable, mandatory e Alternate Exchange
- Node ID: intermediario/03-unroutable-mandatory-e-alternate-exchange
- Data: 2026-06-10
- Fonte principal: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/research-dump.md`

## Conceitos Permitidos no HTML

### Mensagem sem rota

- Tipo: estado
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum depois de mostrar a exchange tentando rotear
- Primeira ocorrência permitida: abertura narrativa, depois de relembrar publicação em exchange e binding compatível ausente
- Explicação mínima exigida antes da primeira ocorrência: uma publicação chegou à exchange, mas nenhuma ligação de routing aponta para destino compatível
- Aliases e paráfrases:
  - sem rota
  - mensagem sem rota
  - publicação sem rota
  - unroutable
  - routing miss
  - não encontrou binding compatível
- Termos relacionados que também exigem preparo:
  - descarte
  - retorno
  - fallback
- Pode aparecer em:
  - título: sim
  - lead: sim, se a abertura já preparar a situação
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - nomear o estado da publicação no momento de roteamento
  - comparar os caminhos de descarte, retorno e fallback
- Usos proibidos:
  - usar como sinônimo de consumer lento, fila cheia ou falha de processamento
- Fronteira com nodes futuros: diagnóstico operacional detalhado fica para o nível avançado
- Fonte base: F1, F3, F4 do dump

### `mandatory`

- Tipo: parâmetro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de explicar que o publisher precisa receber sinal quando a exchange não acha destino
- Explicação mínima exigida antes da primeira ocorrência: é uma opção da publicação que pede retorno ao broker quando não há rota
- Aliases e paráfrases:
  - mandatory
  - `mandatory`
  - mandatory flag
  - flag mandatory
  - pedido de retorno da publicação
- Termos relacionados que também exigem preparo:
  - `basic.return`
  - handler de retorno
- Pode aparecer em:
  - título: sim, depois da abertura
  - lead: sim, como parte do label canônico do node
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - diferenciar sinal ao publisher de fallback topológico
  - explicar retorno de mensagem sem rota
- Usos proibidos:
  - apresentar como garantia de entrega ao consumidor
  - apresentar como confirmação de persistência ou de processamento
- Fronteira com nodes futuros: publisher confirms em profundidade ficam para node posterior
- Fonte base: F1 e F4 do dump

### Retorno ao publisher

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum depois de preparar `mandatory`
- Primeira ocorrência permitida: seção que mostra o publisher pedindo sinal da falha de roteamento
- Explicação mínima exigida antes da primeira ocorrência: o broker devolve a publicação ao lado publicador quando a mensagem sem rota foi publicada com `mandatory=true`
- Aliases e paráfrases:
  - retorno ao publisher
  - mensagem retornada
  - returned message
  - `basic.return`
  - Return method
  - handler de retorno
- Termos relacionados que também exigem preparo:
  - reply code
  - reply text
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar o sinal da falha ao publisher
  - mostrar que sem handler a aplicação pode ignorar o sinal
- Usos proibidos:
  - confundir com consumer acknowledgement
  - confundir com publisher confirm
- Fronteira com nodes futuros: confirms ficam apenas como fronteira curta
- Fonte base: F1 e F4 do dump

### Alternate Exchange

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de mostrar que uma rota alternativa pode capturar o que a rota principal não aceitou
- Explicação mínima exigida antes da primeira ocorrência: é uma exchange configurada como destino alternativo para mensagens que a exchange principal não conseguiu rotear
- Aliases e paráfrases:
  - Alternate Exchange
  - alternate exchange
  - AE
  - exchange alternativa
  - rota alternativa configurada na exchange
- Termos relacionados que também exigem preparo:
  - `alternate-exchange`
  - roteamento de fallback
- Pode aparecer em:
  - título: sim
  - lead: sim, como parte do label canônico do node
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar fallback topológico para mensagens sem rota
  - comparar AE com `mandatory`
- Usos proibidos:
  - tratar como solução para rejeição de consumer
  - tratar como confirmação de processamento
- Fronteira com nodes futuros: policies e x-arguments são apenas mencionados como forma de configuração, sem aprofundamento
- Fonte base: F2 do dump

### Roteamento de fallback

- Tipo: mecanismo
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: sim, como linguagem comum
- Primeira ocorrência permitida: depois de mostrar a rota principal falhando
- Explicação mínima exigida antes da primeira ocorrência: uma rota secundária recebe o que a rota normal não aceitou
- Aliases e paráfrases:
  - fallback
  - roteamento de fallback
  - rota alternativa
  - coleta de órfãs
  - fila de órfãs
- Termos relacionados que também exigem preparo:
  - Alternate Exchange
  - mensagem sem rota
- Pode aparecer em:
  - título: sim
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: sim
  - referências: sim
  - comentário final: sim
- Usos permitidos:
  - explicar migração de routing keys e coleta controlada de publicações sem rota
- Usos proibidos:
  - esconder erro de contrato como sucesso
- Fronteira com nodes futuros: diagnóstico completo fica no avançado
- Fonte base: F1 e F2 do dump

### Handler de retorno

- Tipo: papel
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não
- Primeira ocorrência permitida: depois de `mandatory` e retorno ao publisher estarem preparados
- Explicação mínima exigida antes da primeira ocorrência: a aplicação publicadora precisa ouvir e tratar a mensagem retornada
- Aliases e paráfrases:
  - handler de retorno
  - callback de retorno
  - listener de retorno
  - lógica que trata o retorno
- Termos relacionados que também exigem preparo:
  - `basic.return`
- Pode aparecer em:
  - título: não
  - lead: não
  - corpo: sim
  - tabela: sim
  - visual/aria-label: não
  - referências: não
  - comentário final: sim
- Usos permitidos:
  - mostrar que `mandatory` só vira sinal útil se a aplicação tratar o retorno
- Usos proibidos:
  - virar exemplo de API de biblioteca
- Fronteira com nodes futuros: não entrar em bibliotecas específicas
- Fonte base: F1 do dump

## Conceitos Permitidos Só no Dump

### `immediate`

- Motivo: aparece na referência AMQP perto de `mandatory`, mas não faz parte do recorte deste node.
- Por que não deve aparecer no HTML: abriria uma flag protocolar não usada no contrato do roadmap.
- Aliases bloqueados no HTML:
  - immediate
  - flag immediate
- Fonte base: F4 do dump

### Protocolos não AMQP 0-9-1

- Motivo: a página de publishers compara AMQP 1.0, MQTT e STOMP.
- Por que não deve aparecer no HTML: o node usa recorte AMQP 0-9-1 em RabbitMQ e não deve comparar protocolos.
- Aliases bloqueados no HTML:
  - MQTT
  - STOMP
  - AMQP 1.0
- Fonte base: F1 do dump

### Comandos de administração

- Motivo: fontes oficiais trazem `rabbitmqctl` e `rabbitmqadmin` para configuração.
- Por que não deve aparecer no HTML: a página não deve virar laboratório nem roteiro operacional.
- Aliases bloqueados no HTML:
  - rabbitmqctl
  - rabbitmqadmin
  - HTTP API
- Fonte base: F2 do dump

## Conceitos Reservados a Nodes Futuros

### Mecanismo reservado ao node seguinte

- Node responsável: Dead Letter Exchanges e retry conceitual
- Node ID responsável, quando existir: `intermediario/04-dead-letter-exchanges-e-retry-conceitual`
- Menção permitida no HTML atual: curta como fronteira, sem explicar mecanismo
- Aliases bloqueados:
  - redelivery-limit
  - delivery-limit
  - retry loop
- Condição de exceção: o label real do próximo node pode aparecer no contexto de posição porque é obrigatório pelo contrato da skill.

### Governança de configuração

- Node responsável: Policies, x-arguments e permissões
- Node ID responsável, quando existir: `intermediario/05-policies-x-arguments-e-permissoes`
- Menção permitida no HTML atual: curta como fronteira ou observação de que detalhes ficam depois
- Aliases bloqueados:
  - x-arguments
  - argumentos opcionais em profundidade
  - permissões em profundidade
- Condição de exceção: o campo conceitual `alternate-exchange` pode aparecer como forma mínima da AE, sem comandos nem policy detalhada.

### Publisher confirms em profundidade

- Node responsável: Publisher confirms e confiabilidade
- Node ID responsável, quando existir: `intermediario/07-publisher-confirms-e-confiabilidade`
- Menção permitida no HTML atual: curta como fronteira para dizer que retorno de rota não é confirmação de processamento
- Aliases bloqueados:
  - confirm listener
  - waitForConfirms
  - sequence number de confirm
- Condição de exceção: a expressão "publisher confirms" pode aparecer em nota de fronteira se não for ensinada.

### Diagnóstico operacional avançado

- Node responsável: Diagnóstico de roteamento e observabilidade
- Node ID responsável, quando existir: `avancado/01-diagnostico-de-roteamento-e-observabilidade`
- Menção permitida no HTML atual: curta como consequência de monitorar publicações sem rota
- Aliases bloqueados:
  - management UI
  - rabbitmq-diagnostics
  - troubleshooting completo
- Condição de exceção: "métrica" pode aparecer como palavra comum quando a frase fala apenas de sinal de perda.

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
| F1 | Publishers, Unroutable Message Handling | sim | Documentação de publishers |
| F2 | Alternate Exchanges | sim, depois de preparar AE | Documentação de Alternate Exchanges |
| F3 | Exchanges | sim | Documentação de exchanges |
| F4 | AMQP 0-9-1 Complete Reference Guide | sim | Referência AMQP 0-9-1 |
| F5 | Consumer Acknowledgements and Publisher Confirms | sim, só no rodapé e com nota de fronteira | Documentação sobre acknowledgements e confirmações |
| F6 | Dead Letter Exchanges | não | deixar apenas no dump |
