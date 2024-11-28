FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
ENV DJANGO_PRODUCTION=true
CMD ["gunicorn", "--bind","0.0.0.0:8000","mysite.wsgi:application"]

EXPOSE 8000