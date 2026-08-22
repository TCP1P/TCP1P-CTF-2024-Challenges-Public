#!/bin/sh
set -eu
python3 - <<'PY'
import os
from PIL import Image, ImageDraw
flag = os.environ['RSCTF_FLAG']
image = Image.new('L', (max(640, len(flag) * 8), 96), color=255)
ImageDraw.Draw(image).text((16, 36), flag, fill=0)
image.save('flag.png')
PY
