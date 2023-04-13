
# FROM alpine:3.14

# RUN apk add --upgrade apk-tools && apk upgrade --available
# RUN apk add g++ python3-dev cmake gfortran patchelf openblas
# RUN apk add openblas-dev  
# RUN apk add gcc make cmake
# RUN export CXX=g++ CC=gcc 
# RUN apk add --update --no-cache curl py-pip
# RUN python3 -m ensurepip
# RUN pip3 install --no-cache --upgrade pip setuptools
# RUN pip3 install --upgrade pip
# RUN export PIP_DEFAULT_TIMEOUT=500
# RUN pip --default-timeout=1000 install scipy --only-binary=:all
# RUN apk add --no-cache --virtual .build-deps zlib-dev jpeg-dev && \
#     pip3 --default-timeout=2000 install matplotlib && \
#     apk del .build-deps
# RUN pip3 --default-timeout=2000 install wheel

FROM --platform=linux/amd64 python:3.8

RUN apt-get update -y \
    && apt-get install -y curl  py-pip \
      --no-install-recommends 



RUN mkdir -p /opt/app/tools/TG_bot
RUN mkdir /opt/app/tools/raw_data_prepare

COPY ./requirements.txt /opt/app/tools/TG_bot/
WORKDIR /opt/app

RUN pip install -r ./tools/TG_bot/requirements.txt
RUN groupadd -r tg_user && useradd -r -g tg_user -G audio,video tg_user 
    # \
    #&& mkdir -p /home/tg_user/Downloads \
    #&& chown -R tg_user:tg_user /home/tg_user
#RUN mkdir ./tools/

COPY ./tools/TG_bot/* /opt/app/tools/TG_bot/
COPY ./tools/raw_data_prepare/r2_metaData_extractor.py /opt/app/tools/TG_bot/raw_data_prepare/
COPY ./tools/raw_data_prepare/graph_preparator.py /opt/app/tools/TG_bot/raw_data_prepare/



RUN pip install -e ./tools/TG_bot/

USER tg_user
ARG FROM_DOCKER=1

# test must pass in order to check that all dependencies are properly installed
RUN pytest tests -srA

CMD ["python3", "./tools/TG_bot/bot/bot.py"]
