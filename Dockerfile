FROM python:3.11-alpine AS builder

ARG POETRY_VERSION=1.6.1

RUN pip install --upgrade pip
RUN pip install poetry==$POETRY_VERSION

RUN echo "Poetry version:" && poetry --version

WORKDIR /builder

COPY pyproject.toml poetry.lock poetry.toml .
RUN poetry install --no-interaction --no-ansi --only main

FROM python:3.11-alpine

ENV DIAL_BASE_URL=''
ENV SOURCES=''
ENV PROFILE=''
ENV TARGET_DIR=/sources
ENV TEMPLATES_DIR=/templates
ENV API_KEY=''
ENV JWT=''

RUN adduser -u 1001 --disabled-password --gecos "" appuser

WORKDIR /app

COPY --chown=appuser --from=builder /builder/.venv .venv
COPY aidial_app_builder_python aidial_app_builder_python
COPY templates templates
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Prepare "output" directories for code sources and docker image templates
RUN mkdir ${TARGET_DIR} ${TEMPLATES_DIR} && \
    chown -R appuser:appuser ${TARGET_DIR} ${TEMPLATES_DIR}

ENV PYTHONUNBUFFERED=True
ENV PATH=/app/.venv/bin:$PATH

USER appuser
ENTRYPOINT ["/app/entrypoint.sh"]