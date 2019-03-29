from celery_tasks.tasks import send_active_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from user.models import User
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import re
from django.conf import settings
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
