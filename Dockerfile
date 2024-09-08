FROM python:3.9-slim-buster

# Install PostgreSQL development libraries and build dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /code
COPY *.py /code/
WORKDIR /code
ENV FLASK_APP=flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80