#!/usr/bin/bash

getopts r repl
#echo $repl
#echo [ -z "$repl" ]
if [ "$repl" = r ]; then
   ./repl.py
elif (( $# > 0 )); then
    tail -n +2 "$1" | java -jar parser.jar | python3 .
else
    java -jar parser.jar | python3 .
fi
