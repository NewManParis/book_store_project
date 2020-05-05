from django.test import TestCase
from django.urls import reverse

from .models import Book, Author, User, Booking
from .choices import*


class IndexPageTestCase(TestCase):

    # test that index returns a 200
    # must start with `test`
    def test_index_page(self):
        # you must add a name to index view: name="index"`
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class DetailPageTestCase(TestCase):

    # ran before each test.
    def setUp(self):
        impossible = Book.objects.create(title="Transmission Impossible")
        self.book = Book.objects.get(title='Transmission Impossible')

    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        book_id = self.book.id
        response = self.client.get(reverse('store:detail', args=(book_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the items does not exist
    def test_detail_page_returns_404(self):
        book_id = self.book.id + 1
        response = self.client.get(reverse('store:detail', args=(book_id,)))
        self.assertEqual(response.status_code, 404)

class BookingPageTestCase(TestCase):

    def setUp(self):
        User.objects.create(user_name="Freddie", user_email="fred@queens.forever")
        impossible = Book.objects.create(title="Transmission Impossible")
        journey = Author.objects.create(name="Journey")
        impossible.authors.add(journey)
        self.book = Book.objects.get(title='Transmission Impossible')
        self.user = User.objects.get(user_name='Freddie')

    # test that a new booking is made
    def test_new_booking_is_registered(self):
        old_bookings = Booking.objects.count()
        book_id = self.book.id
        user_name = self.user.user_name
        user_email =  self.user.user_email
        response = self.client.post(reverse('store:detail', args=(book_id,)), {
            'user_name': user_name,
            'user_email': user_email
        })
        new_bookings = Booking.objects.count()
        self.assertEqual(new_bookings, old_bookings + 1)

    # test that a booking belongs to a user
    def test_new_booking_belongs_to_a_user(self):
        book_id = self.book.id
        user_name = self.user.user_name
        user_email =  self.user.user_email
        response = self.client.post(reverse('store:detail', args=(book_id,)), {
            'user_name': user_name,
            'user_email': user_email
        })
        booking = Booking.objects.first()
        self.assertEqual(self.user, booking.user)

    # test that a booking belong to an book
    def test_new_booking_belongs_to_an_book(self):
        book_id = self.book.id
        user_name = self.user.user_name
        user_email =  self.user.user_email
        response = self.client.post(reverse('store:detail', args=(book_id,)), {
            'user_name': user_name,
            'user_email': user_email
        })
        booking = Booking.objects.first()
        self.assertEqual(self.book, booking.book)

    # test that a book is not available after a booking is made
    def test_book_not_available_if_booked(self):
        book_id = self.book.id
        user_name = self.user.user_name
        user_email =  self.user.user_email
        response = self.client.post(reverse('store:detail', args=(book_id,)), {
            'user_name': user_name,
            'user_email': user_email
        })
        # Make the query again, otherwise `available` will still be set at `True`
        self.book.refresh_from_db()
        book_status = BORROWED
        self.assertEqual(self.book.status, BORROWED)