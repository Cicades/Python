def deco1(func):
    def closure():
        print('------deco1-----')
        func()
    return closure

def deco2(func):
    def closure():
        print('---deco2----')
        func()
    return closure

@deco1  # 再对已经改变了指向的test进行装饰
@deco2  # 先对test进行装饰
def test():
    print('----test----')

test()
