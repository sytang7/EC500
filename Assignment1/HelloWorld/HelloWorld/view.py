from django.shortcuts import render

def hello(request):
	context  ={}
	context['hello123'] = ''
	return render (request, 'hello.html',context)

# def python(request):
#         py = request.GET.get('py')
#         os.system('open /applications/TSYMINI.py')
#         return render(request,'callotherapp/callother.html',{'text':'ran  py successful'})

def search(request):

	ctx ={}
	
	if request.POST:
		ctx['rlt'] = request.POST['name']
		
	return render(request, "post.html", ctx)


