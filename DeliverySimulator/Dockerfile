FROM python:3

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

ADD /app /app

# Set the entrypoint
ENTRYPOINT ["python", "./app.py"]