class Test(object):
    def __init__(self, func):
        self.func = func

    def __call__(self):
        """魔术方法__call__可以让实例对象如方法一般被调用"""
        print('使用类完成装饰器')
        self.func()

@Test
def test():
    print('hello')

test()
