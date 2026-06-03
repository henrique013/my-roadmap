# Guardrail 04 - Escolha da Primitiva Visual

Este guardrail audita se cada suporte concreto do `node.html` usa a primitiva
visual correta antes da renderização com Playwright.

## Regra Central

Visual conceitual usa HTML/CSS por padrão. `<pre>` representa texto literal,
não componente visual genérico.

Use componente HTML/CSS semântico para:

- linha do tempo;
- fluxo simples;
- topologia simples;
- estado antes/depois;
- contraste visual;
- barras de atraso ou progresso;
- lanes;
- mapa de fronteira;
- sequência de passos conceituais.

Use `<pre><code>` para código, configuração, arquivo estruturado, log, saída
textual, gramática ou formato literal.

## Entradas

- `node.html`;
- `research-dump.md`;
- `.editorial/concept-ledger.md`;
- `.editorial/pipeline/01-visible-text/visible-text.md`;
- `.editorial/pipeline/02-concept-introduction/concept-audit.md`;
- `.editorial/pipeline/03-example-sufficiency/example-audit.md`.

## Saídas

- `.editorial/pipeline/04-visual-primitive-choice/primitive-audit.md`;
- `.editorial/pipeline/04-visual-primitive-choice/revision-plan.md`.

## Como Auditar

Para cada suporte concreto no HTML:

1. Identifique o que ele mostra: forma, estado, ordem, fluxo, topologia,
   contraste, fronteira, risco, código, configuração, log ou formato literal.
2. Classifique a primitiva usada: componente HTML/CSS, tabela, snippet,
   bloco de código ou ASCII excepcional.
3. Compare com a obrigação registrada no dump.
4. Falhe se uma relação conceitual simples estiver em `<pre>` sem exceção
   explícita e justificada.

## Falhas

Falha quando:

- linha do tempo está em `<pre>`;
- fluxo simples está em `<pre>`;
- topologia simples está em `<pre>`;
- estado antes/depois está em `<pre>`;
- contraste visual está em `<pre>`;
- `<pre>` usa classe, `aria-label` ou texto associado com `diagram`,
  `diagrama`, `flow`, `fluxo`, `timeline`, `linha-do-tempo`, `topology`,
  `topologia`, `state`, `estado` ou `ascii` sem exceção justificada;
- o dump registra demanda de forma, estado, ordem, fluxo, topologia ou
  contraste, mas o HTML resolve com ASCII por conveniência;
- o `primitive-audit.md` omite a justificativa quando ASCII foi usado como
  exceção.

## Exceções

ASCII passa apenas quando todos os pontos forem verdadeiros:

- existe `data-ascii-exception="true"` no `<pre>`;
- existe `data-ascii-reason` não vazio;
- o dump registra por que HTML/CSS seria pior;
- o `primitive-audit.md` registra qual relação o ASCII revela e por que não é
  atalho.

Exceção ASCII é estreita. Ela não deve ser usada para economizar composição de
componentes simples.

## Contrato de `.editorial/pipeline/04-visual-primitive-choice/primitive-audit.md`

Registre:

```md
## Status geral

Status geral: passa/falha

## Checks

| Check | Status | Evidência |
|---|---|---|
| primitiva visual adequada ao conceito | passa/falha | ... |
| exceções ASCII justificadas | passa/falha | ... |
| nenhum `<pre>` usado como atalho visual | passa/falha | ... |
```

Se houver reescrita obrigatória, registre o plano em
`.editorial/pipeline/04-visual-primitive-choice/revision-plan.md`. Se não houver,
o arquivo deve registrar que nenhuma reescrita é obrigatória.

## Espelho no Audit Visual

Quando atualizar `.editorial/pipeline/05-visual-render/visual-audit.md`, inclua este check:

```md
| visuais conceituais não usam `<pre>` como atalho | passa/falha | ... |
```

Se houver ASCII excepcional, registre também:

```md
## Exceções ASCII

| Bloco | Motivo | Por que HTML/CSS seria pior | Status |
|---|---|---|---|
| ... | ... | ... | passa/falha |
```
