FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /backend

COPY system/application/backend .

RUN uv pip install --system -e .

EXPOSE 8000

CMD ["uv", "run", "edgexchange", "-s", "-v", "25"]
