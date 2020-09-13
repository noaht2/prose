#!/usr/bin/env python3

from sys import exit
from os import system
from json import load

from __init__ import main

while True:
    try:
        entered_code = input(">>> ")
    except (EOFError, KeyboardInterrupt):
        print("")
        exit()
    system(f"echo '{entered_code}' | java -jar parser.jar > repl-entry.json")
    with open("repl-entry.json") as f:
        pylists = load(f)
    print(main(pylists))
