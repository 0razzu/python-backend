FROM python:3.12

ENV \
  # Python’s configuration:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry’s configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.3

RUN curl -sSL https://install.python-poetry.org | python3 - && poetry --version

WORKDIR /app

COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry install --no-root --no-interaction --no-ansi

COPY ./lecture_2/hw /app/lecture_2/hw
EXPOSE 8000
CMD ["uvicorn", "lecture_2.hw.shop_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
