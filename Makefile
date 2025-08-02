include stacks/.env

setup/local:
	@echo "Setting up local development environment..."
	@echo "Checking for uv installation..."
	@which uv > /dev/null || (echo "Installing uv..." && curl -LsSf https://astral.sh/uv/install.sh | sh)
	@export PATH="$$HOME/.local/bin:$$PATH" && \
	echo "Ensuring required Python version is available..." && \
	uv python install && \
	echo "Installing Python dependencies..." && \
	uv sync
	@echo "Checking for Node.js installation..."
	@which node > /dev/null || (echo "Please install Node.js from https://nodejs.org/" && exit 1)
	@echo "Installing Node.js dependencies..."
	@cd app/client && npm install
	@echo "✅ Local environment setup complete!"

build:
	@docker build -t ${APP_NAME}:v${APP_VERSION} .

up/local:
	@docker compose -f stacks/docker-compose-local.yml up -d

down/local:
	@docker compose -f stacks/docker-compose-local.yml down

exec/%:
	@container_id=$$(docker ps -q -f "name=${APP_NAME}-$*-1"); \
	if [ -n "$$container_id" ]; then \
		docker exec -it $$container_id /bin/bash; \
	else \
		echo "Service not found: $*"; \
	fi

logs/%:
	@container_id=$$(docker ps -q -f "name=${APP_NAME}-$*-1"); \
	if [ -n "$$container_id" ]; then \
		docker logs --tail 10 $$container_id; \
	else \
		echo "Service not found: $*"; \
	fi