from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Permission
from graphene.test import Client
from visibility.schema import schema


class QueryTests(TestCase):
    def setUp(self):
        self.user_with_permission = User.objects.create_user(username='admin', password='admin123')
        self.user_without_permission = User.objects.create_user(username='test_user', password='test123')

        permission = Permission.objects.get(codename='view_user')
        self.user_with_permission.user_permissions.add(permission)

        self.factory = RequestFactory()
        self.client = Client(schema)

    def test_user_query_with_permission(self):
        """
        Test the user query with the `auth.view_user` permission.
        """
        query = '''
        {
            user(id: 1) {
                username
                email
            }
        }
        '''
        request = self.factory.get('/')
        request.user = self.user_with_permission

        response = self.client.execute(query, context_value=request)
        self.assertIsNone(response.get('errors'))  # No errors expected
        data = response.get('data').get('user')
        self.assertEqual(data['username'], 'admin')

    def test_user_query_without_permission(self):
        """
        Test the user query without the `auth.view_user` permission.
        """
        query = '''
        {
            user(id: 1) {
                username
                email
            }
        }
        '''
        request = self.factory.get('/')
        request.user = self.user_without_permission

        response = self.client.execute(query, context_value=request)
        errors = response.get('errors')
        self.assertIsNotNone(errors)  # Expect an error
        self.assertIn("Cannot query field", errors[0]['message'])
