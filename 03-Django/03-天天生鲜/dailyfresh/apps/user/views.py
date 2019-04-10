from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from celery_tasks.tasks import send_active_mail
from django.core.urlresolvers import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from user.models import User, Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from order.models import OrderInfo
from alipay import AliPay
import re
import os
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
			goods_list = OrderGoods.objects.filter(order=order).order_by('-create_time')
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


class OrderPayView(View):
	"""支付"""
	def post(self, request):
		user = request.user
		if not user.is_authenticated():
			return JsonResponse({'res': 0, 'errmsg': '用户尚未登录!'})
		order_id = request.POST.get('orderId')
		if order_id is None:
			return JsonResponse({'res': 1, 'errmsg': '尚未选择需要支付的订单！'})
		try:
			order = OrderInfo.objects.get(
				order_id=order_id,
				user=user,
				order_status=1,  # 订单尚未支付
				pay_method=3 # 支付方式为支付宝
			)
		except OrderInfo.DoesNotExist:
			return JsonResponse({'res': 2, 'errmsg': '订单信息不合法！'})
		app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')).read()
		alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem')).read()
		alipay = AliPay(
			appid="2016092700606291",
			app_notify_url=None,  # 默认回调url
			app_private_key_string=app_private_key_string,
			# 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
			alipay_public_key_string=alipay_public_key_string,
			sign_type="RSA2",  # RSA 或者 RSA2(支付宝推荐)
			debug=True  # 默认False,沙箱环境应设为True
		)
		# 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
		order_string = alipay.api_alipay_trade_page_pay(
			out_trade_no=order_id,
			total_amount=str(order.total_price + order.transit_price),
			subject='天天生鲜在线支付:' + order_id,
			return_url=None,
			notify_url=None  # 可选, 不填则使用默认notify url
		)
		# 返回应答
		pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
		return JsonResponse({'res': 'OK', 'pay_url': pay_url})


class OrderQueryView(View):
	"""查询支付状态"""
	def post(self, request):
		user = request.user
		if not user.is_authenticated():
			return JsonResponse({'res': 0, 'errmsg': '用户尚未登录!'})
		order_id = request.POST.get('orderId')
		if order_id is None:
			return JsonResponse({'res': 1, 'errmsg': '尚未选择需要支付的订单！'})
		try:
			order = OrderInfo.objects.get(
				order_id=order_id,
				user=user,
				order_status=1,  # 订单尚未支付
				pay_method=3  # 支付方式为支付宝
			)
		except OrderInfo.DoesNotExist:
			return JsonResponse({'res': 2, 'errmsg': '订单信息不合法！'})
		app_private_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')).read()
		alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem')).read()
		alipay = AliPay(
			appid="2016092700606291",
			app_notify_url=None,  # 默认回调url
			app_private_key_string=app_private_key_string,
			# 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
			alipay_public_key_string=alipay_public_key_string,
			sign_type="RSA2",  # RSA 或者 RSA2(支付宝推荐)
			debug=True  # 默认False,沙箱环境应设为True
		)
		while True:
			response = alipay.api_alipay_trade_query(order_id)
			code = response.get('code')  # alipay网关状态
			print(response)
			if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
				# 订单支付成功
				order.trade_no = response.get('trade_no')
				order.order_status = 4  # 订单待评价
				order.save()
				return JsonResponse({'res': 'OK', 'errmsg': '订单支付成功！'})
			elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
				# 订单正在处理
				import time
				time.sleep(5)
				continue
			else:
				return JsonResponse({'res': 3, 'errmsg': response.get('msg')})


