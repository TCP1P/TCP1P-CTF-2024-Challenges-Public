#!/bin/bash

while true; do
    docker compose -p web-hacked down --volumes && docker compose -p web-hacked up --build --detach
    sleep 5m
done
