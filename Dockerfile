FROM python:3.12-slim

LABEL Maintainer="Mykael Briley (bisneksual)"

RUN apt update && apt install tree

COPY ./requirements.txt .

ENV PYUGIOH_CONFIG=/pyugioh/vol/config/config.json

RUN pip install -r requirements.txt

COPY . ./pyugioh

EXPOSE 8080
