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

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/ctf/flag.txt /home/ctf/chall /home/ctf /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_5308ec19097322 -e RSCTF_DYNAMIC_FLAG_1a999d2 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
