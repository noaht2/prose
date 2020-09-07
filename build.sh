#!/usr/bin/sh

cd ~/prose/lexer
lein uberjar
mv target/lexer-0.1.0-SNAPSHOT-standalone.jar ../lexer.jar
