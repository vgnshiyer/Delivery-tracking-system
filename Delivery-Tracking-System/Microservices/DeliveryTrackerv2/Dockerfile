FROM python:3
LABEL maintainer="VIGNESH IYER"

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

ADD /app /app