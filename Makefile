run:
	poetry run uvicorn service.__main__:app --host 0.0.0.0 --port 8000

lint:
	poetry run isort service
	poetry run black service
	poetry run pylint service

docker-up:
	poetry export --without-hashes -f requirements.txt --output service/requirements.txt
	docker-compose up --build -d

docker-down:
	docker-compose down

migrate:
	poetry run alembic upgrade head