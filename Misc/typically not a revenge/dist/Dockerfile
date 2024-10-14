FROM python:3.10-slim

RUN apt-get -y update && apt-get -y install socat python3 --fix-missing && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

COPY jail.py run
RUN chmod 755 run

EXPOSE 5000
CMD echo halo12345 | fold -w1 | shuf | head -1 > /flag-$(head -c8 /dev/urandom | md5sum | tr -cd "[:alnum:]") && socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"python3 -S ./run",su=nobody
