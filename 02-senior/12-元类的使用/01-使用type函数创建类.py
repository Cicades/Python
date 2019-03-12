class Test(object):
    p_num = 100
    @staticmethod
    def print_msg():
        print('这是父类!')
    def __init__(self, name, age):
        self.name = name
        self.age = age

@classmethod
def type_classmethod(cls):
    print('这是使用type创建的类的类方法，类属性type_nu为:%d' % cls.type_num)

@staticmethod
def type_staticmethod():
    print('这是使用type创建的类的静态方法')

def type_instancemethod(self):
    print('这是使用type创建的类的实例方法,I am %s, %d years old' % (self.name, self.age))

type_num = 99

"""使用type创建TypeClass类"""
TypeClass = type('TypeClass', (Test,), {'type_classmethod': type_classmethod, 'type_staticmethod': type_staticmethod, 'type_instancemethod': type_instancemethod, 'type_num': 99})
t = TypeClass('cicades', 21)
t.print_msg()  # 访问父类静态方法
t.type_classmethod()  # 访问本类类方法
t.type_instancemethod()  # 访问本类实例方法
