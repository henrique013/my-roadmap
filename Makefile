.PHONY: setup
setup:
	@python3 --version >/dev/null 2>&1 || { \
		echo "python3 não encontrado."; \
		echo "Instale Python 3 e rode make setup novamente."; \
		exit 1; \
	}
	@python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" || { \
		echo "Python 3.10+ é recomendado para os scripts internos."; \
		exit 1; \
	}
	@if [ -f requirements.txt ]; then \
		echo "Instalando dependências Python de requirements.txt..."; \
		python3 -m pip install -r requirements.txt; \
	fi
	@if [ -f package-lock.json ]; then \
		echo "Instalando dependências Node com npm ci..."; \
		npm ci; \
	elif [ -f package.json ]; then \
		echo "Instalando dependências Node com npm install..."; \
		npm install; \
	else \
		echo "Nenhuma dependência Node declarada para instalar."; \
	fi
	@if [ -f package.json ]; then \
		echo "Instalando Chromium do Playwright..."; \
		npx playwright install chromium; \
	fi
	@echo "Setup concluído."
