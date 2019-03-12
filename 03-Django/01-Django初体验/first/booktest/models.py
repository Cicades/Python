from django.db import models

# Create your models here.
class BookInfo(models.Model):
	"""图书模型类"""
	btitle = models.CharField(max_length=20)  # 字符串类型，最大长度为20
	bpub_date = models.DateField()  # 图书出版日期，日期类型

	def __str__(self):
		"""由于后台管理系统默认将实例对象打印显示，因此可重写__str__方法，使显示更友好"""
		return self.btitle

class HeroInfo(models.Model):
	"""人物英雄表"""
	hname = models.CharField(max_length=20)
	hgender = models.BooleanField(default=False)  # 性别，布尔类型
	hskill = models.CharField(max_length=128)  # 英雄绝招
	hbook = models.ForeignKey('BookInfo')  # 由于书籍和英雄是一对多关系，因此添加外键约束

	def __str__(self):
		return self.hname
