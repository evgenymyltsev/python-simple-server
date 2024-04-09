up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down && docker network prune -f

test-up:
	docker compose -f docker-compose-test.yml up -d

test-down:
	docker compose -f docker-compose-test.yml down && docker network prune -f
