# -*- coding: utf-8 -*-
import scrapy
import re
import json
from lol_spider.items import Heros, HeroSkin


class HerosSpider(scrapy.Spider):
	name = 'heros'
	allowed_domains = ['qq.com']
	start_urls = ['https://lol.qq.com/biz/hero/champion.js']
	detail_base_url = 'https://lol.qq.com/biz/hero/{}.js'

	def parse(self, response):
		content = response.body.decode()
		data = re.search(r'LOLherojs\.champion=(.*)', content).group(1)[:-1]
		hero_list = json.loads(data, encoding='utf-8')['data']
		for hero in hero_list.values():
			item = Heros()
			item['e_name'] = hero['id']
			item['c_name'] = hero['title']
			item['title'] = hero['name']
			item['tags'] = hero['tags']
			# 获取详细页响应
			yield scrapy.Request(
				self.__class__.detail_base_url.format(item.get('e_name')), 
				callback=self.parse_detail,
				meta={'item': item})

	def parse_detail(self, response):
		item = response.meta['item']
		content = response.body.decode()
		data = re.search(r'LOLherojs\.champion\.{}=(.*)'.format(item['e_name']), content).group(1)[:-1]
		hero_info = json.loads(data, encoding='utf-8')['data']		
		# 获取皮肤信息
		# print(data['skins'])
		# item['skins'] = [ {'id': skin['id'], 'name': skin['name']} for skin in hero_info['skins'] ]
		item['skins'] = list()
		for skin in hero_info['skins']:
			item['skins'].append({'id': skin['id'], 'name': skin['name']})
			# # 下载图片
			# yield scrapy.Request(
			# 	'https://ossweb-img.qq.com/images/lol/web201310/skin/big{}.jpg'.format(skin['id']), 
			# 	callback=self.parse_skin,
			# 	meta={'skin': {'hero_name': item['e_name'], 'skin_name': skin['name']}}
			# 	)

		# 获取技能信息
		item['skills'] = [
			{
				'id': skill['id'], 
				'name': skill['name'], 
				'desc': skill['description'], 
				'img_url': 'https://ossweb-img.qq.com/images/lol/img/spell/{}.png'.format(skill['id'])
			} for skill in hero_info['spells']]

		item['skills'].append({
			'id': item['e_name'] + 'P',
			'name': hero_info['passive']['name'],
			'desc': hero_info['passive']['description'],
			'img_url': 'https://ossweb-img.qq.com/images/lol/img/passive/{}_P.png'.format(item['e_name'])
			})
		item['bgstory'] = hero_info['blurb']
		yield item

	def parse_skin(self, response):
		"""下载图片"""
		skin = HeroSkin()
		skin['hero_name'] = response.meta['skin']['hero_name']
		skin['skin_name'] = response.meta['skin']['skin_name']
		skin['img'] = response.body
		yield skin