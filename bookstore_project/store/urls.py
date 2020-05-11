from django.urls import path
from . import views


urlpatterns = [
    path('<book_id>/', views.detail, name='detail'),
    path('', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('login', views.login, name='login'),
    path('register', views.user_register, name='user_register'),

]
