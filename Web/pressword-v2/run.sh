#!/bin/bash

while true; do
    docker compose -p web-pressword-v2 down --volumes && docker compose -p web-pressword-v2 up --build --detach
    sleep 5m
done
