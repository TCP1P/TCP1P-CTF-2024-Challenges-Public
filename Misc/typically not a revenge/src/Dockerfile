FROM python:3.10-slim

RUN apt-get -y update && apt-get -y install socat python3 --fix-missing && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

COPY jail.py run
RUN chmod 755 run

EXPOSE 5000
CMD test -n "$GZCTF_FLAG" && flag_path=/flag-$(head -c8 /dev/urandom | md5sum | tr -cd "[:alnum:]") && printf '%s\n' "$GZCTF_FLAG" > "$flag_path" && unset GZCTF_FLAG && exec socat -dd TCP4-LISTEN:5000,fork,reuseaddr EXEC:"python3 -S ./run",su=nobody
