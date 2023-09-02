CONTAINER = 'bot'
TAIL = 100

build:
	docker compose -f docker-compose.yml build
up:
	docker compose -f docker-compose.yml up -d
down:
	docker compose -f docker-compose.yml down
logs:
	docker compose -f docker-compose.yml logs --tail=$(TAIL) -f $(CONTAINER)
exec:
	docker compose -f docker-compose.yml exec $(CONTAINER) /bin/bash

make-migrations:
	alembic revision --autogenerate
migrate:
	alembic upgrade head

compile-reqs:
	docker compose -f docker-compose.yml run --rm $(CONTAINER) bash -c 'pip install poetry && poetry export -f requirements.txt --output requirements.txt'