FROM python:3.10.5-slim-buster

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# for psycopg2
RUN apt update && \
    apt install --no-install-recommends --no-install-suggests --assume-yes \
    gcc \
    libpq-dev \
    python-dev

RUN python -m pip install --upgrade pip

ENV app app
RUN mkdir /$app
WORKDIR /$app
ADD . /$app

RUN pip install -r requirements.txt

CMD uvicorn main:app --host 0.0.0.0 --port 8000