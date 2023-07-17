def buttonClick():
    print("this works")
    code = Element("mpl-code").element.value

    pyscript.write("output", executeCode(code))

print("v1.6")