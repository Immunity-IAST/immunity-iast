all: up

vm:
	vagrant up --provision

up:
	sudo docker compose -f docker-compose/docker-compose.yml up -d --build

rebuild:
	sudo docker compose -f docker-compose/docker-compose.yml down -v
	sudo docker compose -f docker-compose/docker-compose.yml up -d --build

down:
	sudo docker compose -f docker-compose/docker-compose.yml down

format:
	isort --apply ./backend/
	black ./backend/
	cd frontend/ && npm run format

.PHONY: vm run rebuild stop format