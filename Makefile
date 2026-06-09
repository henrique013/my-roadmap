PYTHON ?= python3
ROADMAP_V2_SKILL_DIR ?= .codex/skills/roadmap-v2

.PHONY: setup
setup:
	@$(PYTHON) --version >/dev/null 2>&1 || { \
		echo "python3 não encontrado."; \
		echo "Instale Python 3 e rode make setup novamente."; \
		exit 1; \
	}
	@$(PYTHON) -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" || { \
		echo "Python 3.10+ é recomendado para os scripts internos."; \
		exit 1; \
	}
	@if [ ! -f "$(ROADMAP_V2_SKILL_DIR)/scripts/setup.py" ]; then \
		echo "Setup público da roadmap-v2 não encontrado em $(ROADMAP_V2_SKILL_DIR)/scripts/setup.py."; \
		echo "Publique as skills declaradas com update-docs antes de rodar make setup."; \
		exit 1; \
	fi
	@$(PYTHON) "$(ROADMAP_V2_SKILL_DIR)/scripts/setup.py"
	@echo "Setup concluído."
