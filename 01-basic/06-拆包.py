# python 中的拆包与js中变量的结构很相似

g_tuple = [1, 2, 3, 4]
g_list = ['a', 'b', 'c']
g_dict = {'name': 'cicades', 'gender': 'male'}


def print_inof(**kwargs):
    print(kwargs)


print(*g_tuple)   # 1, 2, 3, 4
print(*g_list)  # 'a', 'b', 'c'
print(*g_dict)  # 'name', 'gender'
print_inof(**g_dict)    # {'name': 'cicades', 'gender': 'male'}
