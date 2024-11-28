FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
ENV DJANGO_PRODUCTION=true
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind","0.0.0.0:8000","mysite.wsgi:application"]

EXPOSE 8000