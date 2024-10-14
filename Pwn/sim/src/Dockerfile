FROM pwn.red/jail

COPY --from=ubuntu:22.04 / /srv
COPY /chall /srv/app/run
RUN chmod 755 /srv/app/run

ENV FLAG "TCP1P{uhmmmmm_what_the_sigma}"
RUN echo $FLAG > /srv/app/flag.txt

ENV JAIL_MEM=5M JAIL_TIME=120 JAIL_PORT=1337
EXPOSE 1337