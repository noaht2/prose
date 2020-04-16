from proseparser import step2
from sys import stdout

while True:
    try:
        print(step2(eval(input()))())
    except Exception as e:
        stdout.write(str(e))