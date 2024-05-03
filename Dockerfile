FROM python:latest

LABEL Maintainer="Mykael Briley (bisneksual)"

WORKDIR /home/bisneksual/Documents/ygo-git/pyugioh

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["python","./app/scratch.py"]