# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Exchange-to-exchange bindings - Exchanges no RabbitMQ |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Intermediário · 06 de 07 |
| 4 | strong | Intermediário · 06 de 07 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Exchange-to-exchange bindings |
| 7 | p | Anterior: Policies, x-arguments e permissões · Próximo: Publisher confirms e confiabilidade |
| 8 | a | Policies, x-arguments e permissões |
| 9 | h1 | Quando uma exchange precisa apontar para outra |
| 10 | p.lead | Uma topologia fica mais expressiva quando a primeira exchange mantém a entrada estável e outras exchanges recebem parte do fluxo para continuar roteando dentro de seus próprios contratos. |
| 11 | p | Imagine `events.public` como a entrada publicada pelos produtores. O domínio de pedidos quer organizar suas filas em `orders.internal`; auditoria quer receber uma cópia controlada em `audit.internal`. Se o publisher precisar conhecer cada fila final, a topologia vaza para quem só deveria publicar no contrato de entrada. |
| 12 | p | O passo novo é deixar que uma exchange seja destino de um binding. Esse é o exchange-to-exchange binding, ou E2E: uma aresta de roteamento em que a mensagem sai de uma exchange e chega a outra exchange, sem passar por um consumidor intermediário. |
| 13 | div.tag-row@aria-label | Ideias centrais deste node |
| 14 | span.tag | entrada estável |
| 15 | span.tag | domínios internos |
| 16 | span.tag | binding key preservada |
| 17 | span.tag | contrato legível |
| 18 | span.tag | sem consumidor intermediário |
| 19 | h2 | A direção é parte do contrato |
| 20 | p | Em E2E, a exchange onde a mensagem entra no trecho é a source exchange. A exchange que recebe esse trecho do fluxo é a destination exchange. A direção importa porque a source escolhe se o binding combina, e a destination ainda aplica suas próprias regras depois. |
| 21 | p | O método que materializa esse vínculo em RabbitMQ é `exchange.bind`. A forma conceitual abaixo não é um roteiro de execução; ela só deixa visível quais nomes carregam a direção da aresta. |
| 22 | pre.code-block.language-yaml@aria-label | Forma conceitual de exchange.bind entre source e destination exchanges |
| 23 | code | # forma conceitual, não comando operacional binding_kind : exchange-to-exchange source_exchange : events.public destination_exchange : orders.internal binding_key : orders.* |
| 24 | span.syntax-comment | # forma conceitual, não comando operacional |
| 25 | span.syntax-key | binding_kind |
| 26 | span.syntax-op | : |
| 27 | span.syntax-value | exchange-to-exchange |
| 28 | span.syntax-key | source_exchange |
| 29 | span.syntax-op | : |
| 30 | span.syntax-value | events.public |
| 31 | span.syntax-key | destination_exchange |
| 32 | span.syntax-op | : |
| 33 | span.syntax-value | orders.internal |
| 34 | span.syntax-key | binding_key |
| 35 | span.syntax-op | : |
| 36 | span.syntax-value | orders.* |
| 37 | p | A binding key não perde significado. Se `events.public` usa roteamento por tópicos, `orders.created` pode combinar com `orders.*` e seguir para `orders.internal`. Dentro de `orders.internal`, o tipo da exchange e seus próprios bindings continuam decidindo quais filas recebem a mensagem. |
| 38 | div.visual-block@aria-label | Mapa conceitual de source exchange ligada a destination exchanges |
| 39 | p | O mapa fica pequeno quando cada camada tem um trabalho claro. |
| 40 | span.tag | source |
| 41 | h3 | events.public |
| 42 | p | Entrada estável para produtores publicarem eventos públicos do sistema. |
| 43 | span.route-label | orders.* |
| 44 | span | binding E2E para pedidos |
| 45 | span.route-label | #.created |
| 46 | span | binding E2E para auditoria |
| 47 | span.tag | destination |
| 48 | h3 | orders.internal |
| 49 | p | Reorganiza eventos de pedidos para filas internas como `orders.worker.q` e `orders.projection.q`. |
| 50 | span.tag | destination |
| 51 | h3 | audit.internal |
| 52 | p | Recebe eventos criados e aplica suas regras para `audit.q`. |
| 53 | p.small | A conclusão do mapa não é "sempre crie mais exchanges". A conclusão é que outra exchange pode ser destino quando essa camada preserva um contrato mais legível. |
| 54 | h2 | A mensagem atravessa a topologia, não uma nova publicação |
| 55 | p | Depois que `orders.internal` vira destino, a mensagem não precisa ser consumida por uma aplicação só para ser publicada de novo. RabbitMQ trata o E2E como extensão do roteamento. A source e as destinations contribuem para o caminho até as filas finais. |
| 56 | p | Essa diferença muda a leitura operacional. Um consumidor intermediário teria seu próprio ciclo de entrega, erro, confirmação e nova publicação. No E2E, a mensagem continua dentro do roteamento do broker. O desenho fica mais curto, mas a topologia precisa continuar fácil de ler. |
| 57 | table@aria-label | Contraste entre E2E e republicação por aplicação intermediária |
| 58 | th | Desenho |
| 59 | th | Quem move a mensagem |
| 60 | th | O que precisa ficar claro |
| 61 | td | Binding entre exchanges |
| 62 | td | O roteamento do RabbitMQ atravessa source e destination exchanges. |
| 63 | td | Direção source -> destination, binding key e tipo de cada exchange. |
| 64 | td | Consumidor que republica |
| 65 | td | Uma aplicação consome de uma fila e publica outra mensagem. |
| 66 | td | Ciclo de consumo, erro, nova publicação e responsabilidade da aplicação. |
| 67 | p | Por isso E2E costuma ser uma boa peça quando o problema é composição de routing, não transformação de payload nem regra de negócio entre uma fila e outra. Quando a mensagem precisa ser alterada, validada ou enriquecida por código, a topologia já está pedindo outra responsabilidade. |
| 68 | h2 | O caminho pode ser transitivo sem duplicar a fila final |
| 69 | p | Ao encadear exchanges, a topologia vira transitiva: uma mensagem pode alcançar uma exchange, que alcança outra, até chegar a filas. RabbitMQ detecta ciclos durante a entrega e garante que, para cada fila alcançada por uma mensagem, a fila receba uma única cópia. |
| 70 | div.visual-block@aria-label | Roteamento transitivo com convergência e ciclo eliminado |
| 71 | p | O detalhe importante é separar proteção do broker de desenho recomendado. |
| 72 | span.tag | convergência |
| 73 | h3 | Duas rotas chegam a `audit.q` |
| 74 | p | `events.public` pode alcançar `audit.internal` diretamente e também passar por `orders.internal`. Se as duas rotas chegarem à mesma fila, a fila recebe uma cópia daquela mensagem. |
| 75 | span.tag | proteção |
| 76 | h3 | Um ciclo não vira entrega infinita |
| 77 | p | Se exchanges forem ligadas de volta para uma exchange anterior, o ciclo é eliminado durante a entrega. Isso protege o broker, mas não torna o ciclo um desenho simples de operar. |
| 78 | p.small | A garantia permite raciocinar sobre grafos transitivos. Ela não substitui uma topologia com fronteiras compreensíveis. |
| 79 | p | Esse ponto é o limite saudável do E2E. Ele ajuda quando a topologia expressa camadas reais de roteamento: entrada pública, domínio interno, auditoria, projeções. Ele atrapalha quando cada exchange nova existe só para esconder uma decisão que deveria estar documentada no contrato da source. |
| 80 | h2 | A exchange destino pode não mostrar entrada |
| 81 | p | Como E2E não republica a mensagem para a destination exchange, a métrica de ingress dessa exchange não é o melhor sinal de que a rota funcionou. A documentação de exchanges registra que essa taxa de entrada da destination exchange não é atualizada nesse caso; as filas e streams finais continuam refletindo entregas quando são alcançados. |
| 82 | div.signal-grid@aria-label | Leitura mínima de sinais em E2E |
| 83 | span.tag | source |
| 84 | h3 | events.public |
| 85 | p | É o ponto em que publishers publicam e onde a topologia começa a ser avaliada. |
| 86 | span.tag | destination |
| 87 | h3 | orders.internal |
| 88 | p | Pode participar do caminho sem mostrar nova taxa de entrada como se recebesse uma publicação direta. |
| 89 | span.tag | filas finais |
| 90 | h3 | orders.worker.q |
| 91 | p | As filas e streams alcançados são os destinos onde a entrega final aparece. |
| 92 | p | A mesma leitura vale para permissões de topologia. Criar o vínculo toca os dois lados: a operação precisa autoridade para configurar a destination exchange e para escrever a partir da source exchange. Isso mantém o E2E dentro do mesmo raciocínio do node anterior: composição também é uma decisão governada. |
| 93 | h2 | A fronteira continua sendo local e explícita |
| 94 | p | Exchanges, filas, bindings, policies e permissões pertencem a um vhost. O E2E compõe recursos nessa fronteira lógica. Quando o problema real é conectar ambientes separados, nodes diferentes ou regiões diferentes, a pergunta já saiu do escopo deste node. |
| 95 | p | Um bom E2E deixa a frase de roteamento mais clara: "`events.public` entrega eventos de pedidos para `orders.internal`, que decide suas filas internas". Um E2E ruim só troca uma lista grande de filas por um grafo difícil de explicar. |
| 96 | p | Dominar este node é conseguir olhar para uma aresta entre exchanges e dizer o que ela preserva: direção source -> destination, regras normais de binding, roteamento transitivo controlado e ausência de nova publicação. O próximo passo separa aceitação da publicação pelo broker de processamento pelos consumidores, sem confundir routing bem-sucedido com trabalho concluído. |
| 97 | h2 | Referências |
| 98 | li.reference-item | RabbitMQ - Exchange to Exchange Bindings Uso neste node: source, destination, `exchange.bind`, ciclos eliminados e cópia única por fila. |
| 99 | a | RabbitMQ - Exchange to Exchange Bindings |
| 100 | span.reference-note | Uso neste node: source, destination, `exchange.bind`, ciclos eliminados e cópia única por fila. |
| 101 | li.reference-item | RabbitMQ - exchanges Uso neste node: bindings para exchanges, E2E como extensão de roteamento e efeito sobre métrica de ingress. |
| 102 | a | RabbitMQ - exchanges |
| 103 | span.reference-note | Uso neste node: bindings para exchanges, E2E como extensão de roteamento e efeito sobre métrica de ingress. |
| 104 | li.reference-item | RabbitMQ - permissões de recursos Uso neste node: permissões exigidas para criar binding entre exchanges. |
| 105 | a | RabbitMQ - permissões de recursos |
| 106 | span.reference-note | Uso neste node: permissões exigidas para criar binding entre exchanges. |
| 107 | li.reference-item | RabbitMQ - virtual hosts Uso neste node: vhost como fronteira lógica de exchanges, filas e bindings. |
| 108 | a | RabbitMQ - virtual hosts |
| 109 | span.reference-note | Uso neste node: vhost como fronteira lógica de exchanges, filas e bindings. |
| 110 | li.reference-item | RabbitMQ - publishers Uso neste node: publicação em exchange e routing topology em AMQP 0-9-1. |
| 111 | a | RabbitMQ - publishers |
| 112 | span.reference-note | Uso neste node: publicação em exchange e routing topology em AMQP 0-9-1. |
