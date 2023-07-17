def buttonClick():
    Element("output").element.contentDocument.body.innerHTML = ""
    print("this works")
    code = Element("mpl-code").element.value
    result = executeCode(code)

print("v2.3")