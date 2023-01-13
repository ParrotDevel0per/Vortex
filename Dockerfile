FROM ubuntu:20.04

WORKDIR /app


RUN apt-get update -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
ENTRYPOINT FLASK_APP=main.py flask run --host=0.0.0.0