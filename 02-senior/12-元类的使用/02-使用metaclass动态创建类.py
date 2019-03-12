"""利用元类的特性，将一个类中所有的属性变为大写(__开头的属性除外)"""
class MetaClass(type):
    """定义Metaclass类并继承type，那么该类也拥有创建其他类的对象的能力，所该类也成为元类"""
    def __new__(cls, name, parents, attrs):
        """
            name --> 类的名字
            parents --> 父类(元组)
            atts --> 属性(字典)
        """
        new_attrs = dict()
        for key, value in attrs.items():
            if key.startswith('__'):
                continue
            else:
                key = key.upper()
                new_attrs[key] = value
        else:
            return super().__new__(cls, name, parents, new_attrs)  # 调用type的__new__的方法类创建对象
            # return type(name, parents, new_attrs)


class Test(object, metaclass=MetaClass):
    class_name = 'Test'
    class_info = '这是测试类'
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def print_intro(self):
        print('I am %s, %d, %s' % (self.name, self.age, self.gender))


t = Test()
for key, value in t.__class__.__dict__.items():
    print(key, value, sep='---->')
