def input_password():
    password = input('请输入密码：')
    if len(password) > 20 or len(password) < 9:
        raise Exception('密码长度不符合规范！')
    return password


try:
    print(input_password())
except Exception as res:
    print('程序异常：%s' % res)
