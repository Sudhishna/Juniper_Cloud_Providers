from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return render(request,'topology/topology.html')

def serialno(request):
	if request.method == "POST":
		spine=request.POST.get('spine')
		leaf=request.POST.get('leaf')
		factor=int(int(leaf)/int(spine))
		return render(request, 'topology/serialno.html', {'leaf': leaf, 'spine': spine, 'factor': factor} )
