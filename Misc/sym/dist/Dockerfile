FROM python:2-alpine

RUN apk add socat --update --no-cache

WORKDIR /srv
COPY jail.py run
RUN chmod 755 run

ENV PYTHONUNBUFFERED=0
EXPOSE 5000
CMD echo "fake{}" > /flag-$(head -c8 /dev/urandom | md5sum | tr -cd "[:alnum:]") && socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"./run",su=nobody
