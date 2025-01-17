FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get clean
RUN apt-get update --allow-unauthenticated
RUN apt-get install python3-dev default-libmysqlclient-dev -y

RUN mkdir /code
WORKDIR /code
RUN pip install pip -U
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/