include .env
export

WEB_APP_DIR = ./$(PROJ_NAME)
WEB_APP_IMG_NAME = $(PROJ_LOWER_NAME)/$(WEB_APP_LOWER_NAME)

docker-build:
	poetry export --without-hashes -f requirements.txt --output $(WEB_APP_DIR)/requirements.txt
	docker build -f $(WEB_APP_DIR)/Dockerfile -t $(WEB_APP_IMG_NAME) ./$(WEB_APP_DIR)
	docker image prune --force

docker-up:
	docker-compose up app -d  

docker-down:
	docker-compose down --remove-orphans

docker-dbu: docker-down docker-build docker-up

docker-cleanup:
	docker rmi $(WEB_APP_IMG_NAME)
	docker image prune --force

docker-logs:
	docker-compose logs -f

run:
	docker-compose up -d db
	poetry run uvicorn --reload --port 8000 $(PROJ_NAME).main:app

test:
	docker-compose up -d db
	poetry run pytest
