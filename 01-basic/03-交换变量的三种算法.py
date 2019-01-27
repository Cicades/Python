# 交换变量的三种算法
g_num1 = 2
g_num2 = 4


def swap1(a, b):
    """使用临时变量"""
    c = a
    a = b
    b = c
    return a, b


def swap2(a, b):
    """不使用临时变量"""
    a = a + b
    b = a - b
    a = a - b
    return a, b


def swap3(a, b):
    """python特有方式，利用元组进行交换
    :param a:
    :param b:
    :return:
    """
    a, b = b, a
    return a, b


print('算法一交换后的结果为：%d, %d' % swap1(g_num1, g_num2))
print('算法二交换后的结果为：%d, %d' % swap2(g_num1, g_num2))
print('算法三交换后的结果为：%d, %d' % swap3(g_num1, g_num2))
