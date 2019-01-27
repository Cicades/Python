import re,sys
def checkPwd(str):
	if re.compile(r'.{8,}').search(str) ==None:
		print('输入的口令过短')
		sys.exit()
	if re.compile(r'([A-Z]+)|([a-z]+)|(d+)').search(str) == None:
		print('口令需同时包含数字，大小写字母')
		sys.exit()
	print(re.compile(r'([A-Z]+)|[a-z]+|\d+').search(str).group(1))
	print('合法口令')
str = 'NARuto,hyf0'
checkPwd(str)