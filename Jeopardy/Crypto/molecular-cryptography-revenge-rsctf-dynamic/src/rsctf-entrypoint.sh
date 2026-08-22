#!/bin/sh
set -eu
: "${RSCTF_FLAG:?RSCTF_FLAG is required}"
export FLAG="$RSCTF_FLAG" APPFLAG="$RSCTF_FLAG" CTF_FLAG="$RSCTF_FLAG" GZCTF_FLAG="$RSCTF_FLAG" APPSEED="$RSCTF_FLAG"
export FLAG_FILE="${RSCTF_FLAG_FILE:-/flag}" GZCTF_FLAG_FILE="${RSCTF_FLAG_FILE:-/flag}"
marker=RSCTF_DYNAMIC_FLAG_53cad3be5aaf3ffb679bc8f4e9f08a62bf64ead7ca58dd6
payload_marker=RSCTF_DYNAMIC_FLAG_9e892fc30a5d36be47d841722830682082e31603
rsctf_payload=${RSCTF_FLAG#*\{}
rsctf_payload=${rsctf_payload%\}}
if [ -f /etc/rsctf-flag-targets ]; then
  while IFS= read -r target; do
    [ -f "$target" ] || continue
    temporary=${TMPDIR:-/tmp}/rsctf-flag.$$
    sed -e "s|${marker}|${RSCTF_FLAG}|g" -e "s|${payload_marker}|${rsctf_payload}|g" "$target" > "$temporary"
    cat "$temporary" > "$target"
    rm -f "$temporary"
  done < /etc/rsctf-flag-targets
fi
if [ -x /usr/local/bin/rsctf-prepare-flag ]; then /usr/local/bin/rsctf-prepare-flag; fi
[ "$#" -gt 0 ] || { echo 'RSCTF runtime has no command' >&2; exit 1; }
exec "$@"
