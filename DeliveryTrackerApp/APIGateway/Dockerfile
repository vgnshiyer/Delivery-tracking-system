FROM python:3

ADD . /

RUN pip install flask

RUN pip install -U flask-cors

EXPOSE 5000

CMD [ "python", "./app.py" ]