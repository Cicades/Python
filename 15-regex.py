"""
使用正则的步骤
1.import re 导入正则表达式的模块
2.re.compile()  创建一个Regex对象，可以选择传入第二参数
	re.DOTALL——匹配所有字符包括换行
	re.IGNORECASE——忽略大小写
	re.VERBOSE——忽略正则中的注释及空白，可以使复杂的正则表达式写的更具可读性
	可以使用管道，在compile方法的第二个参数中同时包含上述三者
3.向Regex对象的search方法传入想查找的字符串，返回一个Match对象
4.Regex的findall方法会返回一个列表并包含所有匹配到的字符串
4.调用Match对象的group方法，返回匹配的字符串组，传入整数则可获取对应的字符串组
5.Regex.sub(arg1,arg2)
	arg1 要进行替换的字符串
	arg2 被替换的字符串
"""
