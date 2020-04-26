from django.shortcuts import render

# Create your views here.
def index(request):
	context = {'text' : "hello world"}

	return render(request, 'store/index.html', context)