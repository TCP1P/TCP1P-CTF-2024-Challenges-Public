FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install xinetd -y
RUN groupadd -r ctf && useradd -r -g ctf ctf

COPY chall /home/ctf/chall
COPY flag.txt /home/ctf/flag.txt

RUN echo '#!/bin/bash\nservice xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service ctf\n\ 
{\n\ 
    disable = no\n\ 
    socket_type = stream\n\ 
    protocol = tcp\n\ 
    wait = no\n\ 
    user = ctf\n\ 
    type = UNLISTED\n\ 
    port = 8000\n\ 
    bind = 0.0.0.0\n\ 
    server = /home/ctf/run\n\ 
}' > /etc/xinetd.d/ctf
RUN echo '#!/bin/bash\ncd /home/ctf && ./chall' > /home/ctf/run

RUN chmod 400 /etc/xinetd.d/ctf
RUN chmod 550 /home/ctf/chall /home/ctf/run /etc/init.sh

WORKDIR /home/ctf

RUN chown -R root:ctf /home/ctf
RUN service xinetd restart
