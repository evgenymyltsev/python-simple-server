# python-simple-server

## docker:

`make up` for docker up & `make down` for docker down
`make test-up` for docker up & `make test-down` for docker down

## poetry evn

`pyenv install 3.12.2`
`pyenv local 3.12.2`
`poetry install`

## start:

`poetry run start`

## migrations

`poetry run alembic init migrations`

`poetry run alembic revision --autogenerate -m <Commit>`

`poetry run alembic upgrade head`

## test:

`make test-up`
`poetry run test`

## pre commit setting:

`pre-commit install`
