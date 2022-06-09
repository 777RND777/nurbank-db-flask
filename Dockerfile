FROM python:3.9

ENV SECRET_KEY=""
ENV SQLALCHEMY_DATABASE_URI=""

RUN mkdir -p /nurbank-db-flask
WORKDIR /nurbank-db-flask

COPY . /nurbank-db-flask/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "manage.py"]