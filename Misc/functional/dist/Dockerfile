FROM python:3.10-slim
RUN pip install regex --no-cache
RUN apt-get -y update && apt-get -y install socat python3 --fix-missing && rm -rf /var/lib/apt/lists/*

WORKDIR /srv
COPY jail.py run

ENV COUNT=0
RUN mkdir flags
RUN chmod 755 run

EXPOSE 5000
CMD echo REDACTED | base64 | paste -sd "" | fold -w1 | grep -n . | shuf | while read byte; do echo $byte > flags/$COUNT; COUNT=$((COUNT+1)); done && socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"./run",su=nobody
