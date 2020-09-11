#!/usr/bin/sh

cd ~/prose/parser
lein uberjar
mv -v target/parser-0.1.0-SNAPSHOT-standalone.jar ../parser.jar
