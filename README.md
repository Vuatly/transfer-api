# Transfer API

## Start application
* docker-compose up --build
* docker-compose exec -it fastapi alembic -c ./src/infra/alembic.ini upgrade head

## Docs endpoints
* http://localhost:8000/docs
* http://localhost:8000/redoc

## Run tests
* docker-compose up --build
* docker-compose exec -it fastapi alembic -c ./src/infra/alembic.ini upgrade head
* docker-compose exec -it fastapi pytest

## Simplified things
* ENV included in docker-compose.yml
* Login endpoint returns only access token
* Test libraries included in Docker build
* Not all responses included in docs.