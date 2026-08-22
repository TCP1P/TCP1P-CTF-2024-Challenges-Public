#!/bin/sh
set -eu
python3 - <<'PY'
import gzip
import os
from pathlib import Path
archive = Path('/home/ctf/rootfs.cpio.gz')
archived = bytes.fromhex('54435031507b6370202d72204b204b2d526576656e67657d')
current = os.environ['RSCTF_FLAG'].encode()
if len(current) != len(archived):
    raise SystemExit('RSCTF flag length does not match the archived initramfs slot')
raw = gzip.decompress(archive.read_bytes())
if archived in raw:
    raw = raw.replace(archived, current)
elif current not in raw:
    raise SystemExit('archived initramfs flag slot was not found')
temporary = archive.with_name(archive.name + '.rsctf')
temporary.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
temporary.replace(archive)
PY
