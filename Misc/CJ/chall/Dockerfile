FROM ubuntu:latest

RUN useradd -m ctf

RUN apt-get update && apt-get install -y python3 python3-pip build-essential libseccomp-dev socat
RUN pip install pycparser --break-system-packages

COPY app.py /ctf/app.py

COPY flag.txt /flag.txt
RUN chown root:root /flag.txt
RUN chmod 444 /flag.txt

USER ctf
EXPOSE 8080
CMD ["socat", "TCP-LISTEN:8080,reuseaddr,fork", "EXEC:python3 -u /ctf/app.py"]