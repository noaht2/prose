from proseparser import step2

code = [
        "map",
        [
            "λ",
            ["x"],
            [
                "if",
                [
                    "=",
                    [
                        "%",
                        "x",
                        "15"
                    ],
                    "0"
                ],
                "`fizzbuzz'",
                [
                    "if",
                    [
                        "=",
                        [
                            "%",
                            "x",
                            "5"
                        ],
                        "0"
                    ],
                    "`buzz'",
                    [
                        "if",
                        [
                            "=",
                            [
                                "%",
                                "x",
                                "3"
                            ],
                            "0"
                        ],
                        "`fizz'",
                        "x"
                    ]
                ]
            ]
        ],
        "range",
        "0",
        "101",
        "1"
]

if __name__ == "__main__":
    print(step2(code)())