# Guardrail 03 - Suficiência Qualitativa de Exemplos

Este guardrail valida se o HTML tem suporte concreto suficiente para trechos
que dependem de forma, estado, ordem, contraste ou fronteira, sem transformar a
página em laboratório ou coleção de exemplos.

## Regra Central

Exemplo é obrigatório apenas quando reduz ambiguidade essencial. Excesso de
exemplo também é falha.

O guardrail não pergunta se todo trecho tem exemplo. Ele pergunta:

```text
Há algum trecho em que a falta de exemplo impede entender a forma, o estado, a
ordem, o contraste ou a fronteira do conceito?
```

Se a resposta for não, o bloco passa só com prosa. Se a resposta for sim, exija
o menor suporte concreto capaz de resolver a ambiguidade.

## Entradas

- `node.html`;
- `research-dump.md`;
- `.editorial/concept-ledger.md`;
- `.editorial/visible-text.md`;
- `.editorial/concept-audit.md`.

## Saídas

- `.editorial/example-audit.md`;
- `.editorial/revision-plan.md`, quando houver reescrita obrigatória.

## Como Auditar

Audite por blocos de seção, não apenas pela página inteira. Para cada bloco,
registre internamente:

```text
Bloco:
- seção:
- ordem:
- texto:
- termos técnicos usados:
- arquivos citados:
- parâmetros citados:
- fala de sintaxe/regra/formato?
- fala de processo/ordem?
- fala de risco/trade-off?
- existe exemplo concreto próximo?
- existe tabela/visual/snippet associado?
- suficiência: passa | abstrato-demais | exemplo-ausente | exemplo-fraco | exemplo-excessivo | exemplo-fora-de-escopo
- ação:
```

Procure sinais de demanda concreta:

- arquivo de configuração;
- regra, linha, campo, valor ou formato;
- API, comando, schema ou protocolo;
- processo temporal;
- estado antes/depois;
- risco operacional;
- contraste seguro/perigoso;
- três ou mais peças técnicas relacionadas.

Se a prosa bastar, registre `passa`. Se a falta de suporte concreto prejudicar
a compreensão, registre falha e exija o menor suporte suficiente:

- snippet curto;
- tabela curta;
- mini-diagrama;
- miniestado;
- contraste seguro/perigoso.

## Quando a Prosa Basta

Um bloco pode passar só com prosa quando:

- expressa relação causal simples;
- retoma pré-requisito herdado;
- interpreta um exemplo já dado;
- não fala de sintaxe, regra, formato, campo, comando, API, schema ou arquivo;
- não depende de posição, ordem, estado ou estrutura visível;
- não compara "amplo demais" versus "estreito demais" sem consequência
  prática;
- não introduz três ou mais peças técnicas novas relacionadas no mesmo trecho;
- o leitor consegue parafrasear a ideia sem precisar ver forma concreta.

## Quando o Exemplo é Obrigatório

Um bloco falha por `abstrato-demais` ou `exemplo-ausente` quando:

- fala de arquivo de configuração;
- fala de regra, linha, campo, valor, formato, schema, API ou comando;
- a compreensão depende da posição dos elementos;
- usa termos como `campo`, `database`, `origem`, `método`, `linha`,
  `formato`, `valor` ou `regra` sem mostrar a forma;
- fala de risco "amplo demais" ou "estreito demais" sem mostrar contraste;
- apresenta três ou mais peças técnicas relacionadas e nenhuma decomposição;
- fala de estado antes/depois sem mostrar estado;
- fala de processo temporal sem mostrar ordem;
- fala de trade-off sem mostrar os lados.

## Bloqueio por Excesso

Falha também quando o exemplo:

- vira sequência executável;
- domina a seção;
- repete a prosa sem acrescentar forma, estado, ordem ou contraste;
- introduz conceito fora do dump ou do ledger;
- invade node futuro;
- usa dados reais ou específicos demais sem necessidade;
- inclui múltiplos snippets quando um basta;
- substitui a explicação em vez de complementá-la.

Regra curta:

```text
O exemplo deve ser menor que a explicação que ele esclarece.
```

## Matriz de Suporte Mínimo

Use esta matriz como guia qualitativo. Ela não é checklist obrigatório por
quantidade.

| Tipo de trecho | Suporte mínimo recomendado |
|---|---|
| Arquivo de configuração | snippet mínimo + leitura campo a campo |
| Regra ou linha estruturada | snippet mínimo + decomposição |
| Parâmetro isolado | exemplo de valor somente se o valor muda o sentido |
| Vários parâmetros juntos | tabela função/risco |
| Processo temporal | fluxo curto ou linha do tempo |
| Estado antes/depois | miniestado ou comparação curta |
| Risco operacional | contraste seguro/perigoso |
| Sintaxe/API/comando | trecho mínimo, sem roteiro |
| Conceito causal simples | prosa pode bastar |
| Recapitulação de conceito anterior | prosa curta basta |
| Visual já existente que resolve a forma | não adicionar outro exemplo |

## Proximidade do Suporte

O suporte concreto deve aparecer no mesmo bloco, logo depois do trecho abstrato,
ou logo antes quando ele prepara a leitura.

Uma tabela de fechamento no final da página não justifica falta de exemplo
local se o bloqueio acontece muito antes. Um visual genérico não justifica
falta de snippet para sintaxe específica.

## Contrato de `.editorial/example-audit.md`

Use esta estrutura:

```md
# Example sufficiency audit

## Metadados

- Roadmap:
- Node:
- Rodada:
- Data:
- HTML auditado:
- Visible text:
- Dump:
- Ledger:

## Status geral

Status geral: passa | falha

## Rubrica aplicada

- Exemplo obrigatório apenas quando reduz ambiguidade essencial.
- Excesso de exemplo também falha.
- Snippets, tabelas e visuais devem ser mínimos e dentro do escopo.

## Blocos auditados

| Ordem | Seção | Tipo de demanda | Suporte encontrado | Status | Ação |
|---:|---|---|---|---|---|

## Falhas

### <seção ou ordem>

- Problema:
- Por que a prosa não basta:
- Suporte mínimo exigido:
- Risco de excesso:
- Revisão obrigatória:

## Excesso detectado

### <seção ou ordem>

- Problema:
- Por que o exemplo/visual passa do ponto:
- Revisão obrigatória:

## Resultado da rodada

- HTML precisa reescrita: sim/não
- Se sim, atualizar `revision-plan.md` e reiniciar a rodada global após a reescrita.
```

Critério mecânico de passagem:

```text
Status geral: passa
```

Este arquivo é interno. Não mencione `.editorial/example-audit.md` na resposta
final da skill.

## Exemplo Normativo

### Falha

Trecho:

```text
A regra que junta essas peças fica em pg_hba.conf. Para uma conexão física de
replicação, o campo de database usa a palavra especial replication...
```

Classificação:

```text
Status: exemplo-ausente
Tipo de demanda: regra de arquivo de configuração
Motivo: a compreensão depende da forma e da posição dos campos.
```

Correção mínima:

```text
host    replication    replicator    10.0.0.20/32    scram-sha-256
```

Leitura:

| Campo | O que significa |
|---|---|
| `host` | conexão TCP/IP |
| `replication` | conexão física de replicação |
| `replicator` | role dedicada |
| `10.0.0.20/32` | origem permitida |
| `scram-sha-256` | método de autenticação |

Por que não vira laboratório:

- não há sequência de comandos;
- não há instrução para editar arquivo;
- os valores são placeholders;
- a finalidade é leitura da forma, não execução.

### Excesso

Falha por excesso:

```text
Adicionar três variantes de pg_hba.conf, sequência de reload, comando de criação
de role, teste de conexão e diagnóstico de erro.
```

Motivo:

- vira runbook;
- invade bootstrap, diagnóstico ou node futuro;
- muda o centro da página.

Correção:

- manter um snippet e uma leitura de campos;
- remover sequência operacional.

## Interação com o Guardrail de Conceitos

Este guardrail não substitui `01-concept-introduction.md`.

Antes de adicionar exemplo:

- confirme que os conceitos do suporte concreto existem no dump;
- confirme que o ledger permite esses termos no HTML;
- prepare conceitos antes do suporte concreto;
- se o suporte concreto precisar de termo novo, atualize primeiro o dump e o
  ledger.

Exemplos:

- Se o snippet usa `replicator`, trate como placeholder de role somente quando
  esse papel já estiver preparado.
- Se o snippet usa `.pgpass`, falhe quando senha no standby estiver reservada a
  node futuro.
- Se o snippet usa `primary_conninfo`, falhe quando configuração do standby
  estiver reservada a node futuro.

## Critério de Passagem

O HTML passa quando:

- todo trecho que precisa de forma concreta recebeu suporte mínimo;
- nenhum suporte concreto é excessivo;
- nenhum suporte concreto virou laboratório;
- nenhum suporte concreto introduz conceito não preparado;
- nenhum suporte concreto invade node futuro;
- `.editorial/example-audit.md` registra `Status geral: passa`;
- `.editorial/revision-plan.md` registra nenhuma reescrita obrigatória.

Se o HTML foi reescrito, retorne ao pipeline e reinicie a rodada global desde a
extração de `.editorial/visible-text.md`.
