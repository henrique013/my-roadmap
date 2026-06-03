# Qualidade Compartilhada

Esta referência vale para `roadmap-page` e `node-pages`.

## Regra Central

Qualidade tem prioridade sobre velocidade. Gere, valide, corrija e repita até
que a última versão dos artefatos seja a versão validada.

## Responsabilidade do Agente e dos Scripts

| Responsabilidade | Dono |
|---|---|
| interpretar pedido, escopo, ambiguidade e fronteira | agente |
| escolher fontes, narrativa e progressão conceitual | agente |
| validar presença de arquivos, shape HTML, JSON e largura mecânica | scripts |
| renderizar, gerar screenshots e medir overflow | scripts |
| decidir suficiência conceitual, visual e didática | agente |

Scripts não autorizam escopo, não inventam fonte e não substituem inspeção
visual.

## Ponto Fixo

Use esta noção em qualquer modo:

```text
gerar artefatos
  |
  +-> validar texto, estrutura, fontes, contrato e visual
        |
        +-> se corrigiu HTML, JSON, dump ou CSS:
        |     voltar ao começo da rodada
        |
        +-> se nada exige correção:
              entregar resposta curta
```

Ponto fixo só existe quando a rodada completa termina sem reescrita obrigatória
e os artefatos internos correspondem à versão final.
