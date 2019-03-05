def decorator(func):
    def closure(*args, **kwargs):
        print('hello')
        return func(*args, **kwargs)
    return closure

@decorator  # 相当执行了 test = decorator(test)
def test(*args, **kwargs):
    print('----test-----')
    return args[0] + args[1]

res = test(2, 4)
print(res)
