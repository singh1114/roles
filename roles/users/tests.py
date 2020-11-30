from django.contrib.auth.models import Group
from django.test import Client, TestCase


class TestUser(TestCase):
    def setUp(self):
        Group.objects.create(name='USER')

    def test_normal_user_signup(self):
        c = Client()
        response = c.post('/users/signup/', {'username': 'username', 'password': 'pass'},
               HTTP_ACCEPT='application/json')
        self.assertEqual(response.json()['username'], 'username')
        self.assertIsNotNone(response.json()['access'])
        self.assertEqual(response.json()['group'], 'USER')

    # Add some failing tests
