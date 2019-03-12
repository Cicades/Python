from django.contrib import admin
from booktest.models import BookInfo, HeroInfo
# Register your models here.
class BookInfoAdmin(admin.ModelAdmin):
	'''图书模型管理类'''
	list_display = ['id', 'btitle', 'bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
	list_display = ['id', 'hname', 'hskill']


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)