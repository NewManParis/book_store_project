from django.shortcuts import render
from store.models import Book, Author, User, Booking
from .forms import ContactForm, ParagraphErrorList, RegisterForm
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from store.choices import * 
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def user_account(request):
    return render(request, 'store/account.html', locals())

def user_register(request):

    # if this is a POST request we need to process the form data   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_repeat = form.cleaned_data['password_repeat']

            try:
                with transaction.atomic():
                    if User.objects.filter(username=username).exists():
                        return render(request, 'store/register.html', {
                            'form': form,
                            'error_message': 'Username already exists.'
                        })
                    elif User.objects.filter(email=email).exists():
                        return render(request, 'store/register.html', {
                            'form': form,
                            'error_message': 'Email already exists.'
                        })
                    elif password != password_repeat:
                        return render(request, 'store/register.html', {
                            'form': form,
                            'error_message': 'Passwords do not match.'
                        })
                    else:
                        # Create the user:
                        user = User.objects.create_user(username, email, password)
                        user.save()
                       
                        # Login the user
                        login(request, user)
                       
                        # redirect to accounts page:
                        return HttpResponseRedirect('/store/account')
            except:
                return render(request, 'store/register.html', {
                    'form': form,
                    'error_message': '"Une erreur interne est apparue. Merci de recommencer votre requête."'
                    })

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})

def index(request):
    books = Book.objects.filter(status=1).order_by('-created_at')[:12]
    context = {
    'books' : books
    }
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
    books_list = Book.objects.filter(status=1)
    paginator = Paginator(books_list, 5)
    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    context = {
        'books': books,
        'paginate': True
    }
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
