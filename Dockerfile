FROM python:3.10

WORKDIR /app
COPY requirements /app/requirements

ENV PYTHONPATH="${PYTHONPATH}:/app" \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE="auction.settings.prod"

RUN pip install -r requirements/prod.txt

COPY auction /app/auction

RUN django-admin collectstatic --noinput --settings auction.settings.base

EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "auction.wsgi:application"]