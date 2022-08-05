.PHONY: run
run:
	docker-compose up --build db -d && \
	pipenv run python manage.py runserver

.PHONY: migrate
migrate:
	pipenv run python manage.py makemigrations && \
	pipenv run python manage.py migrate && \
	pipenv run python manage.py collectstatic

ARGPATH=.

.PHONY: test
test:
	clear
	docker-compose up --build db -d && \
	pipenv run pytest -vv -k $(ARGPATH)

.PHONY: mypy
mypy:
	clear
	pipenv run mypy . --config-file="../pyproject.toml"



.PHONY: shell
shell:
	pipenv run python manage.py shell

.PHONY: graph
graph:
	pipenv run python manage.py graph_models --rankdir BT api users -o my_project_visualised.png && \
	open my_project_visualised.png

.PHONY: actions
actions:
	act --container-architecture linux/amd64

.PHONY: generate-key
generate-key:
	@echo '' && \
	pipenv -q run python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
