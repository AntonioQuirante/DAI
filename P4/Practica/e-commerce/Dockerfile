# Dockerfile
FROM python:3.11-alpine

WORKDIR /e-commerce
COPY . /e-commerce

RUN apk update && apk add --no-cache \
        python3-dev py3-pip py3-setuptools \
        libffi-dev libxml2-dev libxslt-dev \
        tiff-dev jpeg-dev zlib-dev freetype-dev \
        lcms2-dev libwebp-dev tcl tk tk-dev \
        gcc musl-dev

# Agregar las dependencias al contenedor e instalar las dependencias de Python
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Instalar Pillow
RUN pip install Pillow
RUN pip install django-allauth
