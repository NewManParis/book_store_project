from django.db import models
from django.utils import timezone
from store.choices import * 
# Create your models here.

class Author(models.Model):
	name = models.CharField('name', max_length=200, unique=True)

	class Meta:
		verbose_name = "author"

	def __str__(self):
		return self.name


class Book(models.Model):

	reference = models.IntegerField('reference', null=True)
	created_at = models.DateTimeField('creation date',  auto_now_add=True)
	status = models.IntegerField('status', choices=STATUS_CHOICES, default=AVAILABLE)
	title = models.CharField('title', max_length=200)
	category = models.CharField('category', max_length=200, choices=CATEGORY_CHOICES, default=OTH)
	picture = models.TextField('picture URL')
	price = models.IntegerField('price', null=True)
	release_date = models.IntegerField('release date', null=True)
	language = models.CharField('language', max_length=200)
	authors = models.ManyToManyField(Author, related_name='books', blank=True)

	class Meta:
		verbose_name = "book"

	def __str__(self):
		return self.title


class User(models.Model):
	user_name = models.CharField('contact name', max_length=200)
	user_email = models.EmailField('contact email', max_length=100)

	class Meta:
		verbose_name = "user" 

	def __str__(self):
		return self.user_name


class Booking(models.Model):
	created_at = models.DateTimeField('creation date', auto_now_add=True)
	processed = models.BooleanField('is processed ?', default= False)
	book = models.OneToOneField(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "booking" 

	def __str__(self):
		return self.user.name
