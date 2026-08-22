# check=skip=JSONArgsRecommended
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

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/amnesia/libc.so.6 /home/amnesia/ld-linux.so /home/amnesia/run.sh /home/amnesia/flag.txt /home/amnesia/amnesia /home/amnesia /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_bdf5d66ee96311bf446b26be16ef71894b24cec15 -e RSCTF_DYNAMIC_FLAG_69fb89e3642c28143783acd5449b3b6cb5 {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
USER amnesia
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
