from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    '''商品首页'''
    def get(self, request):
        return render(request, 'index.html')
