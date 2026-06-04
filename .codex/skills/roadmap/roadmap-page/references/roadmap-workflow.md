# Workflow do Modo `roadmap-page`

Use este modo para transformar uma entrada bruta em um roadmap HTML final e em
um contrato estruturado para o modo `node-pages`.

Principio Pareto: mantenha poucas regras, mas rigorosas. O resultado bom vem de
entrada clara, pesquisa real, curadoria semantica, nodes bem delimitados,
anti-repeticao, referencias especificas e validacao final objetiva.

## 1. Entrada, Saida e Ativacao

Use esta skill quando a pessoa pedir um roadmap, trilha de aprendizado, mapa de
estudo, mapa conceitual sequencial ou HTML de roadmap.

Entrada minima:

- `tema`: o que a pessoa quer aprender.

Contexto opcional:

- conhecimentos previos, experiencia, senioridade, objetivo ou contexto
  relevante do leitor, quando a pessoa fornecer.

Se faltar `tema`, pergunte somente pelo tema e nao crie arquivos. Nao pergunte
por contexto previo como requisito para gerar o roadmap.

Saida obrigatoria:

- `.tmp/roadmaps/<slug>/roadmap.html`.

Esse arquivo deve ser um unico roadmap HTML com tres niveis coordenados:

- `basico`: fundamentos, vocabulario indispensavel e modelos mentais;
- `intermediario`: arquitetura, relacoes, decisoes e trade-offs;
- `avancado`: limites, casos de borda, falhas, comportamento avancado e
  criterios de especialista.

Cada nivel pode ter no maximo 20 nodes. O limite e teto, nao meta; nao preencha
nodes para chegar a 20 quando o tema pedir menos.

Saida interna obrigatoria:

- `.tmp/roadmaps/<slug>/.roadmap/roadmap-contract.json`.

Nao gere `prompt.md`.

Nao cole o HTML no chat.

Nao escreva a documentacao completa dos nodes.

Nao gere exercicios, laboratorios, hands-on, desafios praticos, estudos de caso
praticos ou projeto final. Se o pedido trouxer pratica, converta para base
teorica necessaria para praticar fora do roadmap.

Resposta final no chat:

```text
.tmp/roadmaps/<slug>/roadmap.html
Pesquisa usada; referencias estao dentro do HTML.
```

### Checklist desta secao

- [ ] O tema foi identificado.
- [ ] Contexto previo, se fornecido, foi capturado.
- [ ] Arquivos nao foram criados com entrada incompleta.
- [ ] A saida planejada e somente `roadmap.html` com tres niveis coordenados.
- [ ] Nenhum nivel foi planejado com mais de 20 nodes.
- [ ] O pedido pratico, se existir, foi convertido para base teorica.

## 2. Slug e Pasta de Trabalho

Gere o slug principal a partir do tema, nao do contexto opcional.

Regras de slug:

- minusculas;
- sem acentos;
- espacos e separadores viram `-`;
- somente `a-z`, `0-9` e `-`;
- hifens repetidos colapsados;
- sem hifen no inicio ou no fim;
- curto, preservando termos tecnicos;
- se ficar vazio, use `roadmap`.

Use sempre:

```text
.tmp/roadmaps/<slug>/
```

Se a pasta existir, recrie somente a pasta do slug. Antes de apagar, valide que
o caminho resolvido esta dentro de `.tmp/roadmaps/`, nao contem `..`, nao e
`.tmp/`, nao e `.tmp/roadmaps/` e nao aponta para fora do workspace.

### Checklist desta secao

- [ ] O slug foi derivado do tema.
- [ ] O slug segue o formato permitido.
- [ ] A pasta resolvida ficou dentro de `.tmp/roadmaps/`.
- [ ] Somente `.tmp/roadmaps/<slug>/` foi recriada.
- [ ] O HTML final foi salvo dentro da pasta do slug.

## 3. Asset Visual Obrigatorio

Antes de gerar qualquer conteudo final, leia:

```text
    roadmap-page/assets/roadmap-page-template.html
```

Use `roadmap-page-template.html` como referencia visual: tipografia simples, leitura
confortavel, bordas discretas, tabelas limpas, blocos de chamada, cards curtos e
responsividade basica.

Leia tambem:

```text
common/references/visual-system.md
roadmap-page/references/roadmap-contract.md
roadmap-page/references/roadmap-quality-pipeline/pipeline.md
```

Nao copie textos de exemplo do template visual para o roadmap.

Nao referencie o asset no HTML final como fonte tematica.

### Checklist desta secao

- [ ] O template visual foi lido antes de escrever o HTML.
- [ ] O HTML final usou o estilo como referencia, sem copiar exemplos.
- [ ] O asset nao foi citado como referencia tematica.
- [ ] O HTML final ficou limpo, escaneavel e responsivo.
- [ ] Cards foram usados apenas para resumos curtos ou itens repetidos.

## 4. Pesquisa Web e Fontes

Pesquisa web e obrigatoria antes de definir os nodes finais.

Priorize:

1. documentacao oficial;
2. especificacoes, standards, RFCs, PEPs ou normas equivalentes;
3. manuais e guias tecnicos reconhecidos;
4. papers e materiais de referencia;
5. fontes secundarias apenas para clareza conceitual ou contexto.

Verifique datas, versoes e mudancas recentes quando o tema depender de
tecnologia, produto, ferramenta, norma, legislacao ou pratica operacional.

Cada fonte usada deve aparecer no HTML com:

- link clicavel;
- tipo de fonte;
- motivo de uso;
- nodes que sustenta;
- limite da fonte, quando relevante.

Nao invente URLs, versoes, comandos, APIs, conceitos, limitacoes ou
comportamentos.

Se a pesquisa falhar e for essencial, bloqueie a geracao. Nao gere roadmap
fingindo que pesquisou.

### Checklist desta secao

- [ ] Pesquisa web foi feita antes dos nodes finais.
- [ ] Fontes primarias foram priorizadas.
- [ ] Fontes secundarias tiveram motivo claro.
- [ ] Datas e versoes foram verificadas quando relevantes.
- [ ] Fontes usadas aparecem no HTML com motivo.
- [ ] Nenhum link ou fato instavel foi inventado.

## 5. Interpretacao e Recorte

Normalize a entrada antes de curar o roadmap.

Modele internamente:

```text
tema principal:
recorte escolhido:
contexto opcional fornecido:
objetivo final:
profundidade:
limites explicitos:
premissas inferidas:
ambiguidades:
```

Nao exponha esse modelo no chat. Use-o para orientar pesquisa, curadoria e
ordem dos nodes.

Se uma ambiguidade puder gerar roadmaps incompativeis, pergunte antes de criar
arquivos. Se a ambiguidade for leve, escolha a interpretacao mais provavel e
registre a premissa no HTML.

Quando a pessoa fornecer conhecimentos previos, experiencia, senioridade,
objetivo ou contexto relevante, esse contexto deve afetar decisoes reais:
profundidade, vocabulario, ritmo, pre-requisitos, limites e exemplos
conceituais. Se ela nao fornecer esse contexto, use uma premissa neutra e nao
finja personalizacao.

### Checklist desta secao

- [ ] Tema e recorte foram normalizados.
- [ ] Contexto previo foi usado somente quando fornecido.
- [ ] Ambiguidades fortes foram resolvidas com pergunta.
- [ ] Premissas leves foram registradas no HTML.
- [ ] Contexto previo fornecido influenciou decisoes concretas.
- [ ] O escopo nao foi ampliado por iniciativa propria.

## 6. Inventario e Curadoria de Topicos

Antes de definir nodes, crie um inventario candidato.

Inclua apenas topicos que podem contribuir para:

- fundamentos indispensaveis;
- vocabulario tecnico;
- modelos mentais;
- arquitetura, fluxo ou estrutura central;
- decisoes e trade-offs;
- riscos e limites;
- seguranca, diagnostico, observabilidade ou validacao quando aplicavel;
- boas praticas e antipadroes como criterios conceituais.

Classifique mentalmente cada topico como:

- manter;
- unir;
- dividir;
- remover;
- reservar para outro nivel;
- reservar para node futuro do mesmo nivel;
- fora de escopo.

Um topico vira node somente se introduz camada conceitual nova, muda o modelo
mental, e pre-requisito importante ou exige criterio de dominio proprio.

Depois do inventario, distribua os topicos entre os tres niveis antes de fechar
qualquer lista local de nodes:

- `basico`: conceitos que criam a base comum, linguagem, partes essenciais,
  modelos mentais e criterios iniciais de leitura do tema;
- `intermediario`: relacoes entre partes, arquitetura, fluxo, composicao,
  decisoes, trade-offs e efeitos de uma escolha sobre outra;
- `avancado`: limites do modelo, excecoes, falhas, diagnostico conceitual,
  comportamento interno sofisticado, criterios de especialista e fronteiras de
  confianca.

Planeje os tres niveis no mesmo contexto de pesquisa e curadoria. Nao finalize
o `basico` isoladamente se isso puder roubar espaco ou repetir assunto que
pertence melhor a `intermediario` ou `avancado`.

### Checklist desta secao

- [ ] Houve inventario antes dos nodes finais.
- [ ] Topicos secundarios foram removidos ou unidos.
- [ ] Topicos grandes demais foram divididos.
- [ ] Cada node final tem justificativa semantica.
- [ ] Cada topico mantido foi alocado em exatamente um nivel principal.
- [ ] Temas pequenos nao foram inflados para ocupar todos os 60 nodes possiveis.
- [ ] A curadoria reduziu repeticao e inflacao.
- [ ] Topicos fora de escopo nao viraram nodes.

## 7. Niveis e Correntes de Nodes

Crie tres correntes locais de nodes, uma por nivel:

```text
basico:        Node 01 -> Node 02 -> ... -> Node N
intermediario: Node 01 -> Node 02 -> ... -> Node N
avancado:      Node 01 -> Node 02 -> ... -> Node N
```

Cada node deve assumir que os nodes anteriores do mesmo nivel ja foram
estudados. `intermediario` pode assumir a base conceitual do `basico` como
pre-requisito de nivel, e `avancado` pode assumir a base dos dois niveis
anteriores. Isso nao autoriza repetir definicoes: use o que veio antes como
pre-requisito herdado.

Cada node precisa de:

- `level`: `basico`, `intermediario` ou `avancado`;
- `node_id`: identificador global no formato `<level>/<slug>`;
- `label`: titulo humano;
- `slug`: identificador estavel no formato `NN-slug`;
- `order`: posicao numerica local dentro do nivel;
- papel na corrente local e no conjunto tri-level;
- pre-requisitos herdados;
- conceito novo introduzido;
- fronteira do que cobre;
- fronteira do que nao cobre.

Regras do slug do node:

- dois digitos;
- hifen;
- slug sem acentos e em minusculas;
- sem duplicidade dentro do mesmo nivel;
- ordem numerica igual a ordem da corrente local.

O mesmo `slug` pode existir em niveis diferentes apenas quando isso for
semantica e mecanicamente inevitavel; nesse caso, `node_id` continua distinguindo
os nodes. Prefira slugs localmente claros para reduzir ambiguidade humana.

### Checklist desta secao

- [ ] Os tres niveis existem no plano.
- [ ] Cada nivel tem no maximo 20 nodes.
- [ ] A ordem dos nodes segue dependencia real dentro de cada nivel.
- [ ] Todo node tem label.
- [ ] Todo node tem slug `NN-slug`.
- [ ] Todo node tem `level` e `node_id`.
- [ ] Nao ha `node_id` duplicado.
- [ ] Cada transicao local prepara a proxima.
- [ ] Nenhum node exige conceito ainda nao introduzido sem pre-requisito declarado.

## 8. Anti-Repeticao

O roadmap deve tratar repeticao como defeito.

Antes de finalizar as listas locais de nodes, monte uma matriz anti-repeticao
global com:

- conceito;
- `node_id` de primeira introducao;
- retomadas permitidas;
- retomadas proibidas;
- motivo da fronteira.

Inclua essa matriz no HTML.

Em nodes posteriores no mesmo nivel ou em outro nivel, conceitos anteriores
podem aparecer somente como:

- pre-requisito herdado;
- lembrete curto;
- contraste;
- nova camada explicitamente justificada.

Nao redefina conceitos ja ensinados.

Nao use o mesmo exemplo conceitual em varios nodes.

Nao repita a mesma referencia em todos os nodes sem motivo local.

Use a matriz global para decidir fronteiras antes de consolidar cada nivel. Em
seguida, valide a anti-repeticao local de cada nivel. A matriz global evita
sobreposicao entre `basico`, `intermediario` e `avancado`; a revisao local
evita repeticao dentro de um nivel.

### Checklist desta secao

- [ ] A matriz anti-repeticao global foi criada antes das listas finais.
- [ ] Cada conceito central tem `node_id` de introducao unico.
- [ ] As fronteiras entre niveis foram definidas antes da escrita final.
- [ ] Retomadas posteriores sao lembretes ou novas camadas justificadas.
- [ ] Exemplos repetidos foram removidos.
- [ ] Referencias repetidas tem motivo local.
- [ ] A matriz anti-repeticao aparece no HTML.

## 9. Contrato de Cada Node

Cada node deve ser um playbook para outro agente escrever documentacao completa
depois.

Cada secao de node no HTML deve conter:

- level;
- node_id;
- label;
- slug;
- order local;
- papel do node na corrente local e no conjunto tri-level;
- pre-requisitos herdados;
- o que introduz pela primeira vez;
- o que o proximo agente deve cobrir;
- o que o proximo agente nao deve cobrir;
- perguntas que o node deve responder;
- conceitos, termos, ferramentas, arquivos, comandos, parametros ou APIs como vocabulario conceitual;
- exemplos conceituais, analogias curtas ou diagramas permitidos;
- armadilhas e erros comuns;
- criterio de dominio antes de avancar;
- handoff para o proximo node;
- referencias especificas com link e motivo.

O bloco "deve cobrir" precisa ser denso: subtopicos, relacoes, decisoes, riscos,
limites e pontos que exigem explicacao longa futura.

O bloco "nao deve cobrir" precisa impedir repeticao, antecipacao e pratica
proibida.

Comandos podem aparecer apenas como vocabulario conceitual: para que existem,
quando aparecem, que informacao revelam, que risco de interpretacao carregam.
Nunca escreva sequencia de execucao.

### Checklist desta secao

- [ ] Todo node contem todos os blocos obrigatorios.
- [ ] Todo node declara `level`, `node_id`, `order`, label e slug.
- [ ] O bloco "deve cobrir" e especifico e util para documentacao futura.
- [ ] O bloco "nao deve cobrir" protege fronteira e anti-repeticao.
- [ ] Perguntas sao concretas, nao genericas.
- [ ] Criterios de dominio verificam compreensao, nao execucao pratica.
- [ ] Referencias por node tem motivo local.

## 10. Estrutura do HTML

O HTML final deve ser autocontido e conter:

- `<!doctype html>`, `html lang="pt-BR"`, `meta charset="utf-8"` e viewport;
- CSS embutido;
- titulo;
- contexto informado ou premissa neutra;
- compreensao final esperada;
- data da pesquisa;
- premissas e limites;
- mapa tri-level;
- lista resumida navegavel dos nodes por nivel com label, slug, `node_id` e
  link interno para a secao completa do node no proprio `roadmap.html`;
- matriz anti-repeticao global;
- secoes completas dos nodes agrupadas por nivel;
- checklist final de cobertura;
- referencias consolidadas.

Use tabelas para matrizes, listas e referências. Use componentes HTML/CSS para
mapas, fluxos e sequências visuais. Use `<pre>` apenas para texto literal,
código, configuração ou ASCII excepcional justificado.
Use cards apenas para resumos curtos.

Cada secao completa de node deve ter `id` estavel no formato
`<level>-<node-slug>`, alem de `data-level`, `data-node-id` e
`data-node-slug`. A lista resumida deve apontar para esse `id` com link interno.
Quando `<level>/<node-slug>/node.html` ja existir dentro do roadmap, o resumo
tambem deve apontar para esse arquivo com link relativo. Quando ainda nao
existir, deixe o node como planejado ou pendente, sem link quebrado.

Nao use `flow-steps` ou componente equivalente para representar a lista de
nodes quando ele mostrar apenas numeros sem label, slug, `node_id` e links.

Nao deixe Markdown cru no HTML.

Nao escreva secoes chamadas `Laboratorio`, `Exercicio`, `Projeto final`,
`Desafio pratico` ou `Hands-on`.

### Checklist desta secao

- [ ] O HTML contem todas as secoes obrigatorias.
- [ ] O HTML e autocontido e tem CSS embutido.
- [ ] O HTML contem secoes para `basico`, `intermediario` e `avancado`.
- [ ] O mapa, lista de nodes por nivel e matriz global sao coerentes entre si.
- [ ] A lista resumida dos nodes e navegavel e nao usa blocos apenas numericos.
- [ ] Cada node tem link interno para sua secao completa.
- [ ] Links relativos para `node.html` existem somente quando o arquivo existe.
- [ ] Nao ha Markdown cru.
- [ ] Nao ha secoes praticas proibidas.
- [ ] Referencias consolidadas aparecem no final.

## 11. Validacao Final e Recuperacao

Antes de responder, verifique:

- `roadmap.html` existe;
- `.roadmap/roadmap-contract.json` existe e e JSON valido;
- `.roadmap/roadmap-contract.json` passa no schema versionado;
- o arquivo nao esta vazio;
- o HTML contem estrutura obrigatoria;
- o HTML contem os tres niveis;
- nenhum nivel tem mais de 20 nodes;
- o HTML e o contrato JSON concordam sobre niveis, `node_id`, slugs e ordem
  local dos nodes;
- todos os nodes tem `NN-slug`;
- todos os nodes tem `node_id` no formato `<level>/<slug>`;
- todos os nodes tem `id` HTML estavel no formato `<level>-<slug>`;
- a lista resumida dos nodes contem label, slug, `node_id` e link interno para
  cada secao completa;
- links relativos para `node.html` existem somente para nodes ja criados;
- cada node tem referencias;
- matriz anti-repeticao global existe;
- `.roadmap/pipeline/01-html-shape/html-shape-audit.md` registra passagem;
- `.roadmap/pipeline/02-contract-schema/contract-schema-audit.md` registra passagem;
- `.roadmap/pipeline/03-contract-consistency/contract-consistency-audit.md` registra passagem;
- `.roadmap/pipeline/04-source-coverage/source-audit.md` registra passagem;
- `.roadmap/pipeline/05-visual-render/visual-audit.md` registra passagem;
- `.roadmap/pipeline/05-visual-render/render-checks.json` registra passagem;
- o pipeline de qualidade de `roadmap-page` foi executado ate ponto fixo;
- a auditoria visual renderizada verificou largura de conteudo e mobile;
- mapas, fluxos e sequências visuais usam HTML/CSS, não `<pre>` como atalho;
- checklist final existe no HTML;
- nao existe `prompt.md`;
- nao ha laboratorio, exercicio, hands-on ou projeto final;
- a pesquisa foi representada no HTML com fontes reais.

Se algo falhar, corrija antes de responder.

Se a pesquisa falhar por rede, bloqueie e informe.

Se a validacao mostrar node raso, volte para curadoria e aprofunde com conteudo
tecnico: riscos, limites, decisoes, perguntas e referencias. Nao aumente volume
com frase decorativa.

### Checklist desta secao

- [ ] O arquivo final existe.
- [ ] O HTML passou na verificacao estrutural.
- [ ] Proibicoes praticas foram verificadas.
- [ ] Falhas encontradas foram corrigidas ou bloqueadas.
- [ ] A pesquisa aparece com fontes reais no HTML.
- [ ] A resposta final ficou curta e sem conteudo do arquivo.
