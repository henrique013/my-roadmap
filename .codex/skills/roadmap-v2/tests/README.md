# Roadmap V2 Tests

Comandos focados:

```bash
python3 <skill-dir>/scripts/run_tests.py --mode unit
python3 <skill-dir>/scripts/run_tests.py --mode integration
python3 <skill-dir>/scripts/run_tests.py --mode portability
python3 <skill-dir>/scripts/run_tests.py --mode all
```

`unit` valida contratos, regras e runner.
`integration` e `portability` devem rodar dentro da imagem
`roadmap-v2-runner`, com o runtime já preparado no build.

No repositório, use:

```bash
make roadmap-v2-test-container
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
