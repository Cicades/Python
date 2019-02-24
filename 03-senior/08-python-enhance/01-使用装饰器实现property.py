class Goods(object):

    def __init__(self):
        self.goods_price = 100

    @property
    def price(self):
        print('该商品的价格为%d' % self.goods_price)

    @price.setter
    def price(self, value):
        self.goods_price = value
        print('商品的价格已更改为为%d!' %self.goods_price)

    @price.deleter
    def price(self):
        self.goods_price = 0
        print('该商品的价格已置为0')


goods = Goods()
goods.price = 100
goods.price
del goods.price
