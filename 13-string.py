"""
1.多行注释：起始结束为三个双引号
2.python的字符串支持双引号
3.多行输入：’‘’
4.字符串支持切片---不改变源字符
5.查找：in not in
6.大小写：upper(),lower(),isupper(),islower()---不改变源字符
7.字符串校验方法
	isalpha() 全为字母时为true
	isalnum() 仅含数字和字母时为true
	isdecimal() 仅含数字字符时为true
	isspace() 仅含空格，制表符，换行，且不为空时为true
	istitle() 字符串首字母大写，其余为小写时为true
	startswith()
	endswith()
8.str.join(list) 返回的是新的字符串
9.str.split()	默认按照空格，制表符，换行进行分割
10.字符串填充
	center(),ljust(),rjust(),这三个方法需要传入两个参数，
	第一个为填充后的字符串长度，第二个为被用作填充的字符
11.删除空白strip(),lstrip(),rstrip(),也可传入想要删除的字符
12.pyperclip下的copy(str)和paste(),前者将str发送到计算机的剪贴版，后者输出剪贴版的内容
"""
import pyperclip
print('*'.join(['hello', 'world']))#hello*world
print('hello'.center(10,'*'))#**hello***
pyperclip.copy('hello world')
pyperclip.paste()#hello world
