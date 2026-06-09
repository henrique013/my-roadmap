# Roadmap V2 Tests

Comandos focados:

```bash
python3 <skill-dir>/scripts/run_tests.py --mode unit
python3 <skill-dir>/scripts/run_tests.py --mode integration
python3 <skill-dir>/scripts/run_tests.py --mode portability
python3 <skill-dir>/scripts/run_tests.py --mode all
```

`unit` valida contratos, regras e runner sem depender do renderer Astro.
`integration` e `portability` exigem que o setup da skill já tenha preparado o
runtime isolado.

Prepare o runtime com:

```bash
python3 <skill-dir>/scripts/setup.py
```

Checks preparados:

- contratos e modelos Pydantic;
- regras deterministicas;
- manifests e erros do runner;
- parser de saida LLM;
- snapshots e `PipelineRun`;
- gates DOM;
- fixtures de integracao overview/node;
- renderer `PageSpec -> HTML`;
- portabilidade de pacote instalado;
- bloqueio contra escrita em `<skill-dir>` durante runtime.
