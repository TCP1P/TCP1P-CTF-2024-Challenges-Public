# check=skip=JSONArgsRecommended
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

# RSCTF dynamic-flag compatibility layer. The build-time scan records
# exact marker-bearing files; runtime replacement is therefore bounded
# to those files instead of walking the image on every team start.
USER root
COPY rsctf-entrypoint.sh /usr/local/bin/rsctf-entrypoint
RUN set -eu; \
    chmod 0555 /usr/local/bin/rsctf-entrypoint; \
    : > /etc/rsctf-flag-targets; \
    for root in /home/ctf /app /src /srv /home /opt /var/www /challenge /chall /ctf /root /usr/src /usr/local/bin /workspace /flag /flag.txt; do \
      if [ -e "$root" ]; then \
        find "$root" -xdev -type f ! -path /usr/local/bin/rsctf-entrypoint -exec grep -lF -e RSCTF_DYNAMIC_FLAG_e1a380c5a7f21565f459d32c014b8bccfd97ff64 -e RSCTF_DYNAMIC_FLAG_c3de0f05f8f84869a1d8a0088ab6f876b {} + >> /etc/rsctf-flag-targets 2>/dev/null || true; \
      fi; \
    done; \
    sort -u /etc/rsctf-flag-targets > /etc/rsctf-flag-targets.sorted; \
    mv /etc/rsctf-flag-targets.sorted /etc/rsctf-flag-targets; \
    while IFS= read -r target; do [ -f "$target" ] && chmod a+w "$target"; done < /etc/rsctf-flag-targets
ENTRYPOINT ["/usr/local/bin/rsctf-entrypoint"]
