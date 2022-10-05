include .env
export

WEB_APP_DIR = ./$(PROJ_NAME)
WEB_APP_IMG_NAME = $(PROJ_LOWER_NAME)/$(WEB_APP_LOWER_NAME)

docker-build:
	poetry export --without-hashes -f requirements.txt --output $(WEB_APP_DIR)/requirements.txt
	docker build -f $(WEB_APP_DIR)/Dockerfile -t $(WEB_APP_IMG_NAME) ./$(WEB_APP_DIR)
	docker image prune --force

docker-cleanup:
	docker rmi $(WEB_APP_IMG_NAME)
	docker image prune --force

docker-up:
	docker-compose up -d  

docker-down:
	docker-compose down

docker-dbu: down build up

docker-logs:
	docker-compose logs -f

run:
	docker-compose up -d db
	cd $(WEB_APP_DIR) && poetry run uvicorn --reload --host 0.0.0.0 --port 8000 main:app
