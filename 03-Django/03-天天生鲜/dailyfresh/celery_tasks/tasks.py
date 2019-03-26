from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

app = Celery('celery_task.tasks', broker='redis://127.0.0.1:6379/1')


@app.task
def send_active_mail(email, username, token):
    '''发送激活邮件'''
    sender = settings.EMAIL_FROM
    targets = [email]
    html_msg = '''<h1>欢迎%s注册成为会员，点击以下链接即可完成注册：
        </h1><p><a href="127.0.0.1/user/active/%s">点我完成激活！</a></p>''' % (username, token)
    send_mail('天天生鲜会员激活邮件', '', sender, targets, html_message=html_msg)
