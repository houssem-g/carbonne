FROM python:3.10-slim

ENV POETRY_VERSION=1.4.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"


RUN apt-get update && \
    apt-get install -y \
    curl \
    python3-dev \
    build-essential \
    libpq-dev \
    postgresql-client \
    redis-server \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /src

COPY . /src

RUN poetry install --no-root

RUN chmod +x /src/app/db/init_db.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
