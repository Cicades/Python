import re
from pymysql import Connect

ROUTES = dict()

def route(url):
	def deco(func):
		ROUTES[url] = func
		def closure():
			return func()
		return closure
	return deco


@route('/index.html')
def send_index():
	with open('./templates/index.html', encoding='utf8') as f:
		""""open打开的路径是相对web_server来确定的"""
		content = f.read()
		custom_msg = ''
		conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
		cursor = conn.cursor()
		cursor.execute('select * from info;')
		data = cursor.fetchall()
		cursor.close()
		conn.close()
		html_template = """
		<tr>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>
				<input type="button" value="添加" id="toAdd" name="toAdd">
			</td>
		</tr>"""
		for item in data:
			custom_msg += html_template % item
		return re.sub(r'\{%content%\}', custom_msg, content)


@route('/center.html')
def send_center():
	with open('./templates/center.html', encoding='utf8') as f:
		content = f.read()
		custom_msg = ''
		conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
		cursor = conn.cursor()
		cursor.execute('select i.id, i.code, i.short, i.chg, i.turnover, i.price, i.highs, f.note_info from info as i inner join focus as f on i.id = f.info_id;')
		data = cursor.fetchall()
		cursor.close()
		conn.close()
		html_template = """
		<tr>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>
				<a type="button" class="btn btn-default btn-xs" href="#"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
			</td>
			<td>
				<input type="button" value="删除" id="toDel" name="toDel">
			</td>
		</tr>
		"""
		for item in data:
			custom_msg += html_template % item[1:]
		return re.sub(r'\{%content%\}', custom_msg, content)


def application(env, set_header):
	set_header('200 ok', [('Content-Type', 'text/html;charset=utf-8')])
	url = env['url']
	# if url == '/index.html':
	# 	"""请求首页"""
	# 	return send_index()
	# elif url == '/center.html':
	# 	"""请求中心"""
	# 	return send_center()
	try:
		return ROUTES[url]()
	except Exception as ret:
		return '<h1>您寻找的页面丢失了！</h1>'