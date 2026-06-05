# Contrato de `.roadmap/roadmap-contract.json`

O contrato JSON é a fonte mecânica para o modo `node-pages`. O HTML continua
sendo a página humana; o JSON guarda estrutura verificável.

O schema versionado fica em
`roadmap-page/schema/roadmap-contract.schema.json`. Ele valida presença, tipos,
versão e formato mínimo; regras de coerência entre HTML, ordem, slugs e
`source_id` continuam no validador Python.

## Esquema Lógico Mínimo

```json
{
  "schema_version": "2.0",
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
      "supports_nodes": [
        "basico/01-exemplo"
      ],
      "limits": ""
    }
  ],
  "anti_repetition": [
    {
      "concept": "",
      "first_introduction_node": "basico/01-exemplo",
      "allowed_reuses": [
        {
          "node_id": "intermediario/01-exemplo",
          "reuse": "",
          "reason": ""
        }
      ],
      "blocked_reuses": [
        {
          "node_id": "avancado/01-exemplo",
          "reason": ""
        }
      ],
      "boundary_reason": ""
    }
  ],
  "levels": [
    {
      "level": "basico",
      "label": "Básico",
      "semantics": "fundamentos, vocabulário indispensável e modelos mentais",
      "nodes": [
        {
          "node_id": "basico/01-exemplo",
          "level": "basico",
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
  ]
}
```

## Regras

- `schema_version` começa em `2.0` para roadmaps tri-level.
- `roadmap_slug` deve ser igual ao slug da pasta em `.tmp/roadmaps/<slug>/`.
- `background` é campo técnico opcional: preencha somente quando a pessoa
  fornecer contexto relevante; se não fornecer, use string vazia e registre
  premissas necessárias em `assumptions`.
- `levels` deve conter exatamente `basico`, `intermediario` e `avancado`.
- Cada nível pode ter no máximo 10 nodes; 10 é teto, não meta.
- Os níveis podem ter quantidades diferentes; a quantidade de nodes deve ser
  consequência da densidade do conteúdo, da curadoria semântica e da necessidade
  real de decomposição de cada nível, não de arbitragem estética, simetria
  artificial ou tentativa de balanceamento.
- Cada node deve ter `level`, `node_id`, `order`, `slug` e `label`.
- `node_id` deve seguir `<level>/<slug>` e ser único no contrato inteiro.
- `order` deve ser local ao nível e compatível com o prefixo numérico do slug.
- `slug` deve seguir `NN-slug` e é local ao nível.
- `must_cover` precisa ser denso e útil para documentação futura.
- `must_not_cover` deve proteger anti-repetição, conteúdo futuro e prática
  proibida.
- `references` de cada node devem apontar para fontes reais do bloco `sources`.
- `supports_nodes` deve usar `node_id`, como `intermediario/07-rendering`.
- `anti_repetition` deve ter fronteiras reais, globais e level-aware, não
  apenas lista decorativa.
- `first_introduction_node`, `allowed_reuses[].node_id` e
  `blocked_reuses[].node_id` devem apontar para `node_id` existente quando
  fizerem referência a um node.

## Uso por `node-pages`

```text
identificar roadmap
  |
  +-> validar .roadmap/roadmap-contract.json contra o schema versionado
  |
  +-> resolver node por level + node-slug ou por node_id
  |
  +-> usar JSON como contrato principal
  |
  +-> conferir coerência básica com roadmap.html
```

Se `roadmap-contract.json` não existir ou estiver inválido, `node-pages` deve
bloquear e pedir a execução de `roadmap-page`.
