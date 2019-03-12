from django.shortcuts import render
from booktest.models import BookInfo, HeroInfo

# Create your views here.

def index(request):
	return render(request, 'booktest/index.html', {'books': BookInfo.objects.all()})

def show_details(request, bid):
	book = BookInfo.objects.get(id=bid)
	heros = book.heroinfo_set.all()
	return render(request, 'booktest/details.html', {'book': book, 'heros':heros})
