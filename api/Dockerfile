FROM python:3.10.7-slim-buster 
RUN mkdir -p /home/app
WORKDIR /home/app

RUN python -m pip install --upgrade pip
COPY requirements.txt /home/app/
COPY Json2Word.tar.gz /home/app/
RUN pip install -r requirements.txt
RUN pip install Json2Word.tar.gz
RUN apt update
COPY . /home/app/