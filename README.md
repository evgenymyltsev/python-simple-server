# python-simple-server

## docker:

`make up` for docker up & `make down` for docker down

## start:

`uvicorn main:app --reload`

## migrations

`alembic init migrations`

`alembic revision --autogenerate -m <Commit>`

`alembic upgrade heads`
