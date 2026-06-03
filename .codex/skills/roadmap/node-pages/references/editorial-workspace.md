# Bastidor Editorial `.editorial/`

`.editorial/` é a mesa de edição interna de um node. Ela dá memória operacional
ao agente e torna a validação de conceitos repetível.

## Propósito

Use `.editorial/` para registrar:

- quais conceitos podem aparecer;
- quais aliases e paráfrases contam como o mesmo conceito;
- onde o texto do HTML usa esses conceitos;
- quais ocorrências passam ou falham;
- onde a prosa precisa ou não de suporte concreto;
- como os exemplos e snippets renderizam no navegador;
- que revisão precisa acontecer antes de finalizar `node.html`.

`.editorial/` não é conteúdo para a pessoa estudante.

## Local e Segurança

Crie ou recrie `.editorial/` somente dentro da pasta do node atual:

```text
.tmp/roadmaps/<roadmap-slug>/<node-slug>/.editorial/
```

Antes de apagar ou recriar, valide:

- o caminho resolvido está dentro da pasta do node atual;
- o slug do node segue `NN-slug`;
- o slug não contém `..`;
- o alvo não é a pasta do roadmap inteira;
- o alvo não é outro node.

Não crie logs fora de `.editorial/`. Não faça `node.html` depender de arquivos
editoriais. Evidências temporárias do Playwright devem ficar somente dentro de
`.editorial/playwright/`.

## Estrutura Obrigatória

```text
.editorial/
├── concept-ledger.md
├── visible-text.md
├── concept-audit.md
├── example-audit.md
├── visual-audit.md
├── playwright/
│   ├── desktop.png
│   ├── mobile.png
│   └── render-checks.json
└── revision-plan.md
```

`render-checks.json` é auxiliar e pode existir quando o guardrail visual precisar
registrar estilos computados, contraste, overflow ou falhas mecânicas.

## Sequência Obrigatória

Execute nesta ordem:

1. Gere `research-dump.md`.
2. Gere `.editorial/concept-ledger.md` a partir do dump e do contrato do node.
3. Gere a primeira versão de `node.html`.
4. Extraia texto visível e semivisível para `.editorial/visible-text.md`, de
   preferência com `scripts/extract_visible_text.py`.
5. Compare `visible-text.md` contra `concept-ledger.md`.
6. Use `scripts/scan_blocked_terms.py` para procurar aliases bloqueados
   literais como candidatos de revisão.
7. Grave `.editorial/concept-audit.md`.
8. Audite suficiência qualitativa de exemplos, snippets, tabelas e visuais.
9. Grave `.editorial/example-audit.md`.
10. Renderize `node.html` com Playwright em desktop e mobile, usando Chromium
    headless quando viável.
11. Grave evidências somente em `.editorial/playwright/`.
12. Grave `.editorial/visual-audit.md`.
13. Inspecione as screenshots antes de marcar passagem visual.
14. Grave `.editorial/revision-plan.md`.
15. Revise `node.html` ou o CSS embutido quando houver falha.
16. Repita extração, auditoria, renderização, plano e revisão até ponto fixo.

Ponto fixo significa que uma rodada completa de extração, auditoria textual,
auditoria de exemplos, renderização visual e revisão termina sem exigência de
alteração em `node.html`.

Ponto fixo visual só existe quando:

- `.editorial/visual-audit.md` está atualizado com o HTML final;
- screenshots desktop e mobile existem em `.editorial/playwright/`;
- não há falha visual pendente;
- `pre code` não herda chip de inline `code`;
- snippets técnicos têm highlight semântico ou justificativa registrada;
- o agente inspecionou as screenshots.

Os scripts internos executam apenas etapas mecânicas e determinísticas. Eles
não decidem suficiência de explicação, paráfrases semânticas, fronteira com
nodes futuros, necessidade de exemplo, excesso de exemplo, gosto visual amplo
nem revisão narrativa.

## Resposta Final

Não mencione `.editorial/` na resposta final. A resposta continua curta:

```text
.tmp/roadmaps/<roadmap-slug>/<node-slug>/research-dump.md
.tmp/roadmaps/<roadmap-slug>/<node-slug>/node.html
Pesquisa profunda usada; referências estão no dump e no HTML.
```
