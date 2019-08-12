# -*- coding: utf-8 -*-
import scrapy


class GetJobsSpider(scrapy.Spider):
    name = 'get_jobs'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        job_groups = response.xpath('//table[@class="tablelist"]//tr')[1:-1]
        for job_group in job_groups:
        	job_name = job_group.xpath('.//a/text()').extract_first()
        	job_type = job_group.xpath('./td[position()=2]/text()').extract_first()
        	job_nums = job_group.xpath('./td[position()=3]/text()').extract_first()
        	job_city = job_group.xpath('./td[position()=4]/text()').extract_first()
        	item = {
        		'jobName': job_name,
        		'jobType': job_type,
        		'jobNums': job_nums,
        		'jobCity': job_city
        	}
        	yield item
        # 获取下一页url地址
        next_url = response.xpath('//a[@id="next"]/@href').extract_first()
        next_url = 'https://hr.tencent.com/' + next_url
        yield scrapy.Request(next_url, callback=self.parse)
