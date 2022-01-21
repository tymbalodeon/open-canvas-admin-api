# UPenn Open Canvas Admin API

## Installation

- `poetry install`

# PostgreSQL

_Instructions are based on macOS installation. Details may vary on your machine._

- `brew install postgresql`
- `echo 'export PGDATA="/usr/local/var/postgres"' >> ~/.zshrc`
- `pg_ctl start`
- `createdb opencanvas`
- create the file `~/.pg_service.confg` containing:

```ini
[opencanvas]
host=localhost
user=user
dbname=opencanvas
port=5432

```
