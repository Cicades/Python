# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LolSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Heros(scrapy.Item):
	c_name = scrapy.Field()  # 中文名
	e_name = scrapy.Field()  # 英文名
	title = scrapy.Field()  # 称号
	tags = scrapy.Field()  # 类型
	bgstory = scrapy.Field()  #背景故事
	skins = scrapy.Field()  # 皮肤
	skills = scrapy.Field() # 技能


class HeroSkin(scrapy.Item):

	hero_name = scrapy.Field() # 英雄名
	skin_name = scrapy.Field() # 皮肤名
	img = scrapy.Field() # 图片数据二进制
		
