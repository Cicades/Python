class Goods(object):

    def __init__(self):
        self.goods_price = 100

    def get_price(self):
        print('该商品的价格为%d' % self.goods_price)

    def set_price(self, value):
        self.goods_price = value
        print('商品的价格已更改为为%d!' %self.goods_price)

    def del_price(self):
        self.goods_price = 0
        print('该商品的价格已置为0')
    
    # 使用property方法可以类属性, property方法拥有四个参数分别用于获取，设置，删除，查看注释
    Price = property(get_price, set_price, del_price)


goods = Goods()
goods.Price = 100
goods.Price
del goods.Price
