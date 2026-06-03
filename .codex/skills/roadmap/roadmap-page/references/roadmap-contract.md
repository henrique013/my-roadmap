# Contrato de `.roadmap/roadmap-contract.json`

O contrato JSON é a fonte mecânica para o modo `node-pages`. O HTML continua
sendo a página humana; o JSON guarda estrutura verificável.

## Esquema Lógico Mínimo

```json
{
  "schema_version": "1.0",
  "roadmap_slug": "replicacao-postgres",
  "theme": "",
  "background": "",
  "research_date": "",
  "assumptions": [],
  "limits": [],
  "expected_understanding": "",
  "sources": [
    {
      "id": "F1",
      "url": "",
      "type": "",
      "reason": "",
      "supports_nodes": [],
      "limits": ""
    }
  ],
  "anti_repetition": [
    {
      "concept": "",
      "first_introduction_node": "",
      "allowed_reuses": [],
      "blocked_reuses": [],
      "boundary_reason": ""
    }
  ],
  "nodes": [
    {
      "order": 1,
      "slug": "01-exemplo",
      "label": "",
      "role_in_chain": "",
      "inherited_prerequisites": [],
      "first_introduces": [],
      "must_cover": [],
      "must_not_cover": [],
      "questions": [],
      "conceptual_vocabulary": [],
      "allowed_examples_or_diagrams": [],
      "pitfalls": [],
      "mastery_criterion": "",
      "handoff_to_next": "",
      "references": [
        {
          "source_id": "F1",
          "url": "",
          "reason": ""
        }
      ]
    }
  ]
}
```

## Regras

- `schema_version` começa em `1.0`.
- `roadmap_slug` deve ser igual ao slug da pasta em `.tmp/roadmaps/<slug>/`.
- Cada node deve ter `order` compatível com o prefixo numérico do slug.
- `slug` deve seguir `NN-slug`.
- `must_cover` precisa ser denso e útil para documentação futura.
- `must_not_cover` deve proteger anti-repetição, conteúdo futuro e prática
  proibida.
- `references` de cada node devem apontar para fontes reais do bloco `sources`.
- `anti_repetition` deve ter fronteiras reais, não apenas lista decorativa.

## Uso por `node-pages`

```text
identificar roadmap
  |
  +-> se roadmap-contract.json existir:
  |     usar JSON como contrato principal
  |     conferir coerência básica com roadmap.html
  |
  +-> se JSON não existir:
        usar roadmap.html como fallback legado
        registrar compatibilidade no research-dump.md
```

O fallback preserva compatibilidade; ele não justifica deixar `roadmap-page` sem
contrato estruturado.
