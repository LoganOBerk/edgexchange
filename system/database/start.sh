#!/bin/sh
export POSTGRES_USER="$DBUSER" POSTGRES_PASSWORD="$DBPASS" POSTGRES_DB="$DBNAME"
exec docker-entrypoint.sh postgres "$@"