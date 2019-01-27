#python中的字典类似于JS中的对象
spam = {'name': 'cicades', 'age': 20, 'gender': 'male'}
#spam.keys() spam.values() spam.items() 这三个方法会分别返回由spam字典中键，值，键值对，所构成的类似列表的值，并且不能对齐进行修改
#查询字典是否存在某键
'name' in spam.keys()#True
# get() 获取根据字典的键获取值，如果键不存在则返回设置的返回值
spam.get('id',0)#结果返回0
#setDefault() 设置字典某个键的默认值
spam.setdefault('id',1)#因为spam不存在键为id的值，该方法自动为spam加上'id': 1 键值对

