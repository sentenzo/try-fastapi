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
ENV pkg tryFastAPI
RUN mkdir -p /$app/$pkg
WORKDIR /$app
ADD . /$app/$pkg

RUN pip install -r $pkg/requirements.txt

CMD uvicorn $pkg:app --host 0.0.0.0 --port 8000