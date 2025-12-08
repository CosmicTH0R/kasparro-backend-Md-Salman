up:
	docker-compose up --build -d

down:
	docker-compose down

test:
	docker-compose run app pytest

logs:
	docker-compose logs -f