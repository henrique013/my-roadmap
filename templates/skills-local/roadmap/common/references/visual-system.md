# Sistema Visual Compartilhado

## Tema Visual Único

Todo HTML gerado por esta skill usa um único tema visual: `notion-dark`.
Não crie switch de tema, modo claro alternativo nem CSS condicional para tema.

O elemento raiz do HTML deve expor o contrato visual de forma mecânica:

```html
<html lang="pt-BR" data-visual-theme="notion-dark">
```

Use `color-scheme: dark` no `:root` e no `body`.

## Tokens Semânticos

O tema `notion-dark` usa superfícies neutras escuras e cores semânticas
pontuais. A página não deve virar monocromática, mas cor só entra quando
carrega função: link, foco, tag, chamada, aviso, risco, sucesso, código,
tabela ou visual conceitual.

Base recomendada:

```css
:root {
  color-scheme: dark;
  --page: #191919;
  --surface: #202020;
  --surface-hover: #2a2a2a;
  --soft: #242424;
  --soft-2: #2a2a2a;
  --text: #e6e6e6;
  --strong: #f2f2f2;
  --heading: #f2f2f2;
  --muted: #a3a3a3;
  --border: #333333;
  --border-strong: #4a4a4a;
  --accent: #6aaed6;
  --accent-2: #8cc7ff;
  --warn: #ffdc49;
  --code: #e6e6e6;
  --code-bg: #2f3437;
  --tag-bg: #243831;
  --tag-text: #7ad9c5;
  --tag-border: #335f54;
  --blue-soft: #1f2b3f;
  --blue-text: #8cc7ff;
  --blue-border: #365f93;
  --warn-soft: #342f19;
  --warn-border: #5f4f18;
  --success-soft: #1f332b;
  --success-text: #8be6c1;
  --success-border: #2f6b57;
  --purple-soft: #2b2342;
  --purple-text: #c8b6ff;
  --purple-border: #574582;
  --risk-soft: #3a2028;
  --risk-text: #ff9ab3;
  --risk-border: #7a3a4d;
  --pre-bg: #111111;
  --pre-text: #d4d4d4;
  --focus: #6aaed6;
}
```

Regras:

- `body` usa `--page`, não branco.
- cards, tabelas, nodes, lanes e blocos estruturais usam `--surface`.
- chamadas e contexto de node usam `--soft` com borda esquerda semântica.
- `th` usa `--soft-2`; `td` usa `--surface`.
- inline `code` usa `--code-bg`; `pre` usa `--pre-bg`.
- foco de teclado usa outline visível com `--focus`.
- tags usam `--tag-*`.
- tags informativas podem usar `--blue-*`; tags de aviso usam `--warn-*`.
- sucesso usa `--success-*`; ênfase secundária usa `--purple-*`; risco usa `--risk-*`.
- avisos usam `--warn` e `--warn-soft`.
- links usam `--accent` e estado hover visível.
- visuais conceituais customizados, como `.flow-step`, `.state-card`, `.lane`,
  `.event-card`, `.stream-card`, `.part`, `.group-card`, `.tool-card`,
  `.handoff-card`, `.visual-card`, `.process-card` e classes equivalentes,
  usam superfícies escuras e apenas bordas/faixas semânticas para diferenciar
  estado.
- labels internas de mapas ou rotas, como `.route-label`, usam texto claro
  legível sobre superfície escura.

Falha quando uma página gerada usa superfícies claras legadas, como branco
para `body`, `td`, cards, visuais conceituais ou headers de tabela claros.

O `main` ou um contêiner estrutural de alto nível controla a largura útil da
página. Texto comum não deve criar uma coluna artificialmente menor dentro de
uma área larga.

## Primitiva Visual Correta

Use componentes HTML/CSS para visuais conceituais por padrão.

Exemplos que devem ser HTML/CSS, não `<pre>`:

- linha do tempo;
- fluxo simples;
- estados antes/depois;
- topologia simples;
- barras de atraso/progresso;
- lanes;
- comparação visual;
- mapa de fronteira;
- sequência de passos conceituais.

Use `<pre>` apenas para:

- código;
- configuração;
- arquivo estruturado;
- log ou saída textual;
- gramática;
- formato literal;
- diagrama ASCII cuja geometria seria substancialmente pior em HTML/CSS.

Quando usar ASCII como exceção, registre no dump e no audit visual:

- por que HTML/CSS seria pior;
- qual relação o ASCII revela;
- por que não é apenas atalho visual.

## Regra de Largura

Preferir:

```css
main {
  max-width: 1260px;
  margin: 0 auto;
  padding: 32px 28px 56px;
}

p,
ul,
ol,
.lead,
.callout {
  max-width: none;
}

table,
pre,
.content-grid,
.visual-block {
  width: 100%;
  max-width: 100%;
}
```

Use `body { font-size: 18px; }` como base tipográfica. Escale os tamanhos
explícitos do template proporcionalmente a partir da antiga base de `16px`,
mantendo `code { font-size: 0.92em; }` para que código inline acompanhe o texto
pai.

Se a leitura ficar larga demais, reduza `main`, não cada parágrafo isolado.

## Falhas Explícitas

Falha quando `main` está próximo de `1260px` e existe:

```css
p { max-width: 990px; }
.lead { max-width: 1035px; }
.callout { max-width: 1058px; }
```

sem justificativa visual explícita no asset e na auditoria.

## Componentes com Largura Própria

Cards, grids, diagramas, tabelas e blocos de código podem ter comportamento
próprio quando isso for parte estrutural do componente. A regra de largura de
texto não se aplica a parágrafos dentro de `.card`, células de tabela, tags,
snippets, diagramas ou colunas intencionais.

## Auditoria Visual

Registre nos audits:

```md
## Checks de largura de conteúdo

| Check | Status | Evidência |
|---|---|---|
| parágrafos comuns ocupam a largura útil | passa/falha | ... |
| callouts comuns ocupam a largura útil | passa/falha | ... |
| nenhuma coluna textual estreita sem motivo | passa/falha | ... |
```

Playwright deve medir desktop e mobile. Mobile não pode ter overflow horizontal
global; tabelas e blocos de código devem rolar internamente quando necessário.
