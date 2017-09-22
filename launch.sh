#!/usr/bin/env bash

while true
do
    echo 'Launching...'
    python main.py
    echo 'Crashed, relaunching in 20 seconds'
    sleep 20
done
