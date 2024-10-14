#!/bin/bash

while true; do
    docker compose -p nuclei-v2 down --volumes && docker compose -p nuclei-v2 up --build --detach
    sleep 5m
done
