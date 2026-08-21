#!/bin/sh
set -eu

: "${RSCTF_FLAG:?RSCTF_FLAG is required}"
umask 022
printf '%s\n' "$RSCTF_FLAG" > /flag.txt
chown root:root /flag.txt
chmod 0444 /flag.txt
unset RSCTF_FLAG

exec socat TCP-LISTEN:8080,reuseaddr,fork "EXEC:python3 -u /ctf/app.py,su=ctf"
