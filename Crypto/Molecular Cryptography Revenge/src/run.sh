#!/bin/bash

socat TCP-LISTEN:1985,reuseaddr,fork EXEC:"/usr/bin/python3 chall.py"
