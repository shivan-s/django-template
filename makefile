run:
	docker-compose up -d --build db
	pipenv run python manage.py runserver

migrate:
	pipenv run python manage.py collectstatic
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate

.PHONY: test
test:
	pipenv run pytest -vv
