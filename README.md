# UPenn Open Canvas Admin API

## Installation

# PostgreSQL

_Instructions are based on macOS installation. Details may vary on your machine._

- `brew install postgresql`
- `echo 'export PGDATA="/usr/local/var/postgres"' >> ~/.zshrc`
- `pg_ctl start`
- `createdb opencanvas`

## Dev Commands

# PostgreSQL

- Open interactive postgres shell: `psql opencanvas` (`pg_ctl start` if necessary)
- Quit shell: `\q`
