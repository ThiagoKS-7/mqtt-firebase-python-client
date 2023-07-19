# syntax=docker/dockerfile:1

FROM python:latest


WORKDIR /home/
COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

COPY . .
EXPOSE 8083/tcp
CMD ["python3", "mqtt_subscriber.py"]