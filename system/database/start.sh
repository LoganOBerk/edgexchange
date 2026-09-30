#!/bin/sh
export POSTGRES_USER="$DBUSER" POSTGRES_PASSWORD="$DBPASSWORD" POSTGRES_DB="$DBNAME"
exec docker-entrypoint.sh postgres "$@"