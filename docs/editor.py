def buttonClick():
    print("this works")
    code = Element("mpl-code").element.value
    result = executeCode(code)
    
    Element("output").element.contentDocument.body.innerHTML = result

print("v1.7")