#!/bin/bash

nodemon -e go --signal SIGTERM --exec 'go' run .
