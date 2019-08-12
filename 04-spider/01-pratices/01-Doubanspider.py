import requests

class DoubanSpider(object):
	"""douban spider"""
	def __init__(self):
		self.base_url= "https://m.douban.com/rexxar/api/v2/subject_collection/tv_american/items?start=18&count=18&loc_id=108288"
		self.headers = {
		'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
		'Cookie': 'll="118254"; _vwo_uuid_v2=D22235E99835180FA523F191C1EBE42AA|ea35a1b00cbe2ddf8e6f1168d66cf984; gr_user_id=f715ab10-6991-432a-816b-06e1d1fdd26e; _ga=GA1.2.1247491187.1523544747; __utmv=30149280.16001; douban-fav-remind=1; viewed="11589828_4889838_10794788_1152912_26945538_1340507"; bid=6NWlDB3qUNA; __utma=30149280.1247491187.1523544747.1554264213.1555141975.39; __utmc=30149280; __utmz=30149280.1555141975.39.29.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1555141975; talionnav_show_app="0"; Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1555141981; _gid=GA1.2.1485930993.1555141981; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1555141992; _ga=GA1.3.1247491187.1523544747; _gid=GA1.3.1485930993.1555141981'
		}

	def get_content(self):
		response = requests.get(self.base_url, headers=self.headers)
		content= response.content.decode()
		return content

	def save_content(self, content):
		with open('./douban_res.json', 'w') as f:
			f.write(content)

	def run(self):
		content = self.get_content()
		self.save_content(content)


if __name__ == '__main__':
	douban = DoubanSpider()
	douban.run()