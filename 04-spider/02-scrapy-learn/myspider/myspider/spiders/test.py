# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
    	groups = response.xpath('//div[@class="tea_con"]//li')
    	for group in groups:
    		name = group.xpath('.//h3/text()').extract_first()
    		title = group.xpath('.//h4/text()').extract_first()
    		item = {'name': name, 'title': title}
    		yield item
