from django.db import models
from django.utils import timezone

# Create your models here.

class Author(models.Model):
	name = models.CharField("author's name", max_length = 100)

	class meta:
		pass


class Book(models.Model):
	reference = models.IntegerField("book's reference", default=0)
	created_at = models.DateTimeField("book's creation date")
	available = models.BooleanField("available or not", default=True)
	title = models.CharField("book's title", max_length = 100)
	category = models.CharField("book's category", max_length = 100)
	picture = models.URLField("book's url picture", max_length = 200)
	price = models.IntegerField("book's price", default=0)
	authors = models.ManyToManyField(Author)

	class meta:
		pass

class User(models.Model):
	user_name = models.CharField("user's name", max_length = 100)
	user_email = models.CharField("user's email", max_length = 100)

	class meta:
		pass 

class Booking(models.Model):
	created_at = models.DateTimeField("booking creation date")
	processed = models.BooleanField("is processed ?", default= False)
	book = models.OneToOneField(Book, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class meta:
		pass

