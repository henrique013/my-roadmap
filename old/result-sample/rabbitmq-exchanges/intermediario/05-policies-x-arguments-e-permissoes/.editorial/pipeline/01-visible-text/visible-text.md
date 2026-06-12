# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Quem governa a configuração da topologia |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Intermediário · 05 de 07 |
| 4 | strong | Intermediário · 05 de 07 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Policies, x-arguments e permissões |
| 7 | p | Anterior: Dead Letter Exchanges e retry conceitual · Próximo: Exchange-to-exchange bindings |
| 8 | a | Dead Letter Exchanges e retry conceitual |
| 9 | h1 | Quem governa a configuração da topologia |
| 10 | p.lead | Depois que DLX, AE e TTL já são peças conhecidas, a dúvida muda de lugar: não é mais o que essas configurações fazem, mas quem pode defini-las, alterá-las e limitá-las dentro de um domínio RabbitMQ. |
| 11 | p | Imagine que várias filas do domínio de pedidos usam a mesma exchange de dead-letter. Se cada aplicação declara sua fila com o destino escrito no próprio código, uma troca de rota operacional vira uma rodada de mudanças de aplicação. A configuração está tecnicamente correta, mas está presa ao ciclo de vida errado. |
| 12 | p | O modelo útil começa separando três coisas que costumam aparecer misturadas: a declaração que cria o recurso, a regra operacional que ajusta um grupo de recursos e a autorização que diz quem pode tocar cada peça. |
| 13 | div.tag-row@aria-label | Camadas que serão separadas neste node |
| 14 | span.tag | declaração da aplicação |
| 15 | span.tag | regra operacional |
| 16 | span.tag | guardrail do operador |
| 17 | span.tag | permissão por recurso |
| 18 | span.tag | fronteira lógica |
| 19 | h2 | Quando a configuração fica presa ao cliente |
| 20 | p | Uma fila pode nascer com argumentos opcionais enviados pelo cliente no momento da declaração. No vocabulário da documentação, esses argumentos são `x-arguments`. Eles são úteis quando o valor pertence ao próprio nascimento do recurso, mas ficam rígidos quando representam uma decisão operacional que pode mudar depois. |
| 21 | p | O problema aparece com clareza em um grupo de filas `orders.*`. A aplicação sabe declarar sua fila, mas talvez não deva carregar no código a escolha atual da DLX, do TTL ou de outro parâmetro que a plataforma ajusta com o tempo. |
| 22 | pre.code-block.language-yaml@aria-label | Recorte conceitual de configuração hardcoded em declaração de fila |
| 23 | code | # Forma conceitual, não roteiro de execução queue : orders.created declared_by : orders-api x-arguments : dead-letter-exchange : orders.dlx.v1 message-ttl : 60000 |
| 24 | span.syntax-comment | # Forma conceitual, não roteiro de execução |
| 25 | span.syntax-key | queue |
| 26 | span.syntax-op | : |
| 27 | span.syntax-value | orders.created |
| 28 | span.syntax-key | declared_by |
| 29 | span.syntax-op | : |
| 30 | span.syntax-value | orders-api |
| 31 | span.syntax-key | x-arguments |
| 32 | span.syntax-op | : |
| 33 | span.syntax-key | dead-letter-exchange |
| 34 | span.syntax-op | : |
| 35 | span.syntax-value | orders.dlx.v1 |
| 36 | span.syntax-key | message-ttl |
| 37 | span.syntax-op | : |
| 38 | span.syntax-value | 60000 |
| 39 | p | A leitura importante não é a sintaxe. A leitura é a autoridade: nesse desenho, o cliente que declara a fila também escolhe valores que talvez precisem mudar em produção. Quando a mesma escolha precisa valer para muitas filas, esse acoplamento vira custo. |
| 40 | div.visual-block@aria-label | Contraste entre argumento hardcoded e policy por grupo |
| 41 | p | O contraste fica mais claro quando a mesma decisão sai da declaração individual e passa a ser aplicada por grupo. |
| 42 | span.step-label | Antes |
| 43 | strong | Cada fila carrega seu valor |
| 44 | p | `orders.created`, `orders.billing` e `orders.audit` podem nascer com o mesmo argumento repetido em declarações diferentes. |
| 45 | span.step-label | Mudança |
| 46 | strong | A regra casa nomes |
| 47 | p | Uma policy usa um padrão como `orders.*` e aplica uma definição comum às filas que combinam com esse padrão. |
| 48 | span.step-label | Depois |
| 49 | strong | O valor muda no broker |
| 50 | p | A atualização da regra é operacional. As aplicações continuam declarando recursos com nomes previsíveis. |
| 51 | p.note | A policy não elimina a declaração da aplicação. Ela tira da aplicação o que pertence a uma regra operacional compartilhada. |
| 52 | h2 | A policy muda o lugar da decisão |
| 53 | p | Uma policy é uma regra declarativa, escopada por vhost, que casa nomes de filas, exchanges ou streams e injeta uma definição de argumentos opcionais nos recursos correspondentes. Ela é um exemplo de runtime parameter: um valor mantido pelo broker para coisas que podem precisar mudar em operação. |
| 54 | p | Essa flexibilidade tem limites. A policy serve para parâmetros que o RabbitMQ permite ajustar dessa forma. Ela não transforma uma propriedade fixa de declaração em algo mutável. O tipo de fila, por exemplo, nasce com o recurso; não é o tipo de decisão que uma policy deve tentar trocar depois. |
| 55 | h3 | Aplicação |
| 56 | p | Declara recursos com nomes e contratos previsíveis. Ela deve conhecer o que precisa para existir, não todo ajuste operacional possível. |
| 57 | h3 | Policy |
| 58 | p | Aplica parâmetros compatíveis a um grupo de recursos. O foco é mudar comportamento comum sem redesenhar cada aplicação. |
| 59 | h3 | Limite |
| 60 | p | Nem toda chave cabe em policy. Quando o valor é parte estrutural da criação do recurso, a policy não deve ser vendida como saída mágica. |
| 61 | p | Esse ponto é decisivo para não trocar uma rigidez por outra. Uma boa policy deixa explícito o padrão de nomes, o tipo de recurso atingido e o motivo da definição. Uma policy ampla demais pode afetar recursos que só parecem pertencer ao mesmo grupo. |
| 62 | h2 | Quando três camadas disputam a mesma chave |
| 63 | p | Depois que existe declaração da aplicação e policy operacional, surge outra pergunta: se os dois lados definem a mesma chave, qual valor vale? Essa é a regra de precedência. Em RabbitMQ, quando uma chave vem tanto de `x-arguments` do cliente quanto de policy comum, o argumento fornecido pelo cliente prevalece. |
| 64 | p | Isso explica por que valores hardcoded são mais do que uma preferência de estilo. Se a aplicação fixa uma chave que a plataforma queria controlar por policy, a policy pode não produzir o valor esperado para aquele recurso. |
| 65 | div.visual-block@aria-label | Camadas de autoridade para valor efetivo |
| 66 | p | Uma operator policy adiciona uma camada de guardrail: ela protege limites definidos pelo operador e pode restringir valores escolhidos pela aplicação ou pela policy comum. |
| 67 | h3 | 1. Declaração do cliente |
| 68 | p | Fornece `x-arguments`. Para uma mesma chave, pode vencer a policy comum. |
| 69 | h3 | 2. Policy comum |
| 70 | p | Aplica definição por grupo de recursos dentro do vhost, desde que a chave seja compatível. |
| 71 | h3 | 3. Operator policy |
| 72 | p | Age como guardrail. Para valores numéricos de limite, a documentação orienta o valor efetivo para o teto mais restritivo. |
| 73 | p.note | A conclusão prática: não basta ter policy. É preciso saber se a aplicação já colocou a mesma chave na declaração e se existe guardrail acima das duas camadas. |
| 74 | p | A operator policy não é apenas uma policy com nome mais forte. Ela representa uma autoridade diferente: o operador do ambiente pode impor limites para proteger uso de recursos e consistência operacional. A aplicação ainda pode escolher valores dentro desse limite, mas não deve conseguir ultrapassá-lo. |
| 75 | h2 | A configuração também cruza permissões |
| 76 | p | Governar topologia não é só decidir onde o valor fica. É decidir quem pode executar cada ação. Dentro de um vhost, RabbitMQ distingue três permissões de recurso: `configure`, `write` e `read`. Em linguagem simples, configure altera ou cria recurso, write injeta mensagens em recurso e read recupera mensagens de recurso. |
| 77 | p | Essa separação impede que um publisher precise controlar topologia inteira só para publicar. O publisher que envia eventos para uma exchange do domínio precisa de `write` naquela exchange. Ele não precisa, por esse motivo, de permissão para declarar filas consumidoras. |
| 78 | table@aria-label | Permissões conceituais por papel |
| 79 | th | Papel no desenho |
| 80 | th | Ação relevante |
| 81 | th | Recurso tocado |
| 82 | th | Permissão que sustenta a ação |
| 83 | td | Aplicação que declara topologia própria |
| 84 | td | Cria ou altera fila |
| 85 | td | Fila declarada |
| 86 | td | `configure` na fila |
| 87 | td | Publisher do domínio |
| 88 | td | Publica mensagem |
| 89 | td | Exchange de entrada |
| 90 | td | `write` na exchange |
| 91 | td | Consumer |
| 92 | td | Consome mensagem |
| 93 | td | Fila do serviço |
| 94 | td | `read` na fila |
| 95 | td | Fila com DLX configurada |
| 96 | td | Declara referência para a DLX |
| 97 | td | Fila e exchange de DLX |
| 98 | td | `configure` e `read` na fila, `write` na DLX |
| 99 | p | O último caso é a ponte com o node anterior. A DLX continua sendo uma exchange normal, mas configurar uma fila para dead-lettering aponta para outro recurso. Por isso a declaração da fila precisa ser autorizada também em relação à exchange de destino. |
| 100 | p | Uma permissão ampla demais pode mascarar um desenho ruim. Se tudo tem `write` em tudo, a publicação passa, mas o domínio perde fronteira. O objetivo não é bloquear o sistema; é fazer cada papel ter autoridade suficiente para a ação que realmente executa. |
| 101 | h2 | O vhost é a fronteira onde esses nomes valem |
| 102 | p | Até aqui, a explicação falou em filas, exchanges, policies e permissões como se houvesse um único espaço de nomes. No RabbitMQ, esses recursos pertencem a um virtual host, ou vhost. Ele é uma fronteira lógica: a mesma exchange name em dois vhosts representa recursos diferentes, com policies e permissões diferentes. |
| 103 | div.visual-block@aria-label | Vhost como fronteira lógica para recursos e permissões |
| 104 | p | O vhost ajuda a manter domínios separados sem fingir que isso é isolamento físico completo. |
| 105 | span.box-title | vhost `prod.orders` |
| 106 | p | Exchange `events`, filas `orders.*`, policy de DLX do domínio e permissões dos serviços de pedidos. |
| 107 | span.box-title | vhost `prod.payments` |
| 108 | p | Outra exchange `events`, outras filas, outra policy e outro conjunto de permissões. |
| 109 | p.note | O nome pode repetir; a autoridade não atravessa automaticamente a fronteira do vhost. |
| 110 | p | Essa fronteira fecha a pergunta inicial. Uma policy de `orders.*` só faz sentido dentro do vhost em que esses recursos vivem. Uma permissão de `write` também deve ser lida dentro desse vhost. Sem essa referência, "pode publicar em events" é uma frase incompleta. |
| 111 | h2 | O desenho fica legível quando cada camada tem dono |
| 112 | p | A matriz abaixo junta a linha de raciocínio. Ela não é uma lista de cargos; é uma forma de testar se a topologia tem autoridade clara. |
| 113 | table@aria-label | Matriz de ownership para configuração e permissões |
| 114 | th | Camada |
| 115 | th | Responsabilidade |
| 116 | th | Exemplo no domínio `orders` |
| 117 | th | Limite saudável |
| 118 | td | Aplicação |
| 119 | td | Declarar recurso que pertence ao serviço |
| 120 | td | Fila `orders.created` com nome estável |
| 121 | td | Não carregar ajuste operacional compartilhado sem necessidade |
| 122 | td | Plataforma |
| 123 | td | Aplicar policy por grupo |
| 124 | td | DLX comum para `orders.*` |
| 125 | td | Não afetar recursos fora do pattern pretendido |
| 126 | td | Operador |
| 127 | td | Impor guardrail |
| 128 | td | Teto para valores de uso de recurso |
| 129 | td | Não substituir o contrato de domínio por limite genérico |
| 130 | td | Publisher |
| 131 | td | Enviar eventos |
| 132 | td | `write` na exchange de entrada |
| 133 | td | Não receber `configure` só para conseguir publicar |
| 134 | td | Consumer |
| 135 | td | Ler sua fila |
| 136 | td | `read` na fila do serviço |
| 137 | td | Não ganhar acesso de leitura a filas de outro domínio |
| 138 | p | Quando essa divisão está clara, mudar a DLX de um conjunto de filas deixa de ser uma caça por valores repetidos em código. A plataforma altera a regra certa, o operador mantém limites, e as aplicações continuam usando contratos previsíveis. |
| 139 | p | O critério para dominar este node é simples de testar: dado um comportamento de topologia, você consegue dizer se ele deveria nascer na declaração da aplicação, numa policy, num guardrail de operador ou numa permissão de recurso dentro de um vhost. O próximo node usa essa governança local como base para compor exchanges entre si sem transformar a topologia em um grafo opaco. |
| 140 | h2 | Referências |
| 141 | li.reference-item | RabbitMQ - policies Uso neste node: base para policy comum, operator policy, prioridade, apply-to e limites de uso em runtime. |
| 142 | a | RabbitMQ - policies |
| 143 | span.reference-note | Uso neste node: base para policy comum, operator policy, prioridade, apply-to e limites de uso em runtime. |
| 144 | li.reference-item | RabbitMQ - permissões de recursos Uso neste node: separação de configure, write e read e permissões AMQP 0-9-1 para declarar, publicar, bindar e consumir. |
| 145 | a | RabbitMQ - permissões de recursos |
| 146 | span.reference-note | Uso neste node: separação de configure, write e read e permissões AMQP 0-9-1 para declarar, publicar, bindar e consumir. |
| 147 | li.reference-item | RabbitMQ - exchanges e precedência de argumentos Uso neste node: regra de precedência entre argumentos do cliente, policy comum e operator policy. |
| 148 | a | RabbitMQ - exchanges e precedência de argumentos |
| 149 | span.reference-note | Uso neste node: regra de precedência entre argumentos do cliente, policy comum e operator policy. |
| 150 | li.reference-item | RabbitMQ - configuração de DLX Uso neste node: exemplo de DLX configurada por policy e permissões verificadas ao declarar a fila. |
| 151 | a | RabbitMQ - configuração de DLX |
| 152 | span.reference-note | Uso neste node: exemplo de DLX configurada por policy e permissões verificadas ao declarar a fila. |
| 153 | li.reference-item | RabbitMQ - runtime parameters Uso neste node: contexto para entender policy como configuração mantida pelo broker e alterável em operação. |
| 154 | a | RabbitMQ - runtime parameters |
| 155 | span.reference-note | Uso neste node: contexto para entender policy como configuração mantida pelo broker e alterável em operação. |
| 156 | li.reference-item | RabbitMQ - virtual hosts Uso neste node: vhost como fronteira lógica de recursos, permissões e policies. |
| 157 | a | RabbitMQ - virtual hosts |
| 158 | span.reference-note | Uso neste node: vhost como fronteira lógica de recursos, permissões e policies. |
