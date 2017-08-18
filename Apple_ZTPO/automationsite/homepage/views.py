from django.http import HttpResponse
from django.shortcuts import render
import re

#def index(request):
#	return render(request,'homepage/home.html')
#	return HttpResponse("Hello, world. You're at the polls index.")

def netdiag(request):
	if request.method == "POST":
		spine=request.POST.get('spine')
		leaf=request.POST.get('leaf')
		f=open('details.txt', 'w')
		f.write('spine '+spine+' \n')
		f.write('leaf '+leaf+' \n')
		f.close() 
		factor=int(int(leaf)/int(spine))
		return render(request, 'homepage/netdiag.html', {'leaf': leaf, 'spine': spine, 'factor': factor})

	
def newtest(request):
	return render(request, 'homepage/newtest.html')

def awesome(request):
	if request.method == "POST":
		spine,leaf, idlabel=readdetails()
		print(spine)
		print(leaf)
		f=open('details.txt', 'a')
		for i in range(1,int(spine)+1):
			name='Spine'+str(i)
			sn=request.POST.get(name)
			print(sn)
			f.write(str(name)+' '+str(sn)+'\n')	
		f.close()		
		f=open('details.txt','a')		
		for j in range(1, int(leaf)+1):
			name='Leaf'+str(j)
			sn=request.POST.get(name)
			f.write(str(name)+' '+str(sn)+'\n')
		f.close()
		return render(request, 'homepage/awesome.html')
                

def connection(request):
	spine, leaf, idlabel=readdetails()
	params={}
	tmp={}
	spinestate=[]
	leafstate=[]
	links=[]
	params['spine']=spine
	params['leaf']=leaf
	f=open('netstatus.txt', 'r')
	fh=f.read()
	netstatus=eval(fh)
	idstatus=netstatus.get('devices')[0]
	for key, value in idlabel.items():
		for key1, value1 in idstatus.items():
			if value == key1:
				tmp[key]='up'
	
	
	for key, value in idlabel.items():
		try:
			n=tmp[key]
		except:
			tmp[key]='down'

	for i in range(1, int(spine)+1):
		s="Spine"+str(i)
		print(type(tmp[s]))
		spinestate.append(tmp[s])
		
	for i in range(1, int(leaf)+1):
                s="Leaf"+str(i)
                leafstate.append(tmp[s])
	
	params['spinestate']=spinestate
	params['leafstate']=leafstate


	idlink=netstatus.get('links')[0]
	for key, value in idlink.items():
		d1,d2=value.split(' - ')
		for key1, value1 in idlabel.items():
			if value1==d1:
				links.append(key1)
			elif value1==d2:
				links.append(key1)
	params['links']=links

	print(params)
	return render(request, 'homepage/connection.html', params)



def readdetails():
	f=open('details.txt', 'r')
	spine=0
	leaf=0
	idlabel={}
	for line in f:
		if re.search(r'spine ', line):
			spine=re.findall('\d+', line)[0]
		elif re.search(r'leaf ', line):
			leaf=re.findall('\d+', line)[0]
		else:
			label, identity=line.split()
			idlabel[label]=identity	
	return (spine, leaf, idlabel)
