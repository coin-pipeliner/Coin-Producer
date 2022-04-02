FROM python:3.8-alpine

WORKDIR /usr/src/app

ENV ENV "dev"
ENV CODE "KRW-BTC"

COPY requirements.txt ./

RUN apk update && \
        apk add --no-cache \
        bash

# python 기본 패키지
RUN apk add --update build-base python3-dev py-pip

RUN pip3 install -r requirements.txt

COPY produce.py ./

ENTRYPOINT ["python" , "/usr/src/app/produce.py"]


