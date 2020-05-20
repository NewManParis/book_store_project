from django.urls import path
from . import views


urlpatterns = [
    path('<book_id>/', views.detail, name='detail'),
    path('', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('login', views.login, name='login'),
    path('register', views.user_register, name='user_register'),
    path('connexion', views.connexion, name='connexion'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('account', views.update_profile, name='account'),
]
