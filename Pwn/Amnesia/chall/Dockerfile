FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat patchelf
RUN useradd -UM amnesia

COPY amnesia /home/amnesia/amnesia
COPY flag.txt /home/amnesia/flag.txt
COPY run.sh /home/amnesia/run.sh
COPY ld-linux.so /home/amnesia/ld-linux.so
COPY libc.so.6 /home/amnesia/libc.so.6
RUN chown amnesia:amnesia /home/amnesia/flag.txt && chmod 644 /home/amnesia/flag.txt
RUN chown amnesia:amnesia /home/amnesia/flag.txt && chmod 644 /home/amnesia/flag.txt && \
    chmod +x /home/amnesia/amnesia && \
    chmod 755 /home/amnesia/ld-linux.so && \
    chmod 644 /home/amnesia/libc.so.6

RUN patchelf --set-interpreter /home/amnesia/ld-linux.so /home/amnesia/amnesia && \
	patchelf --replace-needed libc.so.6 ./libc.so.6 /home/amnesia/amnesia && \
    patchelf --set-rpath /home/amnesia /home/amnesia/amnesia

RUN chmod 655 /home/amnesia/run.sh
USER amnesia

WORKDIR /home/amnesia
EXPOSE 20037
CMD /home/amnesia/run.sh
