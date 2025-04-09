# Screen Play Assistant

### Tech stack

- Python
  - Django
  - Celery
- Docker
  - Docker compose
- Postgres
- Redis
- AWS

### features

- ready to deploy dockerized application
- base django project with configurations per environment
- django headless CMS (content management system) for front end consumption and a custom admin site
- django api generation helpers, a module located in "api/api/utils/api" with utils for endpoint generation from models

# Environments

if you want to change the base docker compose instruction file change the environment in the "makefile"

all environment variables should be structured in files like:

```
.envs/{env}/cloud
.envs/{env}/db
.envs/{env}/django
```

New environment files should be registered in the environment docker compose file like

```yml
env_file:
  - ./.envs/.local/.django
  - ./.envs/.local/.db
  - ./.envs/.local/.cloud
  - ./.envs/.local/.custom
```

since this are environment variables they are not committed to the code versioning system and a ".envs.example" directory with dummy variables should be in the root of the project following the same structure.

```
.envs.example/{env}/cloud
.envs.example/{env}/db
.envs.example/{env}/django
```

this has no functional purpose but helps new developers to setup their environments faster.

# Relevant commands

all relevant commands for the project are in the "makefile"

- Build the project with:
  `make build`

- Run Django Migrations with:
  `make migrate`

- Run the project with:
  `make up`

- Stop the project with:
  `make down`

many other util commands are registered in the makefile and is suggested to make an overview check of the "makefile"

for quick start of the project execute:

```
make build
make migrate
make up
```

# Project Structure

the project is divided in the following directories

### .envs

as described in "Environments", is used for environment variables, with subdirectories per environment

### .envs.example

as described in "Environments", is used for dummy environment variables, with subdirectories per environment

### api

contains all of the django backend code

### compose

contains all docker related scripts, with subdirectories per environment

### requirements

contains all of the requirements for django, with subdirectories per environment
