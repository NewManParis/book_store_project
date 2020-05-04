from django.shortcuts import render
from store.models import Book, Author, User, Booking
from .forms import ContactForm, ParagraphErrorList
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from store.choices import * 

# Create your views here.
def index(request):
    books = Book.objects.all()
    context = {'books' : books}

    return render(request, 'store/index.html', context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {'book' : book}
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            user_email = form.cleaned_data['user_email']
            user_name = form.cleaned_data['user_name']

            try:
                with transaction.atomic():
                    contact = User.objects.filter(user_email=user_email)
                    if not contact.exists():
                        # If a contact is not registered, create a new one.
                        contact = User.objects.create(
                            user_email=user_email,
                            user_name=user_name
                        )
                    else:
                        contact = contact.first()

                    book = get_object_or_404(Book, id=book_id)
                    booking = Booking.objects.create(
                        user=contact,
                        book=book
                    )
                    book.status = BORROWED
                    book.save()
                    return render(request, 'store/merci.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
    else:
        form = ContactForm()

    context['form'] = form
    context['errors'] = form.errors.items()
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
