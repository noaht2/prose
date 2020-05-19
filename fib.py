#!/usr/bin/env python3
from proseparser import step2
from core import *
from stdlib import *

code = [
        [
            "defun",
            "fib",
            ["n"],
            [
                "if",
                [
                    "=",
                    "n",
                    "0"
                ],
                "0",
                [
                    "if",
                    [
                        "=",
                        "n",
                        "1"
                    ],
                    "1",
                    [
                        "+",
                        [
                            "fib",
                            [
                                "−",
                                "n",
                                "1"
                            ]
                        ],
                        [
                            "fib",
                            [
                                "−",
                                "n",
                                "2"
                            ]
                        ]
                    ]
                ]
            ],
        ],
        "2"
    ]

if __name__ == "__main__":
    print(step2(code)()())
