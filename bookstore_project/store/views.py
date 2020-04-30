from django.shortcuts import render
from store.models import Book, Author, User, Booking

# Create your views here.
def index(request):

	books = Book.objects.all()
	context = {'books' : books}

	return render(request, 'store/index.html', context)

def detail(request, book_id):

	book = Book.objects.filer(id=book_id)
	context = {'book' : book}

	return render(request, 'store/detail.html', context)