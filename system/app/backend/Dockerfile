# syntax=docker/dockerfile:1
# Backend image (API, job worker and ETL share it). Build context is `system/` (see docker-compose.yml): the image
# needs ../openapi.yaml. The ignore rules for this context are in Dockerfile.dockerignore next to this file.
#
# Targets
#   runtime (default)  code copied into the image; runs as an unprivileged user. Used by docker-compose.yml.
#   dev                dependencies only plus the test tools; the code comes from a bind mount of the repository at
#                      /repo (compose.dev.yml), so edits reload without rebuilding.
#
# Build argument WITH_LORA=1 adds PyTorch (CPU) and Transformers for the optional LoRA-D model (plan 2.12, WP10).
# Without it the image stays numpy-only and the frozen npz model is the only one that can serve.
FROM python:3.12.12-slim AS deps
ARG WITH_LORA=0
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 \
    OPENBLAS_NUM_THREADS=1
WORKDIR /srv/system
COPY app/backend/requirements.txt app/backend/requirements-lora.txt app/backend/
RUN pip install -r app/backend/requirements.txt \
 && if [ "$WITH_LORA" = "1" ]; then pip install -r app/backend/requirements-lora.txt; fi

# ---------------------------------------------------------------------------------------------------- dev
FROM deps AS dev
COPY app/backend/requirements-dev.txt app/backend/
RUN pip install -r app/backend/requirements-dev.txt
# compose.dev.yml runs this image as the host user (HOST_UID/HOST_GID) with supplementary group 0, so files written into
# the bind mount stay yours and the shared volumes (group 0, setgid, umask 002) stay writable by both images.
RUN mkdir -p /repo/system/app/backend/models /data/workspace \
 && chmod 2775 /repo/system/app/backend/models /data/workspace
ENV HOME=/tmp PYTHONPATH=/repo/system/app/backend:/repo/system/app
WORKDIR /repo/system/app/backend

# ---------------------------------------------------------------------------------------------------- runtime
FROM deps AS runtime
COPY app/backend app/backend
COPY app/etl app/etl
COPY openapi.yaml openapi.yaml

# The service runs as an unprivileged user in group 0. The model directory and the workspace directory are volumes
# owned by it with group 0, setgid and umask 002, so the dev containers (host user + group 0) can write there too.
# The model directory is filled by the ETL (the weights are not baked into the image).
RUN useradd --system --uid 10001 --gid 0 --home-dir /nonexistent app \
 && mkdir -p /srv/system/app/backend/models /data/workspace \
 && chown -R 10001:0 /srv/system/app/backend/models /data/workspace \
 && chmod 2775 /srv/system/app/backend/models /data/workspace
USER app

WORKDIR /srv/system/app/backend
ENV DF_OPENAPI_CONTRACT=/srv/system/openapi.yaml \
    DF_MODEL_DIR=/srv/system/app/backend/models \
    DF_WORKSPACE_DIR=/data/workspace \
    PYTHONPATH=/srv/system/app/backend:/srv/system/app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=4).status == 200 else 1)"

# One uvicorn worker on purpose: the rate limiter and the usage counters live in process memory.
# The job worker is a separate container (`worker`, implementation plan A-2) using the same image.
CMD ["sh", "-c", "umask 0002 && alembic -c alembic.ini upgrade head && exec uvicorn api.main:create_app --factory --host 0.0.0.0 --port 8000 --no-access-log"]
