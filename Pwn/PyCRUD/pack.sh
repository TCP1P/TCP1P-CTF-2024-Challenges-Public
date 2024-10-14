#!/bin/bash

set -xe

if [ -f dist.zip ]; then
    rm dist.zip
fi

pushd src
cp flag.txt flag.txt.bak
sed -i -r 's/([^{]*)\{[^}]+\}/\1{test_flag}/' flag.txt
zip dist.zip chall.py Dockerfile docker-compose.yml flag.txt
mv flag.txt.bak flag.txt
mv dist.zip ..
popd
