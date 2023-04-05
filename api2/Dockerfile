FROM python:3.8

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN rm -f db.sqlite3
RUN python manage.py migrate
CMD python manage.py runserver
