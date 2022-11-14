run:
	poetry run uvicorn service.__main__:app --host 0.0.0.0 --port 8000

lint:
	poetry run isort service tests
	poetry run black service tests
	poetry run pylint service

docker-up:
	poetry export --without-hashes -f requirements.txt --output service/requirements.txt
	docker-compose -f docker-compose-dev.yml up --build -d

docker-down:
	docker-compose -f docker-compose-dev.yml down

migrate:
	poetry run alembic upgrade head

test:
	poetry run pytest --verbose --capture=no --exitfirst
#   poetry run pytest -v -s -x
#   poetry run pytest -vsx
