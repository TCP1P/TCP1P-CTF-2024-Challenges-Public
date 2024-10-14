FROM ubuntu:jammy
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y xinetd qemu-system-x86-64
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /home/ctf

COPY chall/bzImage .
COPY chall/rootfs.cpio.gz .
COPY chall/run.sh .

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
    server = /home/ctf/run.sh\n\
}' > /etc/xinetd.d/ctf

RUN chmod 400 /etc/xinetd.d/ctf
RUN chmod 444 /home/ctf/*
RUN chmod 550 /home/ctf/run.sh /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:ctf /home/ctf

RUN service xinetd restart
