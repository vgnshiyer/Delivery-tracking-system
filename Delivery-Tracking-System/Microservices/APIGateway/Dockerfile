FROM python:3

ADD . /

RUN pip install flask

RUN pip install -U flask-cors

RUN pip install requests

EXPOSE 5000

CMD [ "python", "./apigw.py" ]