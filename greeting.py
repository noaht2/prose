#!/usr/bin/env python3
from proseparser import step2

code = [
        "bind",
        "greet",
        [
            "λ",
            ["name", "age"],
            [
                "+",
                "`Hello, '",
                "name",
                "`, you are '",
                "age",
                "` years old.'"
            ]
        ]
]

if __name__ == "__main__":
    print(step2(code)())
    import repl