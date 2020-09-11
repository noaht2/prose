#!/usr/bin/bash

if (( $# > 0 )); then
    tail -n +2 "$1" | java -jar parser.jar | python3 .
else
    java -jar parser.jar | python3 .
fi
