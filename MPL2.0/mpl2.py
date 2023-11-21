from compiler2 import compile

test = """
let name = in("What's your name? ");
out("Hi, " +  name + "!");

let array = [1, 2, 3, 4];

if (name == "Alfred") {
    out("Hi, Alfred!");
};
"""

compile(test)