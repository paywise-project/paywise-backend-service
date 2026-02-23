# Backend
backend service

___
## run db migrations

### create alembic migration
```shell
poetry run alembic revision --autogenerate
```
### apply them to local db
```shell
poetry run alembic upgrade head
```
### (optional) get the sql for it
```shell
poetry run alembic upgrade head --sql
```
### verify it worked(heck if database is in sync with models)
```shell
poetry run alembic check
```

___
## run pre-commit

### check if it's installed
```shell
pre-commit --version
```
### install pre-commit
```shell
pre-commit install
```
### apply pre-commit autoupdate
```shell
pre-commit autoupdate
```
### apply pre-commit for all files
```shell
pre-commit run --all-files
```
### deploy
```shell
make bump-patch message=""
```
