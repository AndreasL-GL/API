FROM python:3.10.7-slim-buster 
RUN mkdir -p /home/app
WORKDIR /home/app

RUN python -m pip install --upgrade pip
COPY requirements.txt /home/app/
RUN pip install -r requirements.txt
# Install OpenJDK-8
RUN apt update
COPY . /home/app/