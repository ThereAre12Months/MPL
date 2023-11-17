from compiler2 import compile

test = """
let name = in("What's your name? ");
out("Hi, " +  name + "!");
"""

compile(test)