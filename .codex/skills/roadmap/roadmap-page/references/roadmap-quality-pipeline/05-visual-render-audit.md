# Guardrail 05 - Auditoria Visual Renderizada

Renderize `roadmap.html` antes da resposta final.

## Checks Obrigatórios

- desktop e mobile renderizam;
- screenshots ficam em `.roadmap/playwright/`;
- não há overflow horizontal global;
- texto comum usa a largura útil;
- `.lead` não fica como coluna curta perdida;
- `.callout` usa a largura disponível;
- tabelas e blocos de código controlam overflow internamente;
- mapas, fluxos, sequências e timelines conceituais não usam `<pre>` como
  atalho visual;
- assets externos inesperados são bloqueados ou removidos;
- contraste e legibilidade são suficientes.

Use:

```text
npm run roadmap:roadmap-visual-check -- \
  --html <roadmap-dir>/roadmap.html
```

Registre no audit visual:

```md
## Checks de largura de conteúdo

| Check | Status | Evidência |
|---|---|---|
| parágrafos comuns ocupam a largura útil | passa/falha | ... |
| callouts comuns ocupam a largura útil | passa/falha | ... |
| nenhuma coluna textual estreita sem motivo | passa/falha | ... |
```

Registre também:

```md
| visuais conceituais não usam `<pre>` como atalho | passa/falha | ... |
```
