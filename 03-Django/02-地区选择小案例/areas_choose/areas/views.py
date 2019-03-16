from django.shortcuts import render
from django.http import JsonResponse
from areas.models import RegionInfo
# Create your views here.

def index(request):
	return render(request, 'areas/index.html')


def get_prov(request):
	'''返回省份数据'''
	provs = RegionInfo.objects.filter(parent__id=0)
	data = list()
	for prov in provs:
		data.append({'id': prov.id, 'name': prov.name})
	else:
		return JsonResponse({'data': data})

def get_city(request):
	parent_id = request.GET.get('parent')
	citys = RegionInfo.objects.filter(parent__id=int(parent_id))
	data = list()
	for city in citys:
		data.append({'id': city.id, 'name': city.name})
	else:
		return JsonResponse({'data': data})

def get_region(request):
	parent_id = request.GET.get('parent')
	regions = RegionInfo.objects.filter(parent__id=int(parent_id))
	data = list()
	for region in regions:
		data.append({'id': region.id, 'name': region.name})
	else:
		return JsonResponse({'data': data})
