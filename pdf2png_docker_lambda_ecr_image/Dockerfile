ARG FUNCTION_DIR="/function2"

FROM ubuntu:22.04 as build-image

##MAINTAINER Rick Torzynski "ricktorzynski@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}


RUN apt-get update \
  && apt-get install -y python3 python3-distutils python3-pip \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*
RUN apt update && apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config poppler-utils
#RUN apt-get install -y poppler-utils
#RUN apt-get install poppler-utils
#RUN sudo apt-get install poppler-utils

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y
#RUN pip3 install --upgrade pdf2image
RUN pip install pdf2image
RUN pip install numpy
RUN pip3 install opencv-python
#RUN pip3 install pypdfium2
RUN pip3 install pillow
RUN pip install boto3
#RUN pip3 install poppler-utils

RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

#COPY requirements.txt ./

#RUN pip install -r requirements.txt
##COPY A0B972.png ./
#COPY . /app
#COPY A0B972.png .${FUNCTION_DIR}

COPY app.py .${FUNCTION_DIR}

#WORKDIR /app

WORKDIR ${FUNCTION_DIR}


ENTRYPOINT [ "/usr/bin/python3", "-m", "awslambdaric" ]
CMD [ "app.handler" ]


