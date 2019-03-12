import re
from pymysql import Connect
import urllib.parse

ROUTES = dict()

def route(url):
	def deco(func):
		ROUTES[url] = func
		def closure():
			return func()
		return closure
	return deco


@route(r'/index.html')
def send_index(ret):
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
				<input type="button" value="添加" id="toAdd" name="toAdd" systemIdVaule="%s">
			</td>
		</tr>"""
		for item in data:
			custom_msg += html_template % (item + (item[1], ))
		return re.sub(r'\{%content%\}', custom_msg, content)


@route(r'/center.html')
def send_center(ret):
	with open('./templates/center.html', encoding='utf8') as f:
		content = f.read()
		custom_msg = ''
		conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
		cursor = conn.cursor()
		cursor.execute('select f.id, i.code, i.short, i.chg, i.turnover, i.price, i.highs, f.note_info from info as i inner join focus as f on i.id = f.info_id;')
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
				<a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
			</td>
			<td>
				<input type="button" value="删除" id="toDel" name="toDel" systemIdVaule="%s">
			</td>
		</tr>
		"""
		for item in data:
			custom_msg += html_template % (item[1:] + (item[0], item[0]))
		return re.sub(r'\{%content%\}', custom_msg, content)

@route(r'/add/(\d+)\.html')
def add_foucs(ret):
	"""添加关注 """
	stock_code = ret.group(1)  # 股票代号
	conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
	cursor = conn.cursor()
	# 判断是否存在此股票
	cursor.execute('select 1 from info where code = %s limit 1;', (stock_code,))
	if not cursor.fetchone():
		return '不存在对应的股票信息!'
	# 判断是否已添加关注
	cursor.execute('select * from focus inner join info on focus.info_id = info.id having code = %s;', (stock_code,))
	if cursor.fetchone():
		return '此股票已在关注列表，请勿重复添加!'
	# 若未关注，则添加关注
	cursor.execute('insert into focus (info_id) select id from info where code = %s;', (stock_code,))
	conn.commit()
	cursor.close()
	conn.close()
	return '添加成功!'


@route(r'/del/(\d+)\.html')
def del_foucs(ret):
	"""添加关注 """
	focus_id = ret.group(1)  # 关注id
	conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
	cursor = conn.cursor()
	res = cursor.execute('delete from focus where id = %d' % int(focus_id))  # execute 只能对字符串进行拼接
	if res:
		msg = '删除成功!'
	else:
		msg = '删除失败!'
	conn.commit()
	cursor.close()
	conn.close()
	return msg


@route(r'/update/(\d+)\.html')
def send_update(ret):
	with open('./templates/update.html', encoding='utf8') as f:
		""""open打开的路径是相对web_server来确定的"""
		stock_id = int(ret.group(1))
		content = f.read()
		conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
		cursor = conn.cursor()
		cursor.execute('select * from focus where id = %d;' % stock_id)
		data = cursor.fetchone()
		cursor.close()
		conn.close()
		content = re.sub(r'\{%code%\}', str(data[0]), content)  # sub中用作替换的必须是字符串，否则会报错
		content = re.sub(r'\{%note_info%\}', str(data[1]), content)
		return content


@route(r'/update/(\d+)/(.*)\.html')
def update(ret):
	stock_id = ret.group(1)
	"""由于浏览器会将url中的特殊字符进行url编码，因此在解析时需要对其进行解码码"""
	note = urllib.parse.unquote(ret.group(2), encoding='utf8')
	conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
	cursor = conn.cursor()
	sql = 'update focus set note_info = "%s" where id = %s;' % (note, stock_id)
	print(sql)
	res = cursor.execute(sql)
	if res:
		msg = '修改成功!'
	else:
		msg = '修改失败！'
	cursor.close()
	conn.commit()
	conn.close()
	return msg


def add_foucs(ret):
	"""添加关注 """
	stock_code = ret.group(1)  # 股票代号
	conn = Connect(host='localhost', port=3306, user='root', password='root', database='stock_db', charset='utf8')
	cursor = conn.cursor()
	# 判断是否存在此股票
	cursor.execute('select 1 from info where code = %s limit 1;', (stock_code,))
	if not cursor.fetchone():
		return '不存在对应的股票信息!'
	# 判断是否已添加关注
	cursor.execute('select * from focus inner join info on focus.info_id = info.id having code = %s;', (stock_code,))
	if cursor.fetchone():
		return '此股票已在关注列表，请勿重复添加!'
	# 若未关注，则添加关注
	cursor.execute('insert into focus (info_id) select id from info where code = %s;', (stock_code,))
	conn.commit()
	cursor.close()
	conn.close()
	return '添加成功!'


def application(env, set_header):
	set_header('200 ok', [('Content-Type', 'text/html;charset=utf-8')])
	request_url = env['url']
	# if url == '/index.html':
	# 	"""请求首页"""
	# 	return send_index()
	# elif url == '/center.html':
	# 	"""请求中心"""
	# 	return send_center()
	# try:
	# 	return ROUTES[url]()
	# except Exception as ret:
	# 	return '<h1>您寻找的页面丢失了！</h1>'
	"""使用正则解析url"""
	for url_reg, func in ROUTES.items():
		ret = re.match(url_reg, request_url)
		if not ret:
			continue
		else:
			return func(ret)
	return '不存在url对应的处理函数！'