FROM python:3.12-slim

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

COPY pyproject.toml ./
RUN uv pip install --system --no-cache -r pyproject.toml

COPY . .
RUN uv pip install --system --no-cache --no-deps .

EXPOSE 8000

HEALTHCHECK --interval=3s --timeout=3s --retries=20 --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')"

CMD ["edgexchange", "-s", "-v", "25"]