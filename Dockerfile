FROM python:3.9.16-slim

COPY requirements.txt /

RUN apt update
RUN apt install -y git gcc g++ make libssl-dev \
    && pip install -r /requirements.txt

ADD src /src

WORKDIR /src

ENTRYPOINT ["locust"]
