FROM redis:7-alpine

EXPOSE 6379

COPY --chmod=755 start.sh /usr/local/bin/start-cache

HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
  CMD redis-cli ping

ENTRYPOINT ["start-cache"]