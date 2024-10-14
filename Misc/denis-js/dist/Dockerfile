FROM denoland/deno:alpine-1.40.5

RUN apk --update add socat

WORKDIR /opt/chall
COPY app.ts /opt/chall/app.ts
RUN chmod +x /opt/chall/app.ts

RUN chown -R root:root /opt/chall/

EXPOSE 6000
CMD echo "fake{flag}" > /flag-$(head -c8 /dev/urandom | md5sum | tr -cd '[:alnum:]') && socat TCP-LISTEN:6000,reuseaddr,fork EXEC:"deno run --no-prompt -A /opt/chall/app.ts",su=nobody
