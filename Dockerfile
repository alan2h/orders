FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY /requirements/base.txt /code/

RUN pip install -r base.txt

COPY . /code/
