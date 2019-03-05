import re

def application(env, set_header):
	set_header('200 ok', [('Content-Type', 'text/html;charset=utf-8')])
	url = env['url']
	if url == '/index.py':
		"""请求首页"""
		return send_index()
	elif url == '/center.py':
		"""请求中心"""
		return send_center()

def send_index():
	with open('./templates/index.html', encoding='utf8') as f:
		""""open打开的路径是相对web_server来确定的"""
		content = f.read()
		custom_msg = 'hello nickname'
		return re.sub(r'\{%content%\}', custom_msg, content)

def send_center():
	with open('./templates/center.html', encoding='utf8') as f:
		content = f.read()
		custom_msg = 'here is center'
		return re.sub(r'\{%content%\}', custom_msg, content)