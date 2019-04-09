from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from celery_tasks.tasks import send_active_mail
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
import re
from django.conf import settings
from user.models import User, Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class RegisterView(View):
	"""用户注册处理类"""
	def get(self, request):
		'''get请求'''
		return render(request, 'register.html')

	def post(self, request):
		'''处理post请求'''
		user_name = request.POST.get('user_name')
		pwd = request.POST.get('pwd')
		cpwd = request.POST.get('cpwd')
		email = request.POST.get('email')
		allow = request.POST.get('allow')
		if not all([user_name, pwd, email, cpwd]):
			return render(request, 'register.html', {'errmsg': '输入信息不完整！'})
		if not allow == 'on':
			return render(request, 'register.html', {'errmsg': '尚未同意协议，无法注册！'})
		if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
			return render(request, 'register.html', {'errmsg': '邮箱格式不正确！'})
		if not pwd == cpwd:
			return render(request, 'register.html', {'msg': '两次输入的密码不一致！'})
		try:
			user = User.objects.get(username=user_name)
		except User.DoesNotExist:
			user = None
		if user:
			return render(request, 'register.html', {'errmsg': '用户已存在！'})
		user = User.objects.create_user(user_name, email, pwd)
		user.is_active = 0
		user.save()
		# 生成激活链接
		serializer = Serializer(settings.SECRET_KEY, 3600)  # 用django配置文件中SECRET_KEY作为其名字，并设置过期时间
		token = serializer.dumps({'user_id': user.id}).decode()  # 加密用户的信息，返回的是bytes的数据,所以要对其进行解码
		# 因为发送邮件会堵塞线程，因此使用celery(异步)来完成
		send_active_mail.delay(email, user_name, token)
		# 发送邮件
		return HttpResponse('注册完成，等待激活！')


def user_active(request, token):
	'''激活用户'''
	serializer = Serializer(settings.SECRET_KEY, 3600)
	try:
		info = serializer.loads(token)
	except SignatureExpired:
		return HttpResponse('注册链接已失效，需重新发送激活链接！')
	user_id = info.get('user_id')
	if user_id:
		user = User.objects.get(id=user_id)
		user.is_active = 1
		user.save()
	return redirect(reverse('user:login'))


class UserLogin(View):
	'''用户登录'''
	def get(self, request):
		context = dict()
		username = request.COOKIES.get('username')
		if username is not None:
			context['username'] = username
			context['checked'] = 'checked'
		return render(request, 'login.html', context)

	def post(self, request):
		'''登录'''
		username = request.POST.get('username')
		password = request.POST.get('pwd')
		remember = request.POST.get('remember')
		if not all([username, password]):
			return render(request, 'login.html', {'errmsg': '用户信息不完整！'})
		user = authenticate(username=username, password=password)
		if user is None:
			return render(request, 'login.html', {'errmsg': '账户或密码不正确！'})
		if not user.is_active:
			return render(request, 'login.html', {'errmsg': '用户尚未激活！'})
		login(request, user)
		next_url = request.GET.get('next', reverse('goods:index'))
		response = redirect(next_url)
		if remember == 'on':
			response.set_cookie('username', username)
		else:
			response.delete_cookie('username')
		return response


class UserLogoutView(View):
	'''用户退出登录'''
	def get(self, request):
		logout(request)
		return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):
	'''用户信息'''
	def get(self, request):
		#  获取用户基本信息
		addr = Address.objects.get_default_site(request.user)
		context = {'is_active': 'info', 'addr': addr, 'records': []}
		#  获取用户的浏览记录
		#  由于需要在用户浏览过程不断产生记录，因此采用redis存储记录，
		#  存储格式设计—— key: <user_id>history  value: [goods_sku_id...]
		conn = get_redis_connection('default')  # 建立连接，参数设为读取settings中的默认配置
		records = conn.lrange('{0}_history'.format(request.user.id), 0, 4)  # 读取前四条记录数据
		for sku_id in records:
			goods = GoodsSKU.objects.get(id=sku_id)
			context['records'].append(goods)
		return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
	'''用户订单'''
	def get(self, request, page):
		user = request.user
		# 获取订单信息
		orders = OrderInfo.objects.filter(user=user)
		for order in orders:
			goods_list = OrderGoods.objects.filter(order=order).order_by('-create-time')
			order.order_goods_list = goods_list
			order.text_status = OrderInfo.ORDER_STATUS_LIST[order.order_status]
		# 分页
		page_size = 1
		show_pages = 3  # 页码展示数
		p = Paginator(orders, page_size)
		try:
			sub_page = p.page(page)
		except EmptyPage:
			sub_page = p.page(1)
		except PageNotAnInteger:
			sub_page = p.page(p.num_pages)
		# 限制分页数量
		page = int(page)
		if show_pages >= p.num_pages:
			page_index_range = range(1, p.num_pages + 1)
		elif page <= (show_pages + 1) / 2:
			page_index_range = range(1, show_pages + 1)
		elif page > p.num_pages - (show_pages + 1) / 2:
			page_index_range = range(p.num_pages - (show_pages + 1) // 2, p.num_pages + 1)
		else:
			page_index_range = range(page - show_pages // 2, page + show_pages // 2 + 1)
		print(page_index_range)
		context = {'orders': sub_page, 'is_active': 'order', 'page_index_range': page_index_range}
		return render(request, 'user_center_order.html', context)

	def post(self, request):
		pass


class UserSiteView(LoginRequiredMixin, View):
	'''用户收货地址'''
	def get(self, request):
		context = {'is_active': 'site'}
		default_addr = Address.objects.get_default_site(request.user)
		context['addr'] = default_addr
		return render(request, 'user_center_site.html', context)

	def post(self, request):
		receiver = request.POST.get('reciver')
		addr = request.POST.get('addr')
		phone = request.POST.get('phone')
		zip_code = request.POST.get('zip_code')
		if not all([receiver, addr, phone]):
			return render(request, 'user_center_site.html', {'errmsg': '地址信息不完整！'})
		if re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone) is None:
			return render(request, 'user_center_site.html', {'errmsg': '请输入有效的手机号！'})
		address = Address.objects.create(receiver=receiver, addr=addr, zip_code=zip_code, phone=phone, user=request.user)
		if Address.objects.get_default_site(request.user) is None:
			address.is_default = True
		address.save()
		return redirect(reverse('user:site'))
