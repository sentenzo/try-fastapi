APP_DIR = ./tryFastAPI

build:
	poetry export --without-hashes -f requirements.txt --output $(APP_DIR)/requirements.txt
	docker build -f $(APP_DIR)/Dockerfile -t tryfapi/web ./$(APP_DIR)

up:
	docker-compose up -d  

down:
	docker-compose down

logs:
	docker-compose logs -f
