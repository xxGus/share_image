FROM python:3.9-slim

COPY . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gcc

RUN pip3 install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip3 install -r requirements.txt

CMD gunicorn "share_image.app:create_app()" --bind 0.0.0.0:$PORT
