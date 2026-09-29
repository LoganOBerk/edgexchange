FROM python:3.12-slim

WORKDIR /backend

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

COPY . .
RUN uv pip install --system --no-cache .

EXPOSE 8000

CMD ["edgexchange", "-s", "-v", "25"]








