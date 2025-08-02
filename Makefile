include stacks/.env

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