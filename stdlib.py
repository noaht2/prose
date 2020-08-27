#!/home/noaht2/Documents/prose2/prose2.py --skip-first-line
# [["def", "let",
#   ["lambda", "args",
#    ["if",
#     ["!=", ["rest", ["rest", "args"]], []],
#     ["let1",
#      ["first", ["first", "args"]],
#      ["first", ["rest", ["first", "args"]]],
#      ["let",
#       ["rest", ["rest", ["first", "args"]]], ["first", ["rest", "args"]]]],
#      ["let1",
#       ["first", ["first", "args"]],
#       ["first", ["rest", ["first", "args"]]],
#       ["rest", "args"]]]]],
#  [[["x", "1"], "x"]]]
["list",
 ["def", "fn1", ["lambda", "app", ["lambda", "arg", ["app", ["eval", "arg"]]]]],
 [["fn1", ["lambda", "x", ["+", "x", "1"]]], "2"]]
