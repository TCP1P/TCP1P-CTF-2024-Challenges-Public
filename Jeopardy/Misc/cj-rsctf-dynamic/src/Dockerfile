FROM ubuntu:latest

RUN useradd -m ctf

RUN apt-get update && apt-get install -y python3 python3-pip build-essential libseccomp-dev socat
RUN pip install pycparser --break-system-packages

COPY app.py /ctf/app.py
COPY start.sh /usr/local/bin/start-challenge
RUN chmod 0555 /usr/local/bin/start-challenge

EXPOSE 8080
CMD ["/usr/local/bin/start-challenge"]
