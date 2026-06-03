# Sistema Visual Compartilhado

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
  max-width: 1120px;
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

Se a leitura ficar larga demais, reduza `main`, não cada parágrafo isolado.

## Falhas Explícitas

Falha quando `main` está próximo de `1120px` ou `1180px` e existe:

```css
p { max-width: 880px; }
.lead { max-width: 920px; }
.callout { max-width: 940px; }
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
