FROM python:3.9.16-slim

COPY requirements.txt /

RUN apt update
RUN apt install -y git gcc g++ make libssl-dev \
    && git clone https://github.com/edenhill/librdkafka.git \
    && cd /librdkafka && ./configure --prefix /usr \
    && make && make install \
    && pip install -r /requirements.txt
RUN mkdir /src

ADD src /src
WORKDIR /src

ENTRYPOINT ["locust"]
