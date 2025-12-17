# Dockerfile – VERSION 100% FONCTIONNELLE (admin CSS + superuser + tout)
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy && pip install gunicorn

COPY cropAnomalyPlatform/ .

# Crée le dossier static (pour collectstatic)
RUN mkdir -p /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && \
                python manage.py collectstatic --noinput --clear && \
                python create_superuser.py || true && \
                gunicorn cropAnomalyPlatform.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120"]