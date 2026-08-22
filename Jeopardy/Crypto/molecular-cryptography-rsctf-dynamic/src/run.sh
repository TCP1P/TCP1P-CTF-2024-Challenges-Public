#!/bin/bash

socat TCP-LISTEN:1975,reuseaddr,fork EXEC:"/usr/bin/python3 chall.py"
