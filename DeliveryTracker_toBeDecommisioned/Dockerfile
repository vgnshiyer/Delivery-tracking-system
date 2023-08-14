FROM python:3

COPY requirements.txt /.

RUN pip3 install -r requirements.txt

WORKDIR /app

ADD /app /app

EXPOSE 5000

ENTRYPOINT [ "python", "./app.py" ]