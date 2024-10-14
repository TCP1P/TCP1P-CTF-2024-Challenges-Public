#!/bin/bash

socat TCP-LISTEN:19328,reuseaddr,fork EXEC:"/usr/bin/python3 chall.py"
