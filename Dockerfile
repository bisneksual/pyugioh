FROM python:3.12-slim

RUN apt update && apt install tree

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . ./pyugioh

EXPOSE 8080