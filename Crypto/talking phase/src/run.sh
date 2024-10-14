#!/bin/bash

socat TCP-LISTEN:1965,reuseaddr,fork EXEC:"/usr/bin/python3 chall.py"
# ./run2.sh
# socat TCP-LISTEN:1965,reuseaddr,fork EXEC:"./kodok.sh"
