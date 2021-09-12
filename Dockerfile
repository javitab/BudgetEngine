FROM python:3-buster

WORKDIR /app

COPY py-requirements.txt /app/py-requirements.txt

RUN pip install --no-cache-dir -r py-requirements.txt
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt update
RUN apt upgrade -y
RUN apt install mongo-tools -y
RUN apt install nano
RUN apt install -y mongodb-mongosh