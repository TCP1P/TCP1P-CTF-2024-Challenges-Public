FROM python:3.9.9

RUN apt update

RUN apt install socat -y

RUN useradd -m usero

ADD . /home/usero/

RUN chown -R usero:root /home/usero

#ganti dr root ke usero
USER usero

WORKDIR /home/usero

RUN pip install -r requirements.txt --user

RUN chmod +x ./run.sh


CMD ["./run.sh"]

#CMD ["sleep","36000"]

#sudo docker-compose build
#sudo docker-compose up -d