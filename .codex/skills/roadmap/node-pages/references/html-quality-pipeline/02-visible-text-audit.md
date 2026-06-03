# Guardrail 02 - Auditoria de Texto Visível

Este guardrail garante que `.editorial/visible-text.md` contenha todo texto que
o leitor ou a auditoria conceitual precisa considerar.

## Regra Central

Não audite apenas parágrafos. Todo texto visível ou semivisível do HTML pode
introduzir conceito cedo demais.

## Arquivo de Saída

Gere ou atualize:

```text
.editorial/visible-text.md
```

Quando disponível, gere a extração com:

```text
python3 templates/skills-local/roadmap/node-pages/scripts/extract_visible_text.py \
  --html <node-dir>/node.html \
  --out <node-dir>/.editorial/visible-text.md
```

Depois, confira se a extração contém todos os blocos relevantes. A automação
não elimina a conferência do agente.

Estrutura mínima:

```md
# Visible text extraction

## Ordem de aparição

| Ordem | Local | Texto |
|---:|---|---|
| 1 | title | ... |
| 2 | h1 | ... |
| 3 | lead | ... |
```

## O Que Extrair

Inclua, em ordem de aparição:

- `<title>`;
- H1, H2, H3 etc.;
- lead;
- parágrafos;
- callouts;
- cards;
- tabelas;
- legendas;
- labels de diagramas;
- `aria-label`;
- texto alternativo, quando houver;
- textos de links;
- referências finais;
- comentários finais exigidos pela skill, quando carregarem termos técnicos.

## Conferência Obrigatória

O guardrail passa somente quando:

- todo heading do HTML aparece em `visible-text.md`;
- todo texto de link aparece em `visible-text.md`;
- todo texto de tabela aparece em `visible-text.md`;
- todo `aria-label` aparece em `visible-text.md`;
- todo texto alternativo relevante aparece em `visible-text.md`;
- todo comentário final exigido pela skill aparece em `visible-text.md`;
- nenhum bloco importante do HTML foi omitido;
- a ordem de aparição preserva a sequência do leitor.

Se qualquer item faltar, atualize `visible-text.md` antes de executar o
guardrail de introdução conceitual.

Se `node.html` for reescrito, regenere `visible-text.md` antes de auditar
conceitos novamente.
