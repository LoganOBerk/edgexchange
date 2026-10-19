#!/bin/sh
exec docker-entrypoint.sh redis-server \
  --user default off \
  --user "$CHUSER" on ">$CHPASS" "~*" +@all "$@"