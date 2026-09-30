FROM postgres:16-alpine

ENV PGDATA=/data/pgdata

EXPOSE 5432

COPY --chmod=755 start.sh /usr/local/bin/start-database

HEALTHCHECK --interval=5s --timeout=5s --retries=5 \
  CMD pg_isready -d "$DBNAME" -U "$DBUSER"

ENTRYPOINT ["start-database"]