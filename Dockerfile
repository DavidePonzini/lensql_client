FROM python:3.11

WORKDIR /app

# Requirements
COPY *.py .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Ports
EXPOSE 5000

CMD [ "python", "main.py" ]