import sys,re
def strip(str,arg = None):#arg 是可选参数
	str = re.compile(r'^\s*').sub('',str)
	str = re.compile(r's*$').sub('',str)
	print(str)
strip('     hello world   ')