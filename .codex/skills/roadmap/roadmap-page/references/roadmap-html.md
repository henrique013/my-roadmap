# Contrato de `roadmap.html`

`roadmap.html` é a página humana do roadmap. Ela deve ser autocontida, legível e
coerente com `.roadmap/roadmap-contract.json`.

## Estrutura Obrigatória

O HTML deve conter:

- `<!doctype html>`;
- `html lang="pt-BR"`;
- `meta charset="utf-8"`;
- viewport;
- CSS embutido;
- `<title>` e `<h1>`;
- contexto informado ou premissa neutra;
- compreensão final esperada;
- data da pesquisa;
- premissas e limites;
- mapa tri-level;
- seções para `basico`, `intermediario` e `avancado`;
- lista resumida navegável dos nodes por nível;
- matriz anti-repetição global;
- seções completas dos nodes agrupadas por nível;
- checklist final de cobertura;
- referências consolidadas.

Cada seção de nível deve ter `data-level` com valor `basico`,
`intermediario` ou `avancado`.

A lista resumida de nodes por nível deve funcionar como índice humano. Cada
item deve expor:

- ordem local;
- label do node;
- `node_id`;
- slug;
- link interno para a seção completa do node no próprio `roadmap.html`.

Se o arquivo `<level>/<node-slug>/node.html` já existir, o mesmo item também
deve expor um link relativo para essa página profunda. Se o arquivo ainda não
existir, não crie link quebrado para ele; deixe o node claramente como planejado
ou pendente.

Não use um bloco apenas numérico, como `01`, `02`, `03`, para representar a
lista resumida dos nodes.

Cada seção completa de node deve ter `id` estável derivado de
`<level>-<slug>` e também:

```html
<section id="intermediario-07-rendering-behavior" data-level="intermediario" data-node-id="intermediario/07-rendering-behavior" data-node-slug="07-rendering-behavior">
```

O `data-node-id` é a identidade mecânica usada por `node-pages` e deve ser
igual a `<level>/<slug>`.

## Seções de Node

Cada seção de node deve expor:

- level;
- node_id;
- label;
- slug `NN-slug`;
- order local do nível;
- papel na corrente local e no conjunto tri-level;
- pré-requisitos herdados;
- o que introduz pela primeira vez;
- o que deve cobrir;
- o que não deve cobrir;
- perguntas;
- vocabulário conceitual;
- exemplos conceituais ou diagramas permitidos;
- armadilhas;
- critério de domínio;
- handoff;
- referências específicas.

O HTML deve ajudar outro agente a gerar `node-pages` sem adivinhar escopo.
Para isso, a identidade humana (`label`, `slug`) e a identidade mecânica
(`level`, `node_id`) precisam aparecer no HTML e no JSON.

## Proibições

- Não deixe Markdown cru.
- Não crie `prompt.md`.
- Não gere laboratório, exercício, hands-on, desafio prático ou projeto final.
- Não transforme comandos em roteiro de execução.
- Não use `flow-steps` ou qualquer componente equivalente como lista resumida
  de nodes quando os itens expõem apenas números sem label, `node_id`, slug e
  link interno.
- Não use texto de corpo com largura menor que a largura útil sem justificativa
  visual explícita.
- Não use `<pre>` como atalho para mapa, fluxo, sequência, linha do tempo,
  estado ou contraste conceitual simples.

## Primitivas Visuais

Use tabelas para matrizes, listas e referências. Use componentes HTML/CSS para
mapas, fluxos, sequências e relações visuais. Use `<pre>` apenas para texto
literal, código, configuração ou ASCII excepcional justificado.

Quando ASCII for exceção, o bloco deve ter `data-ascii-exception="true"`,
`data-ascii-reason` não vazio e justificativa no audit visual.

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

Snippets técnicos que mostram JSON, configuração, regra, parâmetro, campo, API,
comando, consulta ou formato devem ter highlight semântico mínimo. Use classes
`syntax-*` no próprio HTML quando não houver biblioteca local de highlight. Um
bloco monocromático só passa para texto literal quando a ausência de highlight
estiver justificada em `.roadmap/pipeline/05-visual-render/visual-audit.md`.

Exemplo de JSON/configuração com highlight manual:

```html
<pre class="code-block language-json" aria-label="Exemplo conceitual de evento estruturado">
<code>{
  <span class="syntax-key">"level"</span><span class="syntax-op">:</span> <span class="syntax-value">"error"</span>,
  <span class="syntax-key">"message"</span><span class="syntax-op">:</span> <span class="syntax-value">"Falha ao consultar pedido"</span>,
  <span class="syntax-key">"status_code"</span><span class="syntax-op">:</span> <span class="syntax-value">500</span>
}</code></pre>
```

Exemplo de CloudWatch Logs Insights com highlight manual:

```html
<pre class="code-block language-cwl" aria-label="Consulta conceitual de Logs Insights">
<code><span class="syntax-key">fields</span> <span class="syntax-value">@timestamp</span>, <span class="syntax-value">route</span>, <span class="syntax-value">status_code</span>
<span class="syntax-op">|</span> <span class="syntax-key">filter</span> <span class="syntax-value">status_code</span> <span class="syntax-op">&gt;=</span> <span class="syntax-value">500</span>
<span class="syntax-op">|</span> <span class="syntax-key">stats</span> <span class="syntax-key">count</span><span class="syntax-op">()</span> <span class="syntax-key">by</span> <span class="syntax-value">route</span></code></pre>
```

## Relação com o Contrato JSON

O HTML e o JSON devem concordar sobre:

- slug do roadmap;
- níveis presentes;
- ordem local dos nodes em cada nível;
- `node_id`, `level`, slug e label de cada node;
- âncora interna estável de cada seção completa de node;
- links relativos para `node.html` apenas quando o arquivo existir;
- conceitos introduzidos;
- escopo positivo e negativo;
- referências por node;
- matriz anti-repetição global.

Se houver divergência, corrija o HTML ou o JSON antes de responder.
