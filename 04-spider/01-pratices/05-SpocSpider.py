import time
import requests
from selenium import webdriver
import re
import base64
import pytesseract
from PIL import Image
import json


class SpocSpider(object):
	"""华师云平台首页爬虫"""
	def __init__(self, username, password):
		self.username = username  # 云平台登录账号
		self.password = password  # 云平台登录密码
		self.start_url = 'http://spoc.ccnu.edu.cn'
		self.driver = webdriver.Chrome()
		self.get_subject_url = 'http://spoc.ccnu.edu.cn/studentHomepage/getMySite'
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest',
			'Content-Type': 'application/json;charset=UTF-8'
		}

	def login(self):
		'''登录'''
		self.driver.get(self.start_url)
		self.driver.find_element_by_id('loginName').send_keys(self.username)  # 输入账号
		self.driver.find_element_by_id('password').send_keys(self.password)  # 输入密码
		# 获取验证码
		very_code = self.get_varify_code()
		self.driver.find_element_by_id('verifCode').send_keys(very_code)  # 输入验证码
		self.driver.find_element_by_id('loginBtn').click()  # 点击登录，跳转首页

	def get_varify_code(self):
		b64_url_str = self.driver.find_element_by_id('verifCodeImg').get_attribute('src')
		# 提取base64码
		b64_str = re.sub(r'data.+?,', '', b64_url_str)
		extension_name = re.search(r'data:image/(.+?);', b64_url_str).group(1)
		img_name = 'code.' + extension_name
		with open(img_name, 'wb') as f:
			f.write(base64.b64decode(b64_str))
		# 使用tesseract识别验证码
		img = Image.open(img_name)
		return pytesseract.image_to_string(img)

	def get_content(self):
		'''获取课程列表'''
		userId = self.driver.find_element_by_id('liaoliaoUserId').get_attribute('value')  # 用户id
		cookies = {item['name']: item['value'] for item in self.driver.get_cookies()}  # 获取cookies
		data = {
			'pageNum': 1,
			'pageSize': 4,
			'termCode': '201901',
			'userId': userId
		}
		response = requests.post(self.get_subject_url, headers=self.headers, cookies=cookies, json=data)
		return response.content.decode()

	def save_content(self, origin_content):
		content = json.loads(origin_content)
		subjects = content['data']['list']
		subject_list = list()
		for subject in subjects:
			subject_list.append({
				'courseName': subject['courseName'],
				'teacherName': subject['teacherName'],
				'courseDesc': subject['classDesc'],
				'studentType': subject['domainName']
			})
		with open(self.username + '_subjects.json', 'a', encoding='utf8') as f:
			data = {
				'username': self.username,
				'subjects': subject_list
			}
			f.write(json.dumps(data, ensure_ascii=False, indent=2))

	def run(self):
		self.login()
		time.sleep(3)
		origin_content = self.get_content()
		self.save_content(origin_content)


if __name__ == '__main__':
	username = '2016214309'
	password = 'NARuto,hyf'
	spoc = SpocSpider(username, password)
	spoc.run()
