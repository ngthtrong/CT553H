# Build context is topics/degron-footprint/system (see docker-compose.yml): the image needs ../openapi.yaml.
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 OPENBLAS_NUM_THREADS=1
WORKDIR /srv/system

COPY app/backend/requirements.txt app/backend/requirements.txt
RUN pip install -r app/backend/requirements.txt

COPY app/backend app/backend
COPY app/etl app/etl
COPY openapi.yaml openapi.yaml

# the service runs as an unprivileged user; /srv/system/app/backend/models is a volume owned by it
RUN useradd --system --uid 10001 --home-dir /nonexistent app \
 && mkdir -p /srv/system/app/backend/models && chown -R app /srv/system/app/backend/models
USER app

WORKDIR /srv/system/app/backend
ENV DF_OPENAPI_CONTRACT=/srv/system/openapi.yaml \
    DF_MODEL_DIR=/srv/system/app/backend/models \
    PYTHONPATH=/srv/system/app/backend:/srv/system/app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=4).status == 200 else 1)"

# One worker on purpose: the rate limiter and the usage counters live in process memory.
CMD ["sh", "-c", "alembic -c alembic.ini upgrade head && exec uvicorn api.main:create_app --factory --host 0.0.0.0 --port 8000 --no-access-log"]
