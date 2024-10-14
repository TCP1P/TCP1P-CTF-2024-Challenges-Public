FROM ubuntu@sha256:b359f1067efa76f37863778f7b6d0e8d911e3ee8efa807ad01fbf5dc1ef9006b

RUN groupadd -r ctf && useradd -r -g ctf ctf

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

COPY flag.txt /home/ctf/flag.txt
COPY chall /home/ctf/chall

RUN chmod 644 /home/ctf/flag.txt
RUN chmod 755 /home/ctf/chall
RUN chown -R root:ctf /home/ctf

WORKDIR /home/ctf
USER ctf
CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./chall,stderr,pty,cfmakeraw,echo=0"]
