# Python starter

The objective of this project is to have a starting point for future server side
python projects

It includes:

- Web server: FastAPI
- Database: SQLAlchemy (with SQLite, which be easily switched) and example
  models/relations
- Migrations: Alembic
- Example integration and unit tests
- Linting
- Type checking
- Basic Dockerfile to build relative image
- Configuration: pydantic + .env

## After cloning from template

- Modify pyproject replacing author and project name
- Rename folders and imports accordingly
- Change database drivers and migration file according to your needs (currently
  the `env.py` for the migrations removes the `+aiosqlite` driver to make it
  work synchronously)
- Adapt sqlalchemy models to your need
- Delete current migrations under `migrations/versions/`
- `make install`
- `make migrate-and-run`
