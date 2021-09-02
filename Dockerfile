FROM python:3-buster

WORKDIR /app

COPY py-requirements.txt /app/py-requirements.txt

RUN pip install --no-cache-dir -r py-requirements.txt
RUN wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian10-x86_64-100.5.0.deb
RUN apt install ./mongodb-database-tools-debian10-x86_64-100.5.0.deb