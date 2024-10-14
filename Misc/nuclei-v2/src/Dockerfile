FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    unzip

# Install nuclei
RUN wget "https://github.com/projectdiscovery/nuclei/releases/download/v3.3.2/nuclei_3.3.2_linux_amd64.zip"
RUN unzip nuclei_3.3.2_linux_amd64.zip
RUN rm nuclei_3.3.2_linux_amd64.zip
RUN mv nuclei /usr/local/bin

WORKDIR /app

COPY ./app /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./flag.txt /root/flag.txt
RUN chmod 400 /root/flag.txt

COPY ./readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod u+s /readflag
RUN rm /readflag.c

RUN useradd -m ctf
USER ctf

EXPOSE 5000

CMD ["python3", "main.py"]
