FROM python:3

WORKDIR app

ADD . /app/

RUN pip install kafka-python

CMD [ "python", "./positionSimulator.py" ]