import sys
import pyperclip
PASSWORDS = {'email': 'NARuto,hyf', 'ubuntu': 'cicades', 'qq': 'NARuto,hyf'}
if len(sys.argv) < 2:
	#python 14-pw.py qq
	print('Usage: python pw.py [account] -copy account password')
	input()
	sys.exit()
account = sys.argv[1]
if account not in PASSWORDS.keys():
	print('不存在' + account + '对应的密码！你可以输入y进行添加，或n退出')
	if input().lower() != 'y':
		sys.exit()
	else:
		print('请输入键值：')
		newKey = input()
		print('请输入密码：')
		newPassword = input()
		PASSWORDS[newKey] = newPassword
		print('添加成功！')
		sys.exit()
pyperclip.copy(PASSWORDS[account])
print(account + '对应的密码已复制到剪贴版！')
input()
		