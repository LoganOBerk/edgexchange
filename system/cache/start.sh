#!/bin/sh
exec docker-entrypoint.sh redis-server \
  --user "$CHUSER" on ">$CHPASSWORD" "~*" +@all "$@"