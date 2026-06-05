# Guardrail 01 - Introdução Conceitual

Este guardrail valida e corrige conceitos usados antes de serem preparados no
`node.html`. Ele compara o texto extraído do HTML contra
`.editorial/concept-ledger.md` e grava o resultado em
`.editorial/pipeline/02-concept-introduction/concept-audit.md`.

## Regra Central

Não use um termo técnico antes de construir a necessidade dele.

A ordem segura é:

```text
necessidade do leitor
  -> explicação em linguagem comum
    -> nome técnico
      -> uso posterior do termo
```

O HTML falha neste guardrail quando um termo, papel, sigla, parâmetro, arquivo,
função, estado, mecanismo, abstração, visual, alias, paráfrase ou referência
aparece antes de o leitor receber a ideia mínima necessária para entendê-lo.

Não basta remover a palavra literal. Se uma ideia equivalente continua
aparecendo cedo demais por alias ou paráfrase, o vazamento permanece.

## Arquivos Obrigatórios

Use como entrada:

- `node.html`;
- `research-dump.md`;
- `.editorial/concept-ledger.md`;
- `.editorial/pipeline/01-visible-text/visible-text.md`.

Quando disponível, rode o scanner literal de termos bloqueados antes da revisão
semântica:

```text
python3 <skill-dir>/node-pages/scripts/scan_blocked_terms.py \
  --ledger <node-dir>/.editorial/concept-ledger.md \
  --visible <node-dir>/.editorial/pipeline/01-visible-text/visible-text.md
```

Trate a saída como lista de candidatos, não como decisão final. Paráfrases não
literais e suficiência de preparação continuam sendo decisão do agente.

Atualize como saída:

- `.editorial/pipeline/02-concept-introduction/concept-audit.md`;
- `.editorial/pipeline/02-concept-introduction/revision-plan.md`.

## O Que Verificar

Leia `.editorial/pipeline/01-visible-text/visible-text.md` e confirme contra o HTML inteiro, incluindo:

- `<title>`;
- H1;
- lead;
- subtítulos;
- parágrafos;
- callouts;
- cards;
- tabelas;
- legendas e textos de visuais;
- labels de diagramas;
- texto alternativo ou `aria-label`;
- textos de links;
- referências comentadas ao fim.

Não valide apenas o corpo em parágrafos. Conceitos usados em títulos, tabelas,
visuais e referências também precisam ser preparados.

Compare cada primeira ocorrência contra `.editorial/concept-ledger.md`:

- conceito canônico;
- aliases explícitos;
- paráfrases listadas;
- termos relacionados que exigem preparo;
- termos permitidos só no dump;
- conceitos reservados a nodes futuros;
- títulos de fontes e textos de links.

## Categorias de Problema

Classifique cada primeira ocorrência relevante como:

- `passa`: conceito preparado antes do uso e dentro do escopo;
- `fraco`: existe alguma preparação, mas ela é insuficiente;
- `falha`: termo, alias ou conceito apareceu cedo demais;
- `fora-do-escopo`: conceito pertence a outro node ou só ao dump;
- `fonte-vazou`: título de fonte, referência ou link introduziu conceito novo.

O HTML só passa quando não houver `falha`, `fora-do-escopo` ou `fonte-vazou` e
quando todo `fraco` tiver sido reescrito ou justificado por pré-requisito
herdado explícito do roadmap ou de node anterior.

Registre a rodada em `.editorial/pipeline/02-concept-introduction/concept-audit.md` com:

- status geral;
- primeiras ocorrências;
- vazamentos encontrados;
- termos de fonte e referência;
- conceitos reservados a nodes futuros.

## Termos Que Exigem Atenção

Procure especialmente:

- siglas;
- nomes de parâmetros;
- nomes de arquivos e diretórios;
- funções e views;
- papéis de arquitetura;
- estados de processo;
- nomes de mecanismos;
- nomes de protocolos;
- nomes de configuração;
- operações administrativas;
- termos de diagnóstico;
- termos reservados a nodes futuros;
- palavras aparentemente comuns que carregam sentido técnico no contexto.

Exemplos de palavras que podem ser comuns, mas carregam conceito técnico:

- `replay`;
- `flush`;
- `recovery`;
- `standby`;
- `primário`;
- `cluster`;
- `commit`;
- `PITR`;
- `logical`;
- `streaming`;
- `observabilidade`;
- `métrica`;
- `view`;
- `slot`;
- `promoção`;
- `failover`.

Esta lista é exemplo, não limite.

Procure também aliases e paráfrases do ledger. Exemplo: se o ledger bloqueia
`PITR`, então `point-in-time recovery`, `recuperação em ponto no tempo`,
`recuperação para um ponto no tempo`, `recuperação até um ponto escolhido` e
formas equivalentes também devem ser tratadas como o mesmo conceito.

## Relação com o Roadmap

Use o contrato do node para distinguir:

- conceitos que o leitor já pode conhecer por pré-requisito herdado;
- conceitos introduzidos pela primeira vez neste node;
- conceitos reservados a nodes futuros;
- conceitos do node anterior que podem ser usados como base;
- conceitos que devem ser apenas mencionados como fronteira.

Se o roadmap reserva um conceito para node futuro, o HTML atual não deve usar
esse conceito como alicerce explicativo. Se for inevitável mencioná-lo, a
menção deve ser curta, preparada e marcada como fronteira, sem depender dele
para ensinar o node atual.

Use o ledger para diferenciar:

- `Pode aparecer no HTML: sim`;
- `Pode aparecer no HTML: não`;
- conceitos permitidos só no dump;
- conceitos reservados a nodes futuros;
- lugares permitidos de aparição, como título, lead, tabela, visual,
  `aria-label`, referências ou comentário final.

## Referências e Títulos de Fonte

Texto de referência também precisa respeitar conceito antes do uso.

Se uma fonte oficial tem título com conceito não preparado:

- adapte o texto visível do link para uma forma já preparada;
- prepare o conceito antes da referência;
- ou deixe a fonte apenas no `research-dump.md` se ela não precisa aparecer no
  HTML visível.

Uma referência final falha quando introduz termo técnico novo, alias bloqueado
ou conceito reservado a node futuro.

## Como Corrigir

Para cada problema encontrado, reescreva o HTML. Não liste o erro para o
usuário.

Formas válidas de correção:

- mover o termo para depois da explicação;
- substituir o termo por linguagem comum até ele poder ser nomeado;
- inserir uma frase de necessidade antes da nomeação;
- trocar título, label, legenda ou card que usa conceito cedo demais;
- remover termo de node futuro quando ele não for necessário;
- remover alias ou paráfrase que vaza conceito bloqueado;
- mover fonte para o dump quando o título da referência carrega conceito fora
  de escopo;
- dividir um parágrafo que despeja vários conceitos ao mesmo tempo;
- transformar uma lista ou tabela inicial em prosa progressiva;
- atualizar o dump ou o ledger antes, se a correção exigir fato, relação,
  conceito, alias ou fronteira ainda ausente.

Forma ruim:

```text
O standby recebe WAL do primário por streaming replication.
```

Forma melhor:

```text
Depois que uma mudança entra na trilha ordenada do banco que aceita escrita,
outro servidor pode acompanhar essa trilha para chegar ao mesmo estado. Nesse
papel, ele não recebe o SQL original; recebe os registros que descrevem as
mudanças. Mais adiante, esse segundo servidor será chamado de standby.
```

Forma ruim:

```text
O replay pode ficar atrás do recebimento.
```

Forma melhor:

```text
Chegar ao segundo servidor não basta. A mudança ainda precisa ser aplicada ao
estado que esse servidor está reconstruindo. A aplicação ordenada desses
registros é chamada de replay.
```

Falha por paráfrase:

```text
O ledger marca `PITR` e seus aliases como não permitidos no HTML deste node. O
HTML não contém `PITR`, mas contém "recuperação para um ponto no tempo". Isso
continua sendo falha, porque o conceito vazou por paráfrase.
```

Correções válidas:

- remover a menção do HTML;
- preparar o conceito antes e confirmar que ele pertence ao escopo do node;
- mover a fonte ou o termo para o dump se a menção só sustenta limite factual.

## Plano de Revisão

Quando houver qualquer `falha`, `fora-do-escopo`, `fonte-vazou` ou `fraco` não
justificado, grave `.editorial/pipeline/02-concept-introduction/revision-plan.md` com:

- rodada;
- base em `concept-audit.md`;
- alterações obrigatórias;
- alterações opcionais, quando existirem;
- critério para nova rodada.

Depois de revisar `node.html`, volte ao pipeline para regenerar
`.editorial/pipeline/01-visible-text/visible-text.md` e `.editorial/pipeline/02-concept-introduction/concept-audit.md`.

Se não houver alteração obrigatória, `revision-plan.md` deve registrar que
nenhuma reescrita é obrigatória nesta rodada.

## Critério de Passagem

O guardrail passa somente quando:

- a primeira ocorrência relevante de cada conceito foi preparada;
- aliases e paráfrases listadas no ledger foram auditados;
- os títulos não usam conceitos antes do texto preparar esses conceitos;
- tabelas, cards e visuais não escondem vocabulário prematuro;
- referências finais não introduzem termos técnicos novos ou bloqueados;
- conceitos reservados a nodes futuros não sustentam a explicação do node
  atual;
- `.editorial/pipeline/02-concept-introduction/concept-audit.md` registra status `passa`;
- `.editorial/pipeline/02-concept-introduction/revision-plan.md` registra nenhuma reescrita obrigatória;
- a leitura segue de informação já dada para informação nova;
- depois de qualquer reescrita, o HTML completo foi relido.

Se o HTML foi reescrito, retorne ao pipeline para reiniciar a rodada global
desde a extração de `.editorial/pipeline/01-visible-text/visible-text.md`.
