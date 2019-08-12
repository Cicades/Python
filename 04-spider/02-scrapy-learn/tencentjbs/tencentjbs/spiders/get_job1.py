# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GetJob1Spider(CrawlSpider):
    name = 'get_job1'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    rules = (
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+&keywords=.*&tid=\d+&lid=\d+'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+#a'), callback='parse_list', follow=True)
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['job_name'] = response.xpath('//td[@id="sharetitle"]/text()').extract_first()
        print(item)


    def parse_list(self, response):
        print(response.url)