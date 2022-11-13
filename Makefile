run:
	poetry run uvicorn service:app --host 0.0.0.0 --port 8000 --reload

lint:
	poetry run isort service
	poetry run black service
	poetry run pylint service

docker-build:
	poetry export --without-hashes -f requirements.txt --output service/requirements.txt
	docker-compose up --build -d

migrate:
	poetry run alembic upgrade head