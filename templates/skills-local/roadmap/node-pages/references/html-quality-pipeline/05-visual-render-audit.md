# Guardrail 05 - Auditoria Visual Renderizada

Este guardrail valida `node.html` no navegador, com CSS aplicado, antes da
entrega. Ele fecha a lacuna entre HTML textualmente correto e página realmente
legível.

## Regra Central

Auditoria visual renderizada é obrigatória. Um HTML que passa em conceito,
texto visível e suficiência de exemplos ainda falha se a página renderizada
apresentar snippets quebrados, contraste ruim, overflow global, sobreposição
incoerente ou bloco de código visualmente confuso.

Use Playwright para validar invariantes mecânicas e gerar evidência visual.
Depois disso, o agente deve inspecionar as screenshots. O script não substitui
julgamento visual.

## Entradas

- `node.html`;
- `research-dump.md`;
- `.editorial/concept-ledger.md`;
- `.editorial/pipeline/01-visible-text/visible-text.md`;
- `.editorial/pipeline/02-concept-introduction/concept-audit.md`;
- `.editorial/pipeline/03-example-sufficiency/example-audit.md`;
- resultado do guardrail `04-visual-primitive-choice.md`.

## Saídas

- `.editorial/pipeline/05-visual-render/visual-audit.md`;
- `.editorial/pipeline/05-visual-render/render-checks.json`;
- `.editorial/pipeline/05-visual-render/revision-plan.md`;
- `.editorial/pipeline/05-visual-render/playwright/desktop.png`;
- `.editorial/pipeline/05-visual-render/playwright/mobile.png`.

Esses arquivos são internos. Não mencione `.editorial/pipeline/05-visual-render/visual-audit.md` nem
screenshots na resposta final da skill.

## Comando Preferencial

Use a interface pública da skill e rode o guardrail mecânico com:

```text
npm run roadmap:node-visual-check -- \
  --roadmap-dir <roadmap-dir> \
  --level <level> \
  --node <node-slug>
```

Também é aceita a forma direta quando o HTML já estiver identificado:

```text
npm run roadmap:node-visual-check -- \
  --html <node-dir>/node.html
```

## Contrato de `.editorial/pipeline/05-visual-render/playwright/`

Qualquer artefato auxiliar do Playwright deve ficar somente dentro de:

```text
.editorial/pipeline/05-visual-render/playwright/
```

Regras obrigatórias:

- criar ou recriar esse diretório apenas dentro da pasta do node atual;
- validar que o caminho resolvido está dentro de `.editorial/`;
- não usar `test-results/`, `playwright-report/`, trace, vídeo, snapshot ou
  screenshot fora de `.editorial/pipeline/05-visual-render/playwright/`;
- abrir `node.html` por `file://` quando isso bastar;
- bloquear ou registrar assets externos inesperados;
- não transformar screenshots em saída final para a pessoa usuária.

## Checks Obrigatórios

O guardrail falha quando:

- `pre code` herda fundo, borda, padding ou `border-radius` de inline `code`;
- inline `code` deixa de ser distinguível e legível fora de `pre`;
- snippet técnico de configuração, regra, parâmetro, campo, API, comando ou
  formato não tem highlight semântico mínimo;
- highlight vira ruído visual ou prejudica a leitura;
- texto normal, inline code ou bloco de código tem contraste inadequado;
- existe overflow horizontal global em desktop ou mobile;
- parágrafos comuns, listas comuns, `.lead` ou `.callout` ocupam menos de 90%
  da largura útil do `main` em desktop sem justificativa visual explícita;
- texto se sobrepõe a outro texto de forma incoerente;
- tabela, card, callout, exemplo ou bloco de código quebra a leitura mobile;
- as cores dos exemplos parecem acidentais, ilegíveis ou fora do padrão visual
  da página.

Para blocos ASCII excepcionais, a ausência de highlight só pode passar se o
bloco tiver
`data-ascii-exception="true"`, `data-ascii-reason` não vazio, justificativa no
`research-dump.md` e registro em `.editorial/pipeline/05-visual-render/visual-audit.md` explicando por
que HTML/CSS seria pior.

## Highlight Semântico

Snippet técnico deve usar marcação semântica mínima no próprio HTML quando não
houver biblioteca local de highlight. Prefira classes `syntax-*`:

```html
<pre class="code-block language-conf" aria-label="Recorte conceitual de configuração">
<code><span class="syntax-key">parametro_principal</span> <span class="syntax-op">=</span> <span class="syntax-value">valor_preparado</span>
<span class="syntax-key">limite_de_saida</span> <span class="syntax-op">=</span> <span class="syntax-value">&lt;placeholder_conceitual&gt;</span></code></pre>
```

Classes aceitáveis:

- `syntax-*`, preferencialmente no HTML gerado pela skill;
- `token*`, quando existir biblioteca local de highlight;
- `hljs-*`, quando existir biblioteca local de highlight.

Não dependa de CDN, JavaScript remoto ou asset externo para destacar snippets.

## Contrato de `.editorial/pipeline/05-visual-render/visual-audit.md`

Use esta estrutura:

```md
# Visual render audit

## Metadados

- Roadmap:
- Level:
- Node:
- Node ID:
- Rodada:
- Data:
- HTML auditado:
- Ferramenta:
- Browser:
- Viewports:

## Evidências

| Viewport | Screenshot | Observações |
|---|---|---|
| desktop | `.editorial/pipeline/05-visual-render/playwright/desktop.png` | ... |
| mobile | `.editorial/pipeline/05-visual-render/playwright/mobile.png` | ... |

## Status geral

Status geral: passa | falha

## Checks mecânicos

| Check | Status | Evidência |
|---|---|---|
| `pre code` não herda chip de inline code | passa/falha | ... |
| snippets técnicos têm highlight semântico | passa/falha | ... |
| visuais conceituais não usam `<pre>` como atalho | passa/falha | ... |
| contraste mínimo em texto e código | passa/falha | ... |
| página sem overflow horizontal global | passa/falha | ... |
| texto comum ocupa largura útil | passa/falha | ... |
| mobile legível sem sobreposição óbvia | passa/falha | ... |

## Checks de largura de conteúdo

| Check | Status | Evidência |
|---|---|---|
| parágrafos comuns ocupam a largura útil | passa/falha | ... |
| callouts comuns ocupam a largura útil | passa/falha | ... |
| nenhuma coluna textual estreita sem motivo | passa/falha | ... |

## Inspeção visual do agente

- Cores dos exemplos:
- Leitura dos snippets:
- Hierarquia visual:
- Problemas observados:

## Falhas

### <falha>

- Onde apareceu:
- Por que falha:
- Revisão obrigatória:

## Resultado da rodada

- HTML precisa reescrita: sim/não
- Se sim, atualizar `.editorial/pipeline/05-visual-render/revision-plan.md` e reiniciar a rodada global depois da reescrita.
```

Critério mecânico de passagem:

```text
Status geral: passa
```

## Como Auditar

1. Rode o guardrail Playwright e gere screenshots desktop e mobile.
2. Abra ou inspecione as screenshots antes de marcar passagem da rodada.
3. Leia `.editorial/pipeline/05-visual-render/render-checks.json` quando houver falha
   mecânica ou dúvida de contraste, overflow ou estilo computado.
4. Atualize `.editorial/pipeline/05-visual-render/visual-audit.md` com a inspeção visual do agente.
5. Se houver falha visual, registre a revisão em `.editorial/pipeline/05-visual-render/revision-plan.md`,
   reescreva `node.html` ou o CSS embutido e reinicie a rodada global desde a
   extração de texto visível.

Se a correção visual alterar HTML ou CSS embutido, os guardrails anteriores
devem rodar novamente porque a mudança pode alterar texto visível, ordem,
estrutura, overflow, legibilidade ou exemplos.
