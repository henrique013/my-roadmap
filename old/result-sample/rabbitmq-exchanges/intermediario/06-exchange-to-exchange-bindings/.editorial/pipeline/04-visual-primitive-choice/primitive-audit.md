# Visual primitive choice audit

Status: passa

## Primitivas escolhidas

| Relação | Primitiva | Status | Motivo |
|---|---|---|---|
| Forma de `exchange.bind` | `<pre><code>` | passa | O conteúdo é forma literal de configuração conceitual, não fluxo visual. |
| Source exchange ligada a destination exchanges | Componente HTML/CSS `topology-map` | passa | A relação é espacial e topológica, melhor como mapa de partes. |
| E2E vs republicação por aplicação | Tabela | passa | O contraste já foi preparado em prosa e a tabela consolida responsabilidades. |
| Roteamento transitivo, convergência e ciclo | Componente HTML/CSS `state-grid` | passa | A relação depende de estado e consequência, não de texto literal. |
| Leitura de sinais de métrica | Componente HTML/CSS `signal-grid` | passa | Os cards separam onde a publicação começa, onde a destination participa e onde a entrega final aparece. |

## ASCII

Não há ASCII excepcional. Nenhum fluxo, topologia simples, estado ou fronteira foi colocado em `<pre>` como atalho.

## Snippets

O único bloco literal tem highlight semântico manual com `syntax-key`, `syntax-op`, `syntax-value` e `syntax-comment`. `pre code` não herda chip de inline `code`.

## Decisão

Não há reescrita obrigatória por escolha de primitiva visual.
