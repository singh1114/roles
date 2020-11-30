from django.contrib.auth.models import Group, User
from django.test import Client,  TestCase

from base.models import ActionLogModel

from tweets.models import Tweet


class TweetTests(TestCase):
    def setUp(self):
        Group.objects.create(name='USER')
        Group.objects.create(name='ADMIN')
        Group.objects.create(name='SUPERADMIN')

    def test_tweet_is_created_by_normal_user(self):
        c = Client()
        response = c.post('/users/signup/',
                          {'username': 'username', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertEqual(response.json()['username'], 'username')
        self.assertIsNotNone(response.json()['access'])
        self.assertEqual(response.json()['group'], 'USER')
        token = response.json()['access']

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        c.post('/tweets/my/', data={'text': 'First Tweet'},
               content_type='application/json', **header)
        response = c.get('/tweets/my/', content_type='application/json', **header)
        self.assertEqual(response.json()[0]['text'], 'First Tweet')
        self.assertIsNotNone(response.json()[0]['id'])
        self.assertIsNotNone(response.json()[0]['created_at'])

    def test_tweet_is_deleted_by_normal_user(self):
        c = Client()
        response = c.post('/users/signup/',
                          {'username': 'username', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertEqual(response.json()['username'], 'username')
        self.assertIsNotNone(response.json()['access'])
        self.assertEqual(response.json()['group'], 'USER')
        token = response.json()['access']

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        c.post('/tweets/my/', data={'text': 'First Tweet'},
               content_type='application/json', **header)
        response = c.get('/tweets/my/', content_type='application/json', **header)
        tweet_id = response.json()[0]['id']
        response = c.delete('/tweets/my/' + str(tweet_id) + '/',
                            content_type='application/json', **header)
        self.assertEqual(response.json()['message'], 'Deleted Successfully')
        self.assertEqual(ActionLogModel.objects.all().count(), 4)

    def test_read_logs(self):
        user = User.objects.create_user(username='username1', password='pass')
        group = Group.objects.get(name='SUPERADMIN')
        user.groups.add(group)
        c = Client()
        response = c.post('/users/api/token/',
                          {'username': 'username1', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertIsNotNone(response.json()['access'])
        token = response.json()['access']

        # create some logs
        self.test_tweet_is_deleted_by_normal_user()

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = c.get('/tweets/logs/', content_type='application/json', **header)
        self.assertEqual(response.json()[0]['user'], 'username')
        self.assertEqual(response.json()[0]['log_type'], 2)
        self.assertEqual(response.json()[0]['action'], 1)
        self.assertIsNotNone(response.json()[0]['created_at'])
        self.assertEqual(ActionLogModel.objects.all().count(), 5)

    def test_admin_normal_user_tweet_get(self):
        user = User.objects.create_user(username='username1', password='pass')
        group = Group.objects.get(name='ADMIN')
        user.groups.add(group)
        c = Client()
        response = c.post('/users/api/token/',
                          {'username': 'username1', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertIsNotNone(response.json()['access'])
        token = response.json()['access']

        # create some logs
        self.test_tweet_is_deleted_by_normal_user()

        user = User.objects.get(username='username')

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = c.get('/tweets/user/' + str(user.id) + '/',
                         content_type='application/json', **header)
        self.assertEqual(response.json()[0]['text'], 'First Tweet')
        self.assertEqual(response.json()[0]['status'], 3)
        self.assertEqual(response.json()[0]['updated_text'], '')
        self.assertIsNotNone(response.json()[0]['created_at'])
        self.assertEqual(ActionLogModel.objects.all().count(), 5)

    def test_admin_normal_user_tweet_create(self):
        user = User.objects.create_user(username='username1', password='pass')
        group = Group.objects.get(name='ADMIN')
        user.groups.add(group)
        c = Client()
        response = c.post('/users/api/token/',
                          {'username': 'username1', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertIsNotNone(response.json()['access'])
        token = response.json()['access']

        # create some logs
        self.test_tweet_is_deleted_by_normal_user()

        user = User.objects.get(username='username')

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = c.post('/tweets/user/' + str(user.id) + '/', {'text': 'text'},
                         content_type='application/json', **header)
        self.assertEqual(response.json()['message'], 'Added successfully')
        tweet = Tweet.objects.get(text='text')
        self.assertEqual(tweet.status, 1)
        self.assertEqual(ActionLogModel.objects.all().count(), 5)

    def test_admin_normal_user_tweet_update(self):
        user = User.objects.create_user(username='username2', password='pass')
        group = Group.objects.get(name='ADMIN')
        user.groups.add(group)
        c = Client()
        response = c.post('/users/api/token/',
                          {'username': 'username2', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertIsNotNone(response.json()['access'])
        token = response.json()['access']

        # create some logs
        self.test_admin_normal_user_tweet_create()

        tweet = Tweet.objects.get(text='First Tweet')

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = c.put('/tweets/user/initiate/' + str(tweet.id) + '/', {'text': 'text'},
                         content_type='application/json', **header)
        self.assertEqual(response.json()['message'], 'Updated successfully')
        tweet = Tweet.objects.get(text='First Tweet')
        self.assertEqual(tweet.status, 5)
        self.assertEqual(tweet.updated_text, 'text')
        self.assertEqual(ActionLogModel.objects.all().count(), 6)

    def test_admin_normal_user_tweet_delete(self):
        user = User.objects.create_user(username='username2', password='pass')
        group = Group.objects.get(name='ADMIN')
        user.groups.add(group)
        c = Client()
        response = c.post('/users/api/token/',
                          {'username': 'username2', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertIsNotNone(response.json()['access'])
        token = response.json()['access']

        # create some logs
        self.test_admin_normal_user_tweet_create()

        tweet = Tweet.objects.get(text='First Tweet')

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = c.delete('/tweets/user/initiate/' + str(tweet.id) + '/',
                            content_type='application/json', **header)
        self.assertEqual(response.json()['message'], 'Deleted Successfully')
        tweet = Tweet.objects.get(text='First Tweet')
        self.assertEqual(tweet.status, 4)
        self.assertEqual(ActionLogModel.objects.all().count(), 6)

    def test_check_awaiting_approval(self):
        user = User.objects.create_user(username='username3', password='pass')
        group = Group.objects.get(name='SUPERADMIN')
        user.groups.add(group)
        c = Client()
        response = c.post('/users/api/token/',
                          {'username': 'username3', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertIsNotNone(response.json()['access'])
        token = response.json()['access']

        # create some logs
        self.test_admin_normal_user_tweet_delete()

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = c.get('/tweets/approve/', content_type='application/json', **header)
        self.assertEqual(response.json()[0]['text'], 'text')
        self.assertEqual(response.json()[0]['status'], 1)
        self.assertEqual(response.json()[0]['updated_text'], '')
        self.assertIsNotNone(response.json()[0]['created_at'])
        self.assertEqual(ActionLogModel.objects.all().count(), 6)

    def test_check_awaiting_approval(self):
        user = User.objects.create_user(username='username3', password='pass')
        group = Group.objects.get(name='SUPERADMIN')
        user.groups.add(group)
        c = Client()
        response = c.post('/users/api/token/',
                          {'username': 'username3', 'password': 'pass'},
                          HTTP_ACCEPT='application/json')
        self.assertIsNotNone(response.json()['access'])
        token = response.json()['access']

        # create some logs
        self.test_admin_normal_user_tweet_delete()

        header = {'HTTP_AUTHORIZATION': 'Bearer ' + token}
        response = c.get('/tweets/approve/', content_type='application/json',
                         **header)
        tweet_id = response.json()[0]['id']
        response = c.get('/tweets/approve/' + str(tweet_id) + '/',
                         content_type='application/json', **header)
        self.assertEqual(response.json()['message'], 'Request Approved')
        tweet = Tweet.objects.get(id=tweet_id)
        self.assertEqual(tweet.status, 2)
        self.assertEqual(ActionLogModel.objects.all().count(), 7)
