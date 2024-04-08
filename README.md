# python-simple-server

## docker:

`make up` for docker up & `make down` for docker down
`make test-up` for docker up & `make test-down` for docker down

## start:

`uvicorn main:app --reload`

## migrations

`alembic init migrations`

`alembic revision --autogenerate -m <Commit>`

`alembic upgrade head`

## test:

`make test-up`
run with flags `pytest -v`
