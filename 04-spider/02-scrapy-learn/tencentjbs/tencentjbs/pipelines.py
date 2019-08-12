# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class TencentjbsPipeline(object):
	client = MongoClient(host='localhost', port=27017)
	def process_item(self, item, spider):
		collection = self.client['tencentSpider']['jobs']
		collection.insert(item)
