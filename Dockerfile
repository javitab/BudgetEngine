FROM python:3-buster

WORKDIR /app

COPY py-requirements.txt /app/py-requirements.txt

RUN pip install --no-cache-dir -r py-requirements.txt
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN apt update
RUN apt upgrade -y
RUN apt install mongo-tools -y
RUN apt install nano