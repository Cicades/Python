def deco_p(level):
    """带参数的装饰器会将最外层的函数的返回值对目标函数进行装饰"""
    def deco_c(func):
        def closure():
            print('验证级别-%d,验证通过!' % level)
            return func()
        return closure
    return deco_c

@deco_p(3)
def test():
    print('hello world')

test()

@deco_p(5)
def test1():
    print('fuck the world')

test1()
