from django.core.mail import send_mail
from django.conf import settings
from celery import Celery

# 初始化django环境，因为celery任务要使用到
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

# 导入包必须在初始化django环境之后
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner
from django.template import loader
# 创建celery实例
app = Celery('celery_task.tasks', broker='redis://127.0.0.1:6379/1')


@app.task
def send_active_mail(email, username, token):
    '''发送激活邮件'''
    sender = settings.EMAIL_FROM
    targets = [email]
    html_msg = '''<h1>欢迎%s注册成为会员，点击以下链接即可完成注册：
        </h1><p><a href="127.0.0.1/user/active/%s">点我完成激活！</a></p>''' % (username, token)
    send_mail('天天生鲜会员激活邮件', '', sender, targets, html_message=html_msg)



@app.task
def generate_static_index():
    '''生成静态首页'''
    # 轮播图左边的商品分类
    types = GoodsType.objects.all()
    # 轮播图
    carousels = IndexGoodsBanner.objects.all().order_by('index')
    # 轮播图右边的活动
    promotions = IndexPromotionBanner.objects.all().order_by('index')
    # 轮播图下方的同类商品list
    for type in types:
        all_goods = IndexTypeGoodsBanner.objects.filter(type=type)
        type.text_show = all_goods.filter(display_type=0).order_by('index')  # 用文字做展示的商品
        type.img_show = all_goods.filter(display_type=1).order_by('index')  # 用图片作展示的商品
    context = {
        'types': types,
        'carousel': carousels,
        'promotions': promotions,
    }
    # 加载模板
    temp = loader.get_template('index_static.html')
    # 渲染模板
    index_content = temp.render(context)
    with open(os.path.join(settings.BASE_DIR, 'static/index.html')) as f:
        f.write(index_content)