FROM ubuntu:jammy
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -yq xinetd git gcc make python3 python3-pip
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /home/ctf

RUN git clone https://github.com/FastVM/minivm.git && \
    cd minivm && \
    git checkout cb1aa65b87c94dd593e018e43d6d4a892e43267e && \
    git submodule update --init --recursive && \
    # make it fast
    make -Bj OPT='-O3 -flto'

COPY chall/ .
COPY --chmod=755 flag.txt .
RUN pip install -r requirements.txt

RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chmod +x ./start.sh
RUN chown -R ctf:ctf /home/ctf

EXPOSE 8000

CMD ./start.sh
