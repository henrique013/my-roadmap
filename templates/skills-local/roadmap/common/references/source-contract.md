# Contrato de Fontes

Use este contrato para manter rastreabilidade entre pesquisa, roadmap, contrato
JSON, dump e HTML.

## Campos Mínimos

```json
{
  "id": "F1",
  "url": "",
  "type": "",
  "reason": "",
  "supports_nodes": [],
  "limits": ""
}
```

## Regras

- `id` deve ser único dentro do artefato.
- `url` deve ser real, absoluta e clicável.
- `reason` deve dizer qual decisão, conceito ou fronteira a fonte sustenta.
- `limits` deve registrar versão, data, recorte ou insuficiência quando isso
  afetar a interpretação.
- Referências por node devem apontar para fontes que sustentam aquele node, não
  para uma bibliografia genérica.
- Texto visível de links em `node.html` também passa pelo guardrail de conceito
  antes do uso.

## Coerência Entre Modos

```text
roadmap-page
  |
  +-> consolida fontes no HTML
  +-> registra fontes no roadmap-contract.json
        |
        +-> node-pages usa essas fontes como ponto de partida
        +-> node-pages expande pesquisa sem invadir escopo futuro
```

O contrato JSON é artefato operacional em `.tmp/`; arquivos versionados não
devem depender de um JSON específico gerado ali.
