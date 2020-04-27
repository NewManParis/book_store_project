from django.db import models
from django.utils import timezone
from enum import Enum 

# Create your models here.

class Author(models.Model):
	name = models.CharField('name', max_length=200, unique=True)

	class Meta:
		verbose_name = "author"

	def __str__(self):
		return self.name


class Book(models.Model):

	class STATUS(Enum):
		available = (1, 'Available to borrow')
		borrowed = (2, 'Borrowed by someone')
		archived = (3, 'Archived - not available anymore')

		@classmethod
		def get_value(cls, member):
			return member.value[0]

	class CATEGORY(Enum):
		other = ('other', 'Other')
		astronomy = ('astronomy', 'Astronomy')
		biology = ('biology', 'Biology')
		chemistry = ('chemistry', 'Chemistry')
		history = ('history', 'History')
		medecine = ('biology', 'Biology')
		mathematics = ('mathematics', 'Mathematics')
		psychology = ('psychology', 'Psychology')

		@classmethod
		def get_value(cls, member):
			return cls[member].value[0]

	reference = models.IntegerField('reference', null=True)
	created_at = models.DateTimeField('creation date',  auto_now_add=True)
	status = models.CharField('status', max_length=200, choices=[x.value for x in STATUS], default=STATUS.get_value(STATUS.available))
	title = models.CharField('title', max_length=200)
	category = models.CharField('category', max_length=200, choices=[x.value for x in CATEGORY], default=CATEGORY.get_value('other'))
	picture = models.TextField('picture URL') 
	price = models.IntegerField('price', null=True)
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


