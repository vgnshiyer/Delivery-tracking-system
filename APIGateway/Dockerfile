FROM python:3

# Set the working directory
WORKDIR /app

# Copy only necessary files
COPY app.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose the specified port
ENV PORT=5000
EXPOSE $PORT

# Set the entrypoint
ENTRYPOINT ["python", "./app.py"]