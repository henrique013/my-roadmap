# Visual primitive choice audit

Status: passa

## Primitivas escolhidas

| Relação | Primitiva | Status | Motivo |
|---|---|---|---|
| Declaração hardcoded vs policy por grupo | Componente HTML/CSS `flow-steps` | passa | Mostra transição de autoridade sem usar ASCII como atalho. |
| Camadas de autoridade e precedência | Componente HTML/CSS `authority-map` | passa | A relação é espacial e hierárquica, melhor como cards conectados por leitura. |
| Permissões por ação | Tabela | passa | A relação é mapeamento papel -> ação -> recurso -> permissão. |
| Vhost como fronteira | Componente HTML/CSS `boundary-map` | passa | Mostra dois espaços lógicos com nomes semelhantes e autoridades diferentes. |
| Configuração mínima | `<pre><code>` | passa | O conteúdo é forma literal de configuração conceitual, não fluxo visual. |

## ASCII

Não há ASCII excepcional. Nenhum fluxo, topologia simples, estado ou fronteira foi colocado em `<pre>` como atalho.

## Snippets

O único bloco literal tem highlight semântico manual com `syntax-key`, `syntax-op`, `syntax-value` e `syntax-comment`. `pre code` não herda chip de inline `code`.

## Decisão

Não há reescrita obrigatória por escolha de primitiva visual.
