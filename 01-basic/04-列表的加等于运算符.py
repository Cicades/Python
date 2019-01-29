g_list = list(range(4))
g_sublist = [7, 8]


def add_item(l1, l2):
    """列表的‘+=’运算符相当于列表的extend方法，同时会改变的实参的内容"""
    l1 += l2


def add_item2(l1, l2):
    """列表的‘+=’运算符不等同于l1 = l1 + l2"""
    l1 = l1 + l2  # l1对应了一个新的列表的引用，即l1是函数内部的局部变量，不同于l1全局变量 


add_item(g_list, g_sublist)
print(g_list)

add_item2(g_list, g_sublist)
print(g_list)
