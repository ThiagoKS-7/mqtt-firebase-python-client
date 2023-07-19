# syntax=docker/dockerfile:1

FROM ubuntu:latest


WORKDIR /home/

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

COPY . .
EXPOSE 8083/tcp
CMD ["python", "mqtt_subscriber.py"]