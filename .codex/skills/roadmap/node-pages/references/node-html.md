# Contrato de `node.html`

O HTML é uma narrativa técnica derivada do tema. Ele não deve ter formato fixo.

Narrativa, aqui, não significa conto, personagem, fábula ou entretenimento.
Narrativa significa ordem de entendimento: a sequência pela qual uma pergunta
técnica vira compreensão.

`node.html` não representa o `research-dump.md`. O dump guarda fatos, fontes,
limites e preparação conceitual. O HTML transforma isso em um capítulo técnico
que conduz o leitor por uma linha de raciocínio.

## Antes de Escrever

Leia o `research-dump.md` completo e `.editorial/concept-ledger.md` antes de
escrever. Faça internamente o projeto narrativo:

1. encontre a pergunta-motor;
2. escolha a narrativa dominante;
3. escolha o exemplo técnico condutor;
4. ordene os conceitos por dependência;
5. decida quais relações realmente precisam de visual;
6. defina títulos que nascem do assunto, não de um template.

Essa etapa não precisa virar arquivo separado. Ela precisa aparecer no resultado.

Se o HTML precisar de conceito, alias, fonte, fronteira ou explicação que não
esteja no dump e no ledger, atualize primeiro `research-dump.md` e
`.editorial/concept-ledger.md`.

## Pergunta-Motor

A pergunta-motor é a pergunta que faz o node existir para o leitor. Ela deve
abrir uma tensão técnica real.

Fraco:

```text
O que é WAL?
```

Melhor:

```text
Como um banco sabe o que recuperar depois de confirmar uma mudança e cair antes
de atualizar todos os arquivos finais?
```

Fraco:

```text
O que são índices?
```

Melhor:

```text
Como o banco evita olhar linha por linha quando a consulta procura uma pequena
parte dos dados?
```

Não escreva uma seção chamada `Objetivo`. Encontre a pergunta que faz o node
existir e comece por ela ou por uma situação técnica que a torne inevitável. O
leitor deve entender a direção da página pelo problema que ela abre, não por um
aviso sobre o que o autor pretende ensinar.

## Narrativa Variável por Tema

A narrativa dominante deve nascer do node. Não use a mesma forma para todos os
HTMLs.

Lentes possíveis:

- processo: quando o assunto é como algo acontece em fases;
- causal: quando o centro é por que algo acontece e o que isso provoca;
- topológica: quando o leitor precisa entender partes e relações;
- contraste: quando duas ideias parecidas precisam ser separadas;
- diagnóstico: quando o leitor interpreta sinais e hipóteses;
- trade-off: quando cada escolha muda risco, custo ou comportamento;
- ciclo de vida: quando um objeto ou estado nasce, muda e termina;
- fronteira conceitual: quando o mecanismo serve para algo, mas não para outra
  coisa.

Essas lentes não são modelos fixos. Um node pode combinar mais de uma, mas deve
haver uma dominante para orientar ordem, exemplo, visuais e fechamento.

Se dois nodes diferentes saem com a mesma abertura, os mesmos títulos e os
mesmos componentes, a skill provavelmente falhou.

## Conceito Antes do Uso

Regra central:

```text
Não use um termo técnico antes de construir a necessidade dele.
```

A sequência de escrita deve seguir esta disciplina:

```text
necessidade do leitor
  -> explicação em linguagem comum
    -> nome técnico
      -> uso do termo em raciocínios futuros
```

Isso vale para:

- siglas;
- parâmetros;
- arquivos;
- funções;
- views;
- papéis;
- estados;
- mecanismos;
- nomes de arquitetura;
- comandos tratados como vocabulário;
- títulos;
- lead;
- cards;
- callouts;
- tabelas;
- diagramas;
- legendas;
- labels;
- `aria-label`;
- referências;
- qualquer texto dentro de componente visual.

O que já foi estabelecido por nodes anteriores do mesmo nível, ou por níveis
anteriores declarados como pré-requisito no contrato, pode ser usado como base.
O que o roadmap diz que este node introduz pela primeira vez precisa ser
preparado antes de ser nomeado.

Use `.editorial/concept-ledger.md` para decidir se um conceito pode aparecer,
qual explicação mínima precisa vir antes e quais aliases ou paráfrases também
contam como uso. Não basta remover a sigla literal se a ideia equivalente
continua aparecendo cedo demais.

## Relação com o Pipeline de Qualidade

Depois da primeira geração do HTML, a skill executa
`references/html-quality-pipeline/pipeline.md`.

As regras deste arquivo orientam a escrita inicial. O pipeline valida o HTML
pronto, materializa `.editorial/pipeline/01-visible-text/visible-text.md`,
`.editorial/pipeline/02-concept-introduction/concept-audit.md`, `.editorial/pipeline/03-example-sufficiency/example-audit.md` e
os `revision-plan.md` dos pipes que podem exigir reescrita, reescreve problemas
e repete os guardrails até ponto fixo.

Quando disponíveis, use os scripts internos para extrair texto visível,
procurar aliases bloqueados literais e validar a forma mecânica do HTML. Eles
não decidem se a narrativa está suficiente nem se uma paráfrase semântica vazou
conceito; essa auditoria continua sendo responsabilidade do agente.

Não trate a primeira versão bem escrita como final. O HTML final é aquele que
passou pelo pipeline sem pendências relevantes.

Conceito antes do uso vale para títulos, lead, tabelas, cards, callouts,
diagramas, legendas, labels, `aria-label` e referências, não apenas para
parágrafos.

Antes de considerar `node.html` final, use `.editorial/concept-ledger.md` e
`.editorial/pipeline/01-visible-text/visible-text.md` para auditar a primeira ocorrência de cada
conceito e alias. A regra vale para todo texto visível ou semivisível,
incluindo referências e `aria-label`.

## Exemplo Condutor

Escolha um exemplo técnico condutor. Ele deve ser pequeno, concreto e recorrente.

O exemplo condutor deve:

- atravessar várias partes da explicação;
- mostrar mudança de estado, decisão, fluxo ou contraste;
- reduzir abstração sem infantilizar;
- carregar apenas o contexto técnico necessário;
- evoluir junto com a narrativa.

O exemplo condutor não deve:

- virar historinha com personagem;
- depender de contexto de negócio irrelevante;
- virar laboratório;
- exigir que o leitor execute comandos;
- ser repetição disfarçada de exemplo usado no node anterior.

Exemplos de natureza possível:

- uma transação confirmada atravessa estados em um mecanismo de replicação;
- uma consulta passa de varredura ampla para busca seletiva;
- uma leitura passa por miss, fill, hit e invalidez;
- um sintoma técnico é acompanhado até hipóteses concorrentes.

Esses exemplos não são templates. Eles mostram o tipo de carga técnica que um
exemplo condutor deve carregar.

## Exemplos Como Complemento, Não Base

A página continua sendo uma narrativa técnica em prosa. Exemplos, snippets,
tabelas e visuais entram apenas quando reduzem uma ambiguidade essencial.

Use suporte concreto quando o leitor precisar ver forma, estado, ordem,
contraste ou fronteira para entender o conceito. Não use exemplo para decorar,
repetir a prosa ou transformar o node em laboratório.

Quando o HTML explicar arquivo de configuração, regra, linha, campo, formato,
schema, API ou comando, inclua um exemplar mínimo de leitura conceitual, salvo
se houver motivo explícito no dump para não fazer isso.

## Primitivas Visuais

Código, configuração, arquivo estruturado, log, saída textual, gramática e
formato literal usam `<pre><code>`.

Visual conceitual usa HTML/CSS semântico, não `<pre>`. Linha do tempo, fluxo
simples, estado antes/depois, topologia, lane, barra de atraso/progresso,
fronteira e contraste visual devem ser componentes HTML/CSS por padrão.

Componentes úteis:

- `.timeline` para ordem temporal;
- `.flow-steps` para passos conectados;
- `.state-grid` para antes/depois ou estados concorrentes;
- `.topology` para partes e relações;
- `.lane-map` para trilhas paralelas, filas ou responsabilidades.

ASCII é exceção estreita. Quando usar, o `<pre>` deve ter
`data-ascii-exception="true"` e `data-ascii-reason` não vazio, com justificativa
no `research-dump.md` e em `.editorial/pipeline/05-visual-render/visual-audit.md` explicando por que
HTML/CSS seria pior.

Snippet conceitual é permitido quando:

- é curto;
- usa placeholders seguros;
- não forma sequência executável;
- vem acompanhado de leitura do significado;
- explica risco, limite ou fronteira;
- não invade node futuro.

Snippet conceitual é proibido quando:

- vira roteiro de execução;
- exige que o leitor rode comandos;
- substitui a explicação;
- inclui detalhes de ambiente;
- abre tópico reservado a outro node.

## Snippets e Código Renderizado

Inline `code` e bloco `<pre><code>` têm papéis visuais diferentes. Inline
`code` deve parecer uma etiqueta curta dentro da frase. Bloco de código deve
parecer uma superfície única de leitura.

Quando usar `<pre><code>`, defina explicitamente `pre code` no CSS para remover
fundo, borda, padding e `border-radius` herdados de inline `code`:

```css
pre code {
  color: inherit;
  background: transparent;
  border: 0;
  border-radius: 0;
  padding: 0;
  font: inherit;
}
```

Snippets técnicos que mostram configuração, regra, parâmetro, campo, API,
comando ou formato devem ter highlight semântico mínimo. Use classes `syntax-*`
no próprio HTML quando não houver biblioteca local de highlight. Um bloco
monocromático só passa para texto literal quando a ausência de highlight estiver
justificada em `.editorial/pipeline/05-visual-render/visual-audit.md`. Visual conceitual simples não deve
usar `<pre>` como atalho.

Exemplo de snippet conceitual com highlight manual:

```html
<pre class="code-block language-conf" aria-label="Recorte conceitual de configuração">
<code><span class="syntax-key">parametro_principal</span> <span class="syntax-op">=</span> <span class="syntax-value">valor_preparado</span>
<span class="syntax-key">limite_de_saida</span> <span class="syntax-op">=</span> <span class="syntax-value">&lt;placeholder_conceitual&gt;</span>
<span class="syntax-key">reserva_por_consumidor</span> <span class="syntax-op">=</span> <span class="syntax-value">&lt;limite_planejado&gt;</span></code></pre>
```

Blocos de código devem ter contraste adequado e caber no mobile com rolagem
interna, sem criar overflow horizontal global. Exemplos de configuração,
parâmetros, campos e regras precisam ser legíveis no navegador, não apenas
corretos no texto do arquivo.

Texto comum deve usar a largura útil do contêiner. Não use `max-width` local em
`p`, `.lead` ou `.callout` para criar uma coluna menor dentro de um `main`
amplo. Se a leitura ficar larga demais, reduza `main`.

A página final precisa ser inspecionada renderizada em desktop e mobile. Não
considere `node.html` final apenas por reler o HTML ou o CSS como texto.

## Visualização Como Pensamento

Use visual quando ele tornar uma relação mais clara. Não use visual para
decorar, preencher espaço ou criar aparência de organização.

Pergunte o que precisa ficar visível:

- o que está mudando?
- em que ordem acontece?
- onde cada parte está?
- o que está mais avançado ou atrasado?
- qual estado existe antes e depois?
- o que se parece mas não é igual?
- que causa produz qual consequência?
- onde está a fronteira entre dentro e fora do escopo?

Mapeamento útil, sem virar obrigação:

```text
ordem temporal -> linha do tempo ou etapas conectadas
causa e consequência -> fluxo causal com condições
partes e relações -> diagrama topológico
contraste -> comparação lado a lado ou matriz curta
acúmulo ou atraso -> barras, filas ou marcadores
fronteira de escopo -> mapa dentro/fora
decisão -> árvore simples ou caminho com trade-offs
```

Use componentes como `.timeline`, `.flow-steps`, `.state-grid`, `.topology` e
`.lane-map` para essas relações. Use `<pre><code>` apenas quando o conteúdo é
literal, como código, configuração, formato, log ou gramática.

Cada visual precisa ter texto antes e depois:

- antes, uma frase prepara o olhar;
- depois, uma frase interpreta a conclusão.

Se o visual não muda o entendimento, remova.

## Tabelas e Resumos

Tabela é boa para consolidar comparação depois que o leitor já tem contexto.
Tabela é ruim como primeiro contato com o coração do node.

Pode usar tabela para:

- comparar ideias já apresentadas;
- consolidar vocabulário no fim;
- mapear fonte, tópico e limite;
- resumir trade-offs depois da explicação.

Não use tabela para:

- abrir a página;
- introduzir o conceito principal;
- substituir a explicação;
- esconder uso prematuro de vocabulário técnico.

## Texto Adulto

Escreva para uma pessoa adulta e inteligente que ainda não tem todos os encaixes
do assunto.

Evite:

- `vamos aprender`;
- `agora você sabe`;
- `este é o objetivo`;
- `ao final você vai saber`;
- `antes de avançar, confirme`;
- `pense assim`;
- frases motivacionais;
- piadas;
- metáforas laterais que roubam foco;
- tom de professor falando com criança.

Prefira:

- situar o problema;
- explicar o mecanismo;
- mostrar a consequência;
- nomear o conceito no momento certo;
- voltar ao exemplo condutor;
- fechar blocos densos com uma conclusão técnica curta.

O texto pode ser simples sem ser pobre. Simples significa direto, preciso e sem
exibicionismo.

## Títulos Derivados da Narrativa

Os títulos devem carregar ideias técnicas do momento narrativo. Eles não devem
expor a engrenagem pedagógica.

Evite títulos como:

- `Objetivo do node`;
- `Mapa mental`;
- `Vocabulário técnico`;
- `Pré-requisitos herdados`;
- `Critério de domínio`;
- `Checklist final`.

Títulos possíveis, quando o tema pedir:

- `Quando uma mudança confirmada ainda não está nos arquivos finais`;
- `A posição no fluxo importa mais que o relógio`;
- `Receber uma mudança não é o mesmo que aplicá-la`;
- `O limite de uma cópia física`;
- `O ponto em que replicação deixa de ser backup`.

Não copie esses títulos como modelo. Eles mostram o princípio: o título deve
nascer da explicação, não da lista de seções do dump.

## Relação com o Dump

Use o dump como fonte principal. Se o HTML precisar de algo que não está no
dump, atualize o dump primeiro. Se esse algo for conceito, alias, fonte ou
fronteira de escopo, atualize também `.editorial/concept-ledger.md` antes de
revisar o HTML.

Separação obrigatória:

```text
research-dump.md
  - guarda fatos, fontes, limites, riscos e ordem conceitual
  - pode ser explícito, metódico e auditável
  - pode ter listas, tabelas e critérios
  - não precisa ser bonito

node.html
  - transforma fatos em entendimento
  - precisa de ritmo, transição e progressão
  - não deve expor a engrenagem pedagógica
  - não deve parecer checklist
```

Validação importante:

```text
Se os títulos do HTML se parecem com as seções do dump, provavelmente falhou.
```

## Referências Finais

Referências finais também são texto visível. O texto do link não pode introduzir
um termo técnico que o capítulo ainda não preparou.

Se o título oficial de uma fonte carregar conceito não preparado:

- prepare o conceito antes da referência;
- adapte o texto visível do link para uma forma já preparada;
- ou deixe a fonte apenas no `research-dump.md` quando ela não for essencial ao
  HTML visível.

Não use uma referência final para fazer vazar conceito reservado a node futuro.
Títulos de fonte, labels de link e comentários finais entram na auditoria de
`.editorial/pipeline/01-visible-text/visible-text.md`.

## Proibições no Corpo Principal

O HTML não deve conter:

- dump reformatado;
- página com seções fixas sempre iguais;
- cards de metadados como abertura;
- `Objetivo do node`;
- `Ao final você vai saber`;
- `Pré-requisitos herdados`;
- `Critério de domínio`;
- `Checklist final`;
- vocabulário técnico antes da explicação;
- tabelas como primeiro ensino;
- visual decorativo;
- metáfora lateral que rouba foco;
- fábula, personagem ou historinha;
- tom infantil;
- comandos para executar quando o node for conceitual;
- laboratório, exercício, hands-on, desafio ou projeto final;
- fórmula fixa de títulos.

Essas proibições valem para o HTML. O dump pode ter seções explícitas de
contrato, objetivo, escopo e critério porque ele é um artefato interno.

Esta lista explicita a proibição de HTML como dump reformatado, a proibição de
seções meta-expositivas no corpo principal, a proibição de fórmula fixa de
títulos e a proibição de infantilização do leitor.

## Estrutura Técnica Mínima

O arquivo deve conter:

- `<!doctype html>`;
- `html lang="pt-BR"`;
- `meta charset="utf-8"`;
- viewport;
- CSS embutido;
- título adequado ao node;
- referências comentadas no fim.

Mantenha boa hierarquia, leitura confortável, contraste suficiente e texto que
caiba nos seus elementos. Use o asset da skill como referência visual, não como
fonte de conteúdo nem como contrato de componentes.

## Validação de Qualidade

Antes de finalizar o HTML, verifique:

- a primeira tela abre uma pergunta técnica real ou uma situação que a torna
  inevitável;
- os títulos nascem do assunto, não de um template;
- a narrativa dominante combina com o node;
- o HTML não segue a estrutura do dump;
- as primeiras ocorrências relevantes de conceitos técnicos foram preparadas
  antes de aparecer;
- aliases e paráfrases de conceitos não preparados foram removidos ou
  preparados;
- referências finais não introduzem vocabulário técnico novo;
- o pipeline de qualidade foi executado até ponto fixo depois da primeira
  geração ou revisão do HTML;
- `.editorial/pipeline/01-visible-text/visible-text.md`, `.editorial/pipeline/02-concept-introduction/concept-audit.md`,
  `.editorial/pipeline/03-example-sufficiency/example-audit.md`,
  `.editorial/pipeline/04-visual-primitive-choice/primitive-audit.md`,
  `.editorial/pipeline/05-visual-render/visual-audit.md` e os `revision-plan.md`
  dos pipes `02`, `03`, `04` e `05` correspondem ao HTML final;
- o exemplo condutor volta ao longo da explicação;
- exemplos necessários aparecem quando forma, estado, ordem, contraste,
  fronteira ou risco ficariam abstratos demais só em prosa;
- exemplos excessivos foram removidos;
- snippets são conceituais, pequenos, acompanhados de leitura e não viram
  roteiro de execução;
- `pre code` não herda estilo visual de inline `code`;
- snippets técnicos têm highlight semântico mínimo ou justificativa registrada;
- visuais conceituais simples usam componentes HTML/CSS em vez de `<pre>`;
- screenshots desktop e mobile foram inspecionadas antes da entrega;
- não há overflow horizontal global em desktop ou mobile;
- os visuais mostram relações que o texto sozinho deixaria abstratas;
- tabelas aparecem apenas depois de contexto suficiente;
- o texto evita meta-exposição sobre o objetivo da aula;
- o leitor adulto é respeitado;
- o fechamento conclui a linha de entendimento em vez de entregar checklist
  escolar;
- as referências existem, são clicáveis e sustentam o que foi afirmado;
- o escopo positivo e o escopo negativo do roadmap foram respeitados.

Se qualquer item falhar, revise o dump ou o HTML antes de responder.
