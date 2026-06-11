# Pipeline de Qualidade do HTML

Este pipeline valida e reescreve `node.html` depois da primeira geração do
capítulo. Ele é parte obrigatória da skill `roadmap/node-pages`.

## Regra Central

Qualidade tem prioridade absoluta sobre velocidade. Execute quantas rodadas
forem necessárias. Um HTML parcialmente bom continua inválido se falhar em
qualquer guardrail.

O pipeline é silencioso para a pessoa usuária. Não gere relatório, log,
checklist ou arquivo auxiliar fora de `.editorial/`. Guardrail existe para
corrigir o HTML antes da entrega e para manter a auditoria interna atualizada.

Scripts internos podem apoiar as etapas mecânicas: extração de texto visível,
busca literal de aliases bloqueados, validação estrutural e conferência dos
artefatos e renderização com Playwright. Eles não substituem os guardrails
semânticos nem o julgamento do agente sobre suficiência conceitual, suficiência
qualitativa de exemplos, apresentação visual renderizada, fronteira de escopo
ou narrativa.

## Entrada e Saída

Entrada:

- `research-dump.md` concluído;
- `.editorial/concept-ledger.md` concluído;
- `node.html` já gerado;
- `.editorial/pipeline/01-visible-text/visible-text.md`, `.editorial/pipeline/02-concept-introduction/concept-audit.md` e
  `.editorial/pipeline/03-example-sufficiency/example-audit.md` quando os guardrails visuais forem executados;
- contrato do node extraído do roadmap;
- matriz anti-repetição;
- artefatos do node anterior, quando existirem.

Saídas internas obrigatórias:

- `.editorial/pipeline/01-visible-text/visible-text.md`;
- `.editorial/pipeline/02-concept-introduction/concept-audit.md`;
- `.editorial/pipeline/02-concept-introduction/revision-plan.md`;
- `.editorial/pipeline/03-example-sufficiency/example-audit.md`;
- `.editorial/pipeline/03-example-sufficiency/revision-plan.md`;
- `.editorial/pipeline/04-visual-primitive-choice/primitive-audit.md`;
- `.editorial/pipeline/04-visual-primitive-choice/revision-plan.md`;
- `.editorial/pipeline/05-visual-render/visual-audit.md`;
- `.editorial/pipeline/05-visual-render/render-checks.json`;
- `.editorial/pipeline/05-visual-render/revision-plan.md`;
- `.editorial/pipeline/05-visual-render/playwright/desktop.png`;
- `.editorial/pipeline/05-visual-render/playwright/mobile.png`.

Saída final entregue:

- o mesmo `node.html`, reescrito até passar nos guardrails.

Não crie logs nem relatórios fora de `.editorial/`.

## Rodada Global

Execute, nesta ordem:

1. Atualizar `.editorial/pipeline/01-visible-text/visible-text.md` a partir de `node.html`, de
   preferência com:

   ```text
   docker/runtime/run python3 <skill-dir>/node-pages/scripts/extract_visible_text.py \
     --html <node-dir>/node.html \
     --out <node-dir>/.editorial/pipeline/01-visible-text/visible-text.md
   ```

2. Executar `02-visible-text-audit.md` para confirmar que a extração contém todo
   texto visível e semivisível relevante.
3. Executar a busca literal de termos bloqueados, quando disponível:

   ```text
   docker/runtime/run python3 <skill-dir>/node-pages/scripts/scan_blocked_terms.py \
     --ledger <node-dir>/.editorial/concept-ledger.md \
     --visible <node-dir>/.editorial/pipeline/01-visible-text/visible-text.md
   ```

   Trate a saída como lista de candidatos. Paráfrases não literais continuam
   sendo responsabilidade do agente.
4. Executar `01-concept-introduction.md` usando:
   - `node.html`;
   - `research-dump.md`;
   - `.editorial/concept-ledger.md`;
   - `.editorial/pipeline/01-visible-text/visible-text.md`.
5. Gravar ou atualizar `.editorial/pipeline/02-concept-introduction/concept-audit.md`.
   Grave também `.editorial/pipeline/02-concept-introduction/revision-plan.md`.
6. Executar `03-example-sufficiency.md` usando:
   - `node.html`;
   - `research-dump.md`;
   - `.editorial/concept-ledger.md`;
   - `.editorial/pipeline/01-visible-text/visible-text.md`;
   - `.editorial/pipeline/02-concept-introduction/concept-audit.md`.
7. Gravar ou atualizar `.editorial/pipeline/03-example-sufficiency/example-audit.md`.
   Grave também `.editorial/pipeline/03-example-sufficiency/revision-plan.md`.
8. Executar `04-visual-primitive-choice.md` usando:
   - `node.html`;
   - `research-dump.md`;
   - `.editorial/concept-ledger.md`;
   - `.editorial/pipeline/01-visible-text/visible-text.md`;
   - `.editorial/pipeline/02-concept-introduction/concept-audit.md`;
   - `.editorial/pipeline/03-example-sufficiency/example-audit.md`.
9. Falhar e revisar o HTML se visual conceitual simples estiver em `<pre>` sem
   exceção ASCII explícita e justificada.
   Grave `.editorial/pipeline/04-visual-primitive-choice/primitive-audit.md` e
   `.editorial/pipeline/04-visual-primitive-choice/revision-plan.md`.
10. Executar `05-visual-render-audit.md` usando os mesmos artefatos para
   preparar a auditoria renderizada.
11. Renderizar `node.html` com Playwright em desktop e mobile, de preferência
   com:

   ```text
   docker/runtime/run node <skill-dir>/node-pages/scripts/check_visual_render.mjs \
     --roadmap-dir <roadmap-dir> \
     --level <level> \
     --node <node-slug>
   ```

   O comando deve gravar evidências somente em
   `.editorial/pipeline/05-visual-render/playwright/` e
   `.editorial/pipeline/05-visual-render/render-checks.json`.
12. Inspecionar as screenshots geradas antes de marcar a rodada como aprovada.
13. Gravar ou atualizar `.editorial/pipeline/05-visual-render/visual-audit.md`.
14. Se houver falha em qualquer guardrail, gravar `revision-plan.md` no pipe
   responsável, revisar `node.html` e voltar ao passo 1.
15. Se não houver falha, `.editorial/pipeline/02-concept-introduction/concept-audit.md`,
   `.editorial/pipeline/03-example-sufficiency/example-audit.md`,
   `.editorial/pipeline/04-visual-primitive-choice/primitive-audit.md` e
   `.editorial/pipeline/05-visual-render/visual-audit.md` devem registrar
   status `passa`, e os `revision-plan.md` dos pipes `02`, `03`, `04` e `05`
   devem registrar que não há reescrita obrigatória.

A saída de um guardrail é a entrada do próximo. Se qualquer guardrail alterar o
HTML, reinicie a rodada global desde a extração de texto visível.

## Ordem dos Guardrails

Execute os guardrails nesta ordem:

1. `02-visible-text-audit.md`
2. `01-concept-introduction.md`
3. `03-example-sufficiency.md`
4. `04-visual-primitive-choice.md`
5. `05-visual-render-audit.md`

`02-visible-text-audit.md` roda antes porque valida a extração usada pelo
guardrail conceitual. O prefixo `02` foi mantido para preservar o contrato
recomendado do arquivo novo. `03-example-sufficiency.md` roda depois do
guardrail conceitual porque exemplos só podem usar conceitos já preparados no
dump e no ledger. `04-visual-primitive-choice.md` roda antes do Playwright
porque decide se o suporte concreto deveria ser HTML/CSS, tabela, snippet,
bloco literal ou ASCII excepcional. `05-visual-render-audit.md` roda por último
porque observa o HTML completo no navegador, depois que texto, conceitos,
exemplos e primitiva visual já foram consolidados.

Novos guardrails futuros devem ser adicionados com prefixo numérico:

```text
06-<categoria>.md
07-<categoria>.md
```

## Ponto Fixo

O pipeline deve operar até ponto fixo:

```text
rodada global:
  execute extract_visible_text.py
  execute 02-visible-text-audit.md
  execute scan_blocked_terms.py
  execute 01-concept-introduction.md
  execute 03-example-sufficiency.md
  execute 04-visual-primitive-choice.md
  execute 05-visual-render-audit.md
  atualize concept-audit.md
  atualize example-audit.md
  atualize primitive-audit.md
  atualize visual-audit.md
  atualize revision-plan.md do pipe aplicável

se qualquer guardrail reescreveu o HTML:
  volte à extração de visible-text.md

pare somente quando:
  uma rodada global completa passar sem reescritas obrigatórias
```

Ponto fixo só existe quando:

- `.editorial/pipeline/01-visible-text/visible-text.md` está atualizado com o HTML final;
- `.editorial/pipeline/02-concept-introduction/concept-audit.md` está atualizado com o `visible-text.md` final;
- `.editorial/pipeline/03-example-sufficiency/example-audit.md` está atualizado com o `visible-text.md` final;
- `.editorial/pipeline/04-visual-primitive-choice/primitive-audit.md` está atualizado com o HTML final;
- `.editorial/pipeline/05-visual-render/visual-audit.md` está atualizado com o HTML final;
- `.editorial/pipeline/05-visual-render/render-checks.json` registra `status` como `passa`;
- screenshots desktop e mobile foram geradas dentro de
  `.editorial/pipeline/05-visual-render/playwright/`;
- não há falha visual pendente;
- não há coluna textual estreita sem motivo em parágrafos comuns, `.lead` ou
  `.callout`;
- o agente inspecionou as screenshots;
- não há falha de primeira ocorrência;
- não há alias semântico vazando;
- não há termo de fonte vazando;
- não há conceito reservado a node futuro sustentando a explicação;
- não há trecho abstrato demais por falta de forma, estado, ordem, contraste,
  fronteira ou risco concreto;
- não há exemplo, snippet, tabela ou visual excessivo;
- o HTML final foi relido por completo depois da última auditoria.

## Quando Atualizar o Dump ou o Ledger

Se a correção do HTML exigir fato, limite, fonte, inferência, exemplo, suporte
concreto ou relação conceitual que não existe no `research-dump.md`, atualize o
dump antes de reescrever o HTML.

Se a correção envolver conceito, alias, termo reservado, fronteira ou título de
fonte que não existe em `.editorial/concept-ledger.md`, atualize o ledger antes
de revisar o HTML.

O pipeline não autoriza inventar conteúdo para melhorar a narrativa.

## Como Lidar com Bloqueios

Se um problema não puder ser corrigido sem quebrar o contrato do node, invadir
node futuro, ignorar fonte ou violar incrementalidade, aborte a geração e
explique o bloqueio de forma curta.

Fora desse caso, não reporte problemas internos: corrija.
