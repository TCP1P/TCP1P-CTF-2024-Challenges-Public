FROM python:2-alpine

RUN apk add socat --update --no-cache

WORKDIR /srv
COPY jail.py run
RUN chmod 755 run

ENV PYTHONUNBUFFERED=0
EXPOSE 5000
CMD echo "TCP1P{py7h0n_m374_7r1ck_n3v3r_6375_4x3d_52066ed3d3}" > /flag-$(head -c8 /dev/urandom | md5sum | tr -cd "[:alnum:]") && socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"./run",su=nobody
