from compiler2 import compile

# test = """
# let name = in("What's your name? ");
# out("Hi, " +  name + "!");
# 
# 
# if (name == "Alfred") {
#     out("Hi, Alfred!");
# };
# """

with open("fib.mpl", "r") as f:
    test = f.read()

print(test)

compile(test)