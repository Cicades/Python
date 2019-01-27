try:
    num = int(input('请输入一个正整数！'))
    print('the result is %.2f' % (8 / num))
except ZeroDivisionError:
    # 具体错误
    print('除零错误！')
except Exception as res:
    # 未知错误
    print('未知错误：%s' % res)
else:
    print('程序正常执行！没有发现错误')  # try子句没有出现错误
finally:
    print('程序执行完毕！')  # 不管try子句中有没有出现错误，都会执行此代码
