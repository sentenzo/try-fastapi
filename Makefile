run:
	poetry run python -m service

lint:
	poetry run isort service
	poetry run black service
	poetry run pylint service