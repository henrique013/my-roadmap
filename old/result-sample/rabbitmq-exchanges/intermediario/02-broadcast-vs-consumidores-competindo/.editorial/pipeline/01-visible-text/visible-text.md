# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | Broadcast vs consumidores competindo |
| 2 | a.backlink | Voltar ao roadmap |
| 3 | p | Intermediário · 02 de 07 |
| 4 | strong | Intermediário · 02 de 07 |
| 5 | p | Roadmap: Exchanges no RabbitMQ |
| 6 | p | Node atual: Broadcast vs consumidores competindo |
| 7 | p | Anterior: Contrato de topologia e roteamento · Próximo: Unroutable, mandatory e Alternate Exchange |
| 8 | a | Contrato de topologia e roteamento |
| 9 | h1 | Quando três interessados não são três workers |
| 10 | p.lead | Quando cada serviço precisa processar o mesmo evento, o desenho multiplica filas. Quando instâncias equivalentes dividem o mesmo trabalho, o desenho compartilha uma fila. Essa diferença separa broadcast de consumidores competindo. |
| 11 | h2 | O evento precisa existir em mais de um lugar |
| 12 | p | Imagine uma publicação `pedido.criado`. O serviço de e-mail usa o evento para avisar o cliente, auditoria usa o mesmo evento para registrar trilha, e analytics usa o mesmo evento para alimentar métricas. Se apenas um deles receber a mensagem, o sistema perde uma consequência esperada. |
| 13 | p | A unidade de independência, aqui, não é o processo que está online agora. É o papel de consumo. Cada papel precisa ter seu próprio ponto de acúmulo, sua própria velocidade e sua própria falha isolada. No RabbitMQ, esse ponto é uma fila. |
| 14 | div.visual-block@aria-label | Contraste entre cópia por fila e divisão de trabalho em uma fila |
| 15 | span.tag | Papéis diferentes |
| 16 | h3 | Uma publicação, três filas |
| 17 | p | O evento passa pela exchange e entra em filas separadas. Cada fila guarda uma cópia para o serviço que tem um motivo próprio para processar. |
| 18 | span.tag.blue | Papel igual |
| 19 | h3 | Uma fila, três workers |
| 20 | p | As instâncias fazem o mesmo trabalho lógico. A fila mantém a sequência de tarefas e cada entrega vai para um dos workers disponíveis. |
| 21 | div.worker-strip@aria-label | Workers equivalentes consumindo da mesma fila |
| 22 | p | No primeiro desenho, a exchange multiplica destinos: cada fila representa um interessado independente. No segundo, a fila concentra o trabalho e distribui entregas para instâncias equivalentes. A diferença parece pequena no diagrama, mas muda o contrato de processamento. |
| 23 | h2 | A cópia nasce na fila, não no processo |
| 24 | p | Quando a publicação precisa chegar a vários papéis, o efeito importante é a cópia por fila. Uma mesma mensagem roteada para três filas cria três trilhas de consumo: e-mail pode estar atrasado sem impedir auditoria; analytics pode cair sem apagar o backlog de e-mail; cada serviço confirma o próprio processamento. |
| 25 | p | Depois que essa relação está clara, o nome técnico ajuda: esse desenho é broadcast. Em RabbitMQ, fanout é a forma mais direta de produzir esse efeito, porque ignora a routing key e envia uma cópia a cada destino ligado. Mas broadcast arquitetural não depende apenas de fanout. Direct e topic também podem atingir mais de uma fila quando mais de um binding combina com a publicação. |
| 26 | h2 | Workers equivalentes disputam a mesma sequência |
| 27 | p | Agora troque o cenário. Um serviço precisa gerar relatórios, e três instâncias idênticas estão online para dividir a carga. Se cada instância tiver sua própria fila ligada à exchange, a mesma tarefa pode aparecer três vezes. Isso não é escala horizontal; é trabalho duplicado. |
| 28 | p | Para dividir trabalho, as instâncias compartilham uma fila. Cada mensagem fica disponível para o grupo, e uma entrega concreta vai para um consumer. O nome comum para esse padrão é consumidores competindo: não porque os processos saibam uns dos outros, mas porque a fila entrega unidades de trabalho a consumers equivalentes. |
| 29 | th | Intenção técnica |
| 30 | th | Desenho de filas |
| 31 | th | Consequência observável |
| 32 | td | Todos os serviços precisam processar o evento. |
| 33 | td | Uma fila por papel interessado. |
| 34 | td | Cada fila recebe sua cópia e avança no próprio ritmo. |
| 35 | td | Uma tarefa deve ser feita por uma instância equivalente. |
| 36 | td | Uma fila compartilhada pelo grupo de consumidores. |
| 37 | td | Cada entrega vai para um worker do grupo, não para todos. |
| 38 | h2 | Fanout resolve cópia, não escala workers |
| 39 | p | Uma confusão frequente aparece quando alguém liga uma fanout exchange a uma única fila e coloca três consumers nessa fila esperando que todos recebam a mesma mensagem. O fanout já cumpriu seu papel quando roteou para a fila ligada. A partir daí, quem decide a entrega é a fila, e a fila está compartilhada por consumers equivalentes. |
| 40 | p | O inverso também acontece. Se a intenção é dividir trabalho, criar uma fila por worker faz a exchange entregar cópias independentes, porque cada fila vira destino próprio. A topologia passa a multiplicar tarefas quando o que se queria era repartir tarefas. |
| 41 | h2 | A janela de entregas muda a aparência da disputa |
| 42 | p | Dentro de uma fila compartilhada, a distribuição não deve ser lida como promessa de alternância perfeita. Um consumer pode receber mensagens e ainda não ter confirmado o processamento. Enquanto essas entregas estão em andamento, existe uma janela local aberta naquele consumer. |
| 43 | p | O nome dessa janela é prefetch. No RabbitMQ, o valor aplicado ao consumer limita quantas entregas não confirmadas ele pode manter antes de receber novas mensagens. Isso não cria cópia, não troca a topologia e não decide se o desenho é broadcast. Ele só muda quanto trabalho pode ficar adiantado em cada consumer. |
| 44 | div.window-grid@aria-label | Janela conceitual de prefetch em consumidores da mesma fila |
| 45 | span.tag | worker A |
| 46 | h3 | Janela cheia |
| 47 | p.small | Enquanto nada é confirmado, a fila não precisa enviar mais para este worker. |
| 48 | span.tag.blue | worker B |
| 49 | h3 | Há espaço |
| 50 | p.small | A próxima entrega pode seguir para quem ainda tem janela livre. |
| 51 | span.tag.warn | fila |
| 52 | h3 | Sinal de capacidade |
| 53 | p.small | Consumer capacity ajuda a observar se a fila consegue entregar imediatamente. |
| 54 | p | Essa é a leitura suficiente para este ponto do roadmap: prefetch afeta a distribuição observada dentro do grupo de consumidores. Valores, throughput, latência e escolhas finas pertencem a outra discussão. |
| 55 | h2 | A decisão cabe em uma pergunta de papel |
| 56 | p | Quando a topologia estiver confusa, ignore por um momento o nome da exchange e pergunte o que cada processo representa. Se ele representa um papel independente, ele precisa de sua própria fila. Se ele representa mais uma instância do mesmo papel, ele compete na fila compartilhada. |
| 57 | span.tag | Todos precisam ver |
| 58 | h3 | Use múltiplas filas |
| 59 | p | E-mail, auditoria e analytics são consequências diferentes do mesmo evento. Cada serviço recebe uma cópia por fila e confirma no próprio ritmo. |
| 60 | span.tag.blue | Um equivalente precisa fazer |
| 61 | h3 | Use uma fila compartilhada |
| 62 | p | Três workers de relatório executam o mesmo papel. Eles disputam entregas da mesma fila para aumentar capacidade sem duplicar trabalho. |
| 63 | p | O desenho fica estável quando a fila representa a unidade certa de independência. Papéis diferentes recebem cópias em filas separadas; instâncias equivalentes dividem entregas na mesma fila. A próxima pergunta aparece quando a publicação não encontra destino compatível. |
| 64 | h2 | Referências |
| 65 | li.reference-item | Documentação oficial de exchanges Uso neste node: sustenta fanout, direct, topic e o roteamento para destinos ligados. |
| 66 | a | Documentação oficial de exchanges |
| 67 | span.reference-note | Uso neste node: sustenta fanout, direct, topic e o roteamento para destinos ligados. |
| 68 | li.reference-item | Tutorial oficial de filas de trabalho Uso neste node: sustenta workers equivalentes compartilhando uma fila e a leitura conceitual de prefetch. |
| 69 | a | Tutorial oficial de filas de trabalho |
| 70 | span.reference-note | Uso neste node: sustenta workers equivalentes compartilhando uma fila e a leitura conceitual de prefetch. |
| 71 | li.reference-item | Tutorial oficial de publicação para vários interessados Uso neste node: sustenta uma fila por receptor interessado e binding como ligação com a exchange. |
| 72 | a | Tutorial oficial de publicação para vários interessados |
| 73 | span.reference-note | Uso neste node: sustenta uma fila por receptor interessado e binding como ligação com a exchange. |
| 74 | li.reference-item | Documentação oficial de filas Uso neste node: sustenta fila como ponto de acúmulo e entrega para consumidores. |
| 75 | a | Documentação oficial de filas |
| 76 | span.reference-note | Uso neste node: sustenta fila como ponto de acúmulo e entrega para consumidores. |
| 77 | li.reference-item | Documentação oficial de consumidores e capacidade Uso neste node: sustenta consumo a partir de filas e consumer capacity como sinal operacional. |
| 78 | a | Documentação oficial de consumidores e capacidade |
| 79 | span.reference-note | Uso neste node: sustenta consumo a partir de filas e consumer capacity como sinal operacional. |
| 80 | li.reference-item | Documentação oficial de prefetch Uso neste node: sustenta o limite de entregas não confirmadas aplicado a consumers no RabbitMQ. |
| 81 | a | Documentação oficial de prefetch |
| 82 | span.reference-note | Uso neste node: sustenta o limite de entregas não confirmadas aplicado a consumers no RabbitMQ. |
| 83 | li.reference-item | Guia oficial de acknowledgements e prefetch Uso neste node: sustenta a janela de entregas em andamento e sua relação com acknowledgements. |
| 84 | a | Guia oficial de acknowledgements e prefetch |
| 85 | span.reference-note | Uso neste node: sustenta a janela de entregas em andamento e sua relação com acknowledgements. |
