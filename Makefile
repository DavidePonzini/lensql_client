SHELL := /bin/bash

VENV=./venv
ENV=.env
REQUIREMENTS=requirements.txt

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

.PHONY: start psql $(VENV)_upgrade

start:
	docker compose down
	docker rmi lensql_client-server
	docker compose up

psql:
	docker exec -it lensql_client_db psql -U postgres


$(ENV):
	cp $(ENV).template $(ENV)

$(VENV):
	python -m venv $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade -r $(REQUIREMENTS)

$(VENV)_upgrade: $(VENV)
	$(VENV_BIN)/python -m pip install --upgrade -r $(REQUIREMENTS)