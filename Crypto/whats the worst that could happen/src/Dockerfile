FROM python:3.9.9

RUN apt update

RUN apt install socat -y

RUN useradd -m usero

ADD . /home/usero/

RUN chown -R usero:root /home/usero

USER usero

WORKDIR /home/usero

RUN pip install -r requirements.txt --user

RUN chmod +x ./run.sh


CMD ["./run.sh"]
