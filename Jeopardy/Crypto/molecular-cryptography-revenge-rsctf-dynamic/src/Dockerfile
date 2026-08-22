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

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
COPY rsctf-prepare-flag.sh /usr/local/bin/rsctf-prepare-flag
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/usero /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_53cad3be5aaf3ffb679bc8f4e9f08a62bf64ead7ca58dd6 -e RSCTF_DYNAMIC_FLAG_9e892fc30a5d36be47d841722830682082e31603 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets; \
    chmod 0555 /usr/local/bin/rsctf-prepare-flag; \
    chmod a+w /home/usero/flag.png
USER usero
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
