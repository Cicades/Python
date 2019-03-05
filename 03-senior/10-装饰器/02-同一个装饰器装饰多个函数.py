def decorator(func):
    def closure(*args, **kwargs):
        print('hello')
        return func(*args, **kwargs)
    return closure

@decorator
def test(*args, **kwargs):
    print('----test-----')
    return args[0] + args[1]

@decorator
def test1(*args, **kwargs):
    print('----test2----')
    return args[0] + args[1]

res = test(2, 4)
print(res)
res = test1(10, 10)
print(res)

