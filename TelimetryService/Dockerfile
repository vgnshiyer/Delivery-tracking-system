FROM python:3

# Copy requirements
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy necessary files
ADD /app /app

# Set the entrypoint
ENTRYPOINT ["python3", "./app.py"]