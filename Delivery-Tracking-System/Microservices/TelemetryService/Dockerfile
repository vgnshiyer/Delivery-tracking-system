FROM python:3

WORKDIR app

ADD . /app/

RUN pip install kafka-python

RUN pip install pymongo

CMD [ "python", "./TelimetryService.py" ]