.PHONY: build start stop logs ps tests

ENV ?= dev
START_SERVICES ?=
RUN_SERVICE ?=

COMPOSE_EXEC ?= docker compose

build:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml build

start:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml up -d $(START_SERVICES)

stop:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml down

run:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml run --rm $(RUN_SERVICE)

logs:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml logs $(ARGS)

ps:
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml ps

tests:
	make build
	make start
	${COMPOSE_EXEC} -f docker-compose.yml -f docker-compose.$(ENV).yml run --rm frs python manage.py test
	make stop
