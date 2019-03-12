from contextlib import contextmanager

# 使用类完成上下文管理器

class File(object):

    def __init__(self, path, operation):
        self.path = path
        self.operation = operation

    def __enter__(self):
        self.file = open(self.path, self.operation)
        return self.file

    def __exit__(self, *args):
        self.file.close()


# 使用装饰器完成上下文管理器
@contextmanager
def open_file(path, operation):
    """通过使用yield可以实现与__enter__, __exit__同样的效果"""
    f = open(path, operation)
    yield f
    f.close()  # 执行完with代码块中的语句后会执行yield之后的语句

# 测试第一种方式
with File('test.text', 'w') as f:
    f.write('hello world')

# 测试第二种方式
with open_file('test2.txt', 'w') as f:
    f.write('使用装饰器实现上下文管理器!')
