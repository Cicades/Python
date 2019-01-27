# 在python中可以使用元组和字典来存储多值参数


def test(num, *nums, **person):
    """
    :param num: 普通参数
    :param nums: 以元组的方式存储参数
    :param person: 以字典的方式存储参数
    """

    print(num)  # 1
    print(nums)   # (2, 3, 4)
    print(person)  # {'name': 'cicades', 'gender': 'male'}


test(1, 2, 3, 4, name='cicades', gender='male')
