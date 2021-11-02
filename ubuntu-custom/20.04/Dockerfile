FROM ubuntu:20.04

RUN sed -i -e "s%http://[^ ]\+%http://ftp.jaist.ac.jp/pub/Linux/ubuntu/%g" /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    wget \
    curl \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*
