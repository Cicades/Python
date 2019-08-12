import requests
from lxml import etree
import json

class TiebaSpider(object):

	def __init__(self, tieba_name):
		self.tieba_name = tieba_name
		self.base_url = 'https://tieba.baidu.com/mo/q/m?kw='+ self.tieba_name +'&pn={offset}&is_ajax=1'
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
		}
		self.total_page = 10  # 初始页数设为10页

	def send_request(self):
		'''发送请求'''
		content = requests.get(self.base_url.format(offset=0), headers=self.headers).content.decode()
		return content

	def get_content(self, origin_content):
		content = json.loads(origin_content)
		content = content['data']['content']
		html = etree.HTML(content)
		tie_groups = html.xpath('//ul[@class="threads_list"]/li[@data-floor]')
		tie_list = list()  # 本页帖子的所有数据
		for group in tie_groups:
			ti_infos = group.xpath('.//div[contains(@class, "ti_infos")]')
			if len(ti_infos) == 0:
				continue
			ti_infos = ti_infos[0]
			t_avatar = ti_infos.xpath('./div[@class="ti_avatar"]/img/@src')
			t_publish_time = ti_infos.xpath('./div[@class="ti_author_time"]//span[@class="ti_time"]/text()')
			t_author_name = ti_infos.xpath('./div[@class="ti_author_time"]//span[@class="ti_author"]/text()')
			t_title = group.xpath('.//div[@class="ti_title"]/span/text()')
			t_images = group.xpath('.//div[@class="medias_wrap clearfix"]//img/@src')
			t_replys = group.xpath('.//div[@class="ti_zan_reply clearfix"]//span/text()')
			tie_data = {
				't_info':{
					't_avatar': t_avatar,
					't_publish_time': t_publish_time,
					't_author_name': t_author_name
				},
				't_title': t_title,
				't_images': t_images,
				't_replys': t_replys
			}  # 单个帖子的所有数据
			tie_list.append(tie_data)
		return tie_list

	def save_page_content(self, tie_list, current_page):
		page_data = {
			'page': current_page,
			'content': tie_list
		}
		# print(page_data)
		with open('{}_tieba_data.json'.format(self.tieba_name), 'a', encoding='utf8') as f:
			f.write(json.dumps(page_data, ensure_ascii=False, indent=2))
			print('{}贴吧第{}页保存成功'.format(self.tieba_name, current_page))




	def run(self):
		origin_content = self.send_request()
		content = self.get_content(origin_content)
		self.save_page_content(content, 1)


if __name__ == '__main__':
	t = TiebaSpider('lol')
	t.run()