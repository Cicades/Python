line_obj = open('hello')
text = line_obj.readline()
while text:
    print(text)
    text = line_obj.readline()
line_obj.close()
