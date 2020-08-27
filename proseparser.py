#!/usr/bin/env python3
from typing import *
from core import *
from stdlib import *


def step2(tokenised: Union[tuple, list, str]
          ) -> Union[Cons, Number, String, Symbol]:
    """Parse Joe’s output."""

    if isinstance(tokenised, list):
        return list_(*map(step2, tokenised))
    elif isinstance(tokenised, tuple):
        return list_(*map(step2, tokenised), for_eval=False)
    else:
        try:
            return Number(float(tokenised))
        except ValueError:
            if tokenised.startswith("`") and tokenised.endswith("'"):
                return String(tokenised[1:-1])
            else:
                return Symbol(
                    tokenised,
                    # for_eval=(not tokenised.startswith("'"))
                )
