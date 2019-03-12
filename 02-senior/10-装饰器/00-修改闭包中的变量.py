def closure(num):
    def func():
        nonlocal num
        num += 2
        print('传入的值加2为:%d' % num)
    return func

f = closure(5)
f()
