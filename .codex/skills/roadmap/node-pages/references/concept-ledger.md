# Contrato de `.editorial/concept-ledger.md`

`concept-ledger.md` é o arquivo principal de conceitos do bastidor editorial.
Ele deve ser criado depois de `research-dump.md` e antes de `node.html` final.

O ledger lista conceitos, aliases, paráfrases, termos reservados, fronteiras e
locais em que cada termo pode aparecer. Ele deve capturar equivalências
semânticas, não apenas grafias exatas.

## Estrutura Obrigatória

Use esta estrutura como contrato mínimo:

```md
# Concept ledger

## Metadados

- Roadmap:
- Level:
- Node:
- Node ID:
- Data:
- Fonte principal:

## Conceitos Permitidos no HTML

### <conceito canônico>

- Tipo: sigla | termo | papel | estado | parâmetro | arquivo | função | mecanismo | fonte | outro
- Pode aparecer no HTML: sim
- Pode aparecer antes de nomear: não | sim, como linguagem comum
- Primeira ocorrência permitida:
- Explicação mínima exigida antes da primeira ocorrência:
- Aliases e paráfrases:
  - ...
- Termos relacionados que também exigem preparo:
  - ...
- Pode aparecer em:
  - título: sim/não
  - lead: sim/não
  - corpo: sim/não
  - tabela: sim/não
  - visual/aria-label: sim/não
  - referências: sim/não
  - comentário final: sim/não
- Usos permitidos:
  - ...
- Usos proibidos:
  - ...
- Fronteira com nodes futuros:
- Fonte base:

## Conceitos Permitidos Só no Dump

### <conceito>

- Motivo:
- Por que não deve aparecer no HTML:
- Aliases bloqueados no HTML:
  - ...
- Fonte base:

## Conceitos Reservados a Nodes Futuros

### <conceito>

- Node responsável:
- Node ID responsável, quando existir:
- Menção permitida no HTML atual: nenhuma | curta como fronteira | handoff final
- Aliases bloqueados:
  - ...
- Condição de exceção:

## Títulos de Fontes e Termos de Referência

| Fonte | Termos carregados pelo título | Pode aparecer visível? | Forma visível recomendada |
|---|---|---|---|
```

## Regra de Aliases

Aliases e paráfrases listados no ledger contam como ocorrência do conceito.
Não basta procurar a palavra canônica.

Exemplo normativo:

```md
### PITR

- Pode aparecer no HTML: não, salvo se o conceito for preparado e fizer parte do escopo.
- Aliases e paráfrases:
  - PITR
  - point-in-time recovery
  - recuperação em ponto no tempo
  - recuperação para um ponto no tempo
  - recuperação até um ponto escolhido
  - voltar para um ponto anterior
- Uso permitido no node: apenas se a página introduzir antes a necessidade de reconstruir estado histórico e se isso não invadir node futuro.
- Uso recomendado neste node: preferir deixar no dump ou mencionar backup de forma simples, sem abrir PITR.
```

Esse exemplo mostra rigor esperado; não copie cegamente para todos os nodes.

## Atualização do Ledger

Atualize o ledger quando:

- o HTML precisar de conceito ainda ausente;
- a auditoria encontrar alias ou paráfrase não previsto;
- uma fonte visível trouxer termo técnico pelo título;
- uma revisão mudar a fronteira entre HTML, dump e node futuro.

Se a atualização exigir fato ou fonte que não está no dump, atualize
`research-dump.md` antes.
