FROM python:3.11-slim

# setup
WORKDIR /app

COPY src/ .
COPY requirements.txt requirements.txt
COPY settings.py settings.py

# install packages
RUN pip install -r requirements.txt

# run server
EXPOSE 8000
CMD python3 -m gunicorn --bind 0.0.0.0:8000 'app:app'
