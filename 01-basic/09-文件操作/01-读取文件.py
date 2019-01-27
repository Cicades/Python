line_obj = open('./09-文件操作/hello')
text = line_obj.readline()
while text:
    print(text)
    text = line_obj.readline()
line_obj.close()
