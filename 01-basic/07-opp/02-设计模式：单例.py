# 所谓单例，便是一个类的实例对象只能存在唯一一个


class MusicPlayer(object):
    instance = None  # instance类属性用来保存实例对象的地址
    init_flag = False

    def __new__(cls, *args, **kwargs):
        # 内置方法__new__负责为实例对象分配内存空间，并将实例对象的引用作为参数传递给__init__(self)
        # __new__()方法始终是类的静态方法，即使没有被加上静态方法装饰器
        cls.instance = super().__new__(cls) if cls.instance is None else cls.instance
        return cls.instance

    def __init__(self):
        if MusicPlayer.init_flag:
            return
        print('初始化完成！')
        MusicPlayer.init_flag = True


print(MusicPlayer())
print(MusicPlayer())
print(MusicPlayer())
