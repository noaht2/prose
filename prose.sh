#!/usr/bin/bash

if (( $# > 0 )); then
    tail -n +2 "$1" | java -jar lexer.jar | python3 .
else
    java -jar lexer.jar | python3 .
fi
