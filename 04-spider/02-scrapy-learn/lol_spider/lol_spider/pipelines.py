# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from lol_spider.items import Heros, HeroSkin
from lol_spider.settings import IMAGES_SAVE_DIR
import os

class LolSpiderPipeline(object):
	def open_spider(self, spider):
		"""当打开spider时调用"""
		self.collections = MongoClient()['lol']['heros']
		
	def process_item(self, item, spider):
		self.collections.insert(dict(item))


class SaveSkinImagePipeline(object):
	"""保存皮肤图片"""
	def process_item(self, item, spider):
		if isinstance(item, Heros):
			# 如果是hero信息
			return item
		elif isinstance(item, HeroSkin):
			# 保存图片
			save_dir = os.path.join(IMAGES_SAVE_DIR, item['hero_name'])
			if not os.path.exists(save_dir):
				os.makedirs(save_dir)
			with open(os.path.join(save_dir, '{}.jpg'.format(item['skin_name'])), 'wb') as f:
				f.write(item['img'])



