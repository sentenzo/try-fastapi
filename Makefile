include .env
export

WEB_APP_DIR = ./$(PROJ_NAME)
WEB_APP_IMG_NAME = $(PROJ_LOWER_NAME)/$(WEB_APP_LOWER_NAME)

build:
	poetry export --without-hashes -f requirements.txt --output $(WEB_APP_DIR)/requirements.txt
	docker build -f $(WEB_APP_DIR)/Dockerfile -t $(WEB_APP_IMG_NAME) ./$(WEB_APP_DIR)
	docker image prune --force

cleanup:
	docker rmi $(WEB_APP_IMG_NAME)
	docker image prune --force

up:
	docker-compose up -d  

down:
	docker-compose down

logs:
	docker-compose logs -f
