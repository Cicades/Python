import requests
import re

class DuanziSpider(object):
	def __init__(self):
		self.base_url = 'https://tieba.baidu.com/p/3664912449?pn={}'
		self.pattern = re.compile(r'<div id="post_content_\d+" class="d_post_content j_d_post_content " style="display:;">(.*?)</div>', re.DOTALL)  # re.DOTALL-匹配换行空格制表符
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
		}

	def send_request(self):
		'''发送请求'''
		response = requests.get(self.base_url.format(1), headers=self.headers)
		return response.content.decode()

	def get_content(self, origin_content):
		'''提取内容'''
		return self.pattern.findall(origin_content)

	def save_content(self, filename, content_list):
		'''保存内容'''
		with open(filename, 'a', encoding='utf8') as f:
			for item in content_list:
				content = re.sub(r'<a.*?>(?P<content>.*?)</a>|<br>', '\g<content>', item)
				f.write('-'*50)
				f.write('\n')
				f.write(content.strip())
				f.write('\n')

	def run(self):
		self.save_content('joke.txt', self.get_content(self.send_request()))
		print('保存完毕！')


if __name__ == '__main__':
	duanzi = DuanziSpider()
	duanzi.run()