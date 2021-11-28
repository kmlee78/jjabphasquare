dev-up:
	docker-compose up --build
dev-down:
	docker-compose down
dev-shell:
	docker-compose run --rm web /bin/bash