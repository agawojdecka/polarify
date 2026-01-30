FROM python:3.13

ENV POETRY_VERSION=1.8.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

WORKDIR /code

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY alembic.ini .
COPY alembic ./alembic
COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "54321"]
