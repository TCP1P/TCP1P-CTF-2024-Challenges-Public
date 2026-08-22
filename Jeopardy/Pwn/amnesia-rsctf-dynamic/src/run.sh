#!/bin/bash

socat tcp-l:20037,reuseaddr,fork exec:./amnesia,stderr