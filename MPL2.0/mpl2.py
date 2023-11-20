from compiler2 import compile

test = """
let name = in("What's your name? ");
out("Hi, " +  name + "!");

if (name == "Alfred") {
    out("Hi, Alfred!");
};
"""

compile(test)