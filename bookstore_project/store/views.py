from django.shortcuts import render
from store.models import Book, Author, Booking, Profile
from .forms import ParagraphErrorList, RegisterForm, ConnexionForm, UserForm, ProfileForm
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from store.choices import * 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def account(request):
    return render(request, 'store/account.html', locals())

def deconnexion(request):
    logout(request)
    return HttpResponseRedirect(reverse('store:connexion'))

def connexion(request):
    if request.user.is_authenticated:
        return render(request, 'store/connexion.html', locals())

    error = False
    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return render(request, 'store/connexion.html', {   
                    'form': form,
                    'error_message': error
                 }) 
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'store/connexion.html', {
        'form': form,
        'error_message': error
    })

def user_register(request):
    #if the user is logged in, redirects him to user_account view
    if request.user.is_authenticated:
        render(request, 'store/account.html', locals())

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
                        try:
                            user = User.objects.create_user(username, email, password)
                            profile = Profile.objects.create(user=user)
                        except Exception as e:
                            return render(request, 'store/register.html', {
                            'form': form,
                            'error_message': str(e)
                           })

                        try:
                            user.save()
                            profile.save()
                        except:
                            return render(request, 'store/register.html', {
                            'form': form,
                            'error_message': "error in save user!"
                           })       

                        # Login the user
                        try:
                            login(request, user)
                        except:
                            return render(request, 'store/register.html', {
                            'form': form,
                            'error_message': "error in login user !"
                           })
                        return render(request, 'store/register.html', {
                            'form': form,
                            'error_message': "Inscription réussie, vous pouvez désormais réserver les livres disponibles !"
                           })
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
    books = Book.objects.filter(status=AVAILABLE).order_by('-created_at')[:12]
    context = {
    'books' : books
    }
    return render(request, 'store/index.html', context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    context = {
        'book' : book,
        'book_title': book.title,
    }
    error = False
    if request.method == 'POST':
        try:
            with transaction.atomic():
                #get the user name
                if request.user.is_authenticated:
                    username = request.user.username
                    #create booking
                    booking = Booking.objects.create(user=request.user, book=book)
                    #change the status of book on borrowed
                    book.status = BORROWED
                    book.save()
                    #return render(request, 'store/detail.html', context)
                    return render(request, 'store/booking_success.html', context)
                    
        except IntegrityError as e:
            print(e)
            error = True
            message = "Une erreur interne est apparue. Merci de recommencer votre requête."
            context = {
                'book' : book,
                'message': message,
                'error': error
            }
            return render(request, 'store/detail.html', context)

    return render(request, 'store/detail.html', context)

def listing(request):
    books_list = Book.objects.filter(status=AVAILABLE)
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
        books = Book.objects.filter(status=AVAILABLE)
    else:
        # title contains the query is and query is not sensitive to case.
        books = Book.objects.filter(title__icontains=query, status=AVAILABLE)
    if not books.exists():
        books = Book.objects.filter(authors__name__icontains=query, status=AVAILABLE)
    title = "Résultats pour la requête %s"%query
    context = {
        'books': books,
        'title': title
    }
    return render(request, 'store/search.html', context)

@login_required
@transaction.atomic
def update_profile(request):
    bookings = Booking.objects.all()
    #get user's bookings
    books= []
    for e in bookings:
        if (e.user.username == request.user.username):
            books.append(e.book)
    context = {
        'books': books,
        'username' : request.user.username,
        'email' : request.user.email,
        'web_site' : request.user.profile.web_site,
        'signature' : request.user.profile.signature,
        'avatar' : request.user.profile.avatar
    }
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form['username']
            email = user_form['email']
            context['user_form'] = user_form
            context['profile_form'] = profile_form
            try:
                if User.objects.filter(username=username).exists():
                    context['message'] = "Nom d'utilisateur existe dans la base de donnée !"
                    return render(request, 'store/account.html', context)
                elif User.objects.filter(email=email).exists():
                    context['message'] = 'Email existe dans la base de donnée !'
                    return render(request, 'store/account.html', context)
                else:
                    user_form.save()
                    profile_form.save()
                    #update context
                    context = {
                        'books': books,
                        'username' : request.user.username,
                        'email' : request.user.email,
                        'web_site' : request.user.profile.web_site,
                        'signature' : request.user.profile.signature,
                        'avatar' : request.user.profile.avatar,
                    }
                    context['user_form'] = user_form
                    context['profile_form'] = profile_form
                    context['message'] = 'Votre profil est mis à jour !'
                    return render(request, 'store/account.html', context)
            except:
                context['message'] = 'Une erreur interne est apparue. Merci de recommencer votre requête.'
                return render(request, 'store/account.html', context)
        else:
            pass
            #print('profile_form is not valid !')

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    return render(request, 'store/account.html', context)