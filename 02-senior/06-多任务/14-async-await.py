# -*- coding: utf-8 -*-
# @Author: Cicades
# @Date:   2019-04-23 11:37:29
# @Last Modified by:   寒蝉HYF
# @Last Modified time: 2019-04-23 11:46:41

class PotatoSale(object):
	"""使用async、await完成西红柿异步交易"""
	def __init__(self, init_stock):
		self.stock = init_stock # 初始库存

	def get