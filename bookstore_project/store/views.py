from django.shortcuts import render
from store.models import Book, Author, User, Booking

# Create your views here.
def index(request):
	books = Book.objects.all()
	context = {'books' : books}

	return render(request, 'store/index.html', context)

def detail(request, book_id):
	book = Book.objects.get(pk=book_id)
	context = {'book' : book}

    form = ContactForm()
    context['form'] = form
    
	return render(request, 'store/detail.html', context)

def listing(request):
	books = Book.objects.all()
	context = {'books' : books}

	return render(request, 'store/listing.html', context)

def search(request):
    query = request.GET.get('query')
    if not query:
        books = Book.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        books = Book.objects.filter(title__icontains=query)
    if not books.exists():
        books = Book.objects.filter(authors__name__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'books': books,
        'title': title
    }
    return render(request, 'store/search.html', context)
