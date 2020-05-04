from django.test import TestCase
from django.urls import reverse

from .models import Book, Author, User, Booking


class IndexPageTestCase(TestCase):

    # test that index returns a 200
    # must start with `test`
    def test_index_page(self):
        # you must add a name to index view: `name="index"`
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)