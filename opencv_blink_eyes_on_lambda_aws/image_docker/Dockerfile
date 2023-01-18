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
  && apt-get -y install tesseract-ocr \
  && apt-get install -y python3 python3-distutils python3-pip \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip3 install pytesseract
RUN pip3 install opencv-python
RUN pip3 install pillow
RUN pip install dlib
RUN pip install scipy

RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

COPY requirements.txt ./

RUN pip install -r requirements.txt

##COPY A0B972.png ./
#COPY . /app

COPY shape_predictor_68_face_landmarks.dat .${FUNCTION_DIR}
COPY app_vid.py .${FUNCTION_DIR}

#WORKDIR /app

WORKDIR ${FUNCTION_DIR}


ENTRYPOINT [ "/usr/bin/python3", "-m", "awslambdaric" ]
CMD [ "app_vid.handler" ]


