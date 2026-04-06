FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install poetry --break-system-packages

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

COPY . .

RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

CMD poetry run python manage.py migrate --noinput && \
    poetry run gunicorn ojoniter.wsgi:application --bind 0.0.0.0:${PORT:-8000}
