FROM python:latest

WORKDIR /app

# Requirements
RUN pip install --no-cache-dir --upgrade pip
COPY *.py .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Ports
EXPOSE 5000

CMD [ "python", "main.py" ]
