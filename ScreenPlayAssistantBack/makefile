DOCKER_COMPOSE_FILE = local.yml

up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up

upd:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

up_dj:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm --service-ports django

stop:
	docker compose -f $(DOCKER_COMPOSE_FILE) stop

down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down
	docker compose -f $(DOCKER_COMPOSE_FILE) stop

build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

shell:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py shell

admin:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py createsuperuser

migrate:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py migrate

m:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py migrate

mm:# Make Migrations
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py makemigrations $(app)

mnm:# Make and migrate
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py makemigrations $(app)
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py migrate

me:# Make empty migration
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py makemigrations --empty $(app)

mmm:# Make Migrations Merge
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py makemigrations --merge

permission:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py load_policies

users:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py loaddata user.json

tools:
	docker compose -f $(DOCKER_COMPOSE_FILE) run --rm django python manage.py load_tools

logs:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f -t
	
