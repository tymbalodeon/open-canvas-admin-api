# UPenn Open Canvas Admin API

## Installation

To install project dependencies, run:

- `poetry install`

### tmux

The `make run` command requires tmux, which can be installed (on macOS) with:

- `brew install tmux`

#### Without tmux

Without tmux, you will need to start tailwind and runserver manually:

- Open a shell and run `poetry run python manage.py tailwind start`
- Open a second shell and run `poetry run python manage.py runserver`

### PostgreSQL

_Instructions are based on macOS installation. Details may vary on your machine._

- `brew install postgresql`
- `echo 'export PGDATA="/usr/local/var/postgres"' >> ~/.zshrc`
- `pg_ctl start`
- `createdb opencanvas`
- create the file `~/.pg_service.conf` containing:

```ini
[opencanvas]
host=localhost
user=user
dbname=opencanvas
port=5432
```
