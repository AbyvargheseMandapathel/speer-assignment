from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class TestApi(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', email='testuser1@gmail.com', password='123')
        self.client = APIClient()
        self.token = None

    def test_user_signup(self):
        signup_data = {'username': 'newuser', 'email': 'newuser@gmail.com', 'password': 'newpassword'}
        response = self.client.post('/api/auth/signup', signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login(self):
        login_data = {'username': 'testuser1', 'password': '123'}
        response = self.client.post('/api/auth/login', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.token = response.data['token']

    def test_create_and_get_notes(self):
        self.test_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Create a note
        note_data = {'title': 'Test Note', 'content': 'This is a test note.'}
        create_response = self.client.post('/api/notes', note_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Get the list of notes
        get_response = self.client.get('/api/notes')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_update_and_delete_note(self):
        self.test_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Create
        note_data = {'title': 'Test Note', 'content': 'This is a test note.'}
        create_response = self.client.post('/api/notes', note_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Update 
        update_data = {'title': 'Updated Note', 'content': 'This note has been updated.'}
        update_response = self.client.put(f'/api/notes/{create_response.data["id"]}', update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        # Delete 
        delete_response = self.client.delete(f'/api/notes/{create_response.data["id"]}')
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)

    def test_share_note_and_get_shared_notes(self):
        self.test_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Create  note
        note_data = {'title': 'Test Note', 'content': 'This is a test note.'}
        create_response = self.client.post('/api/notes', note_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Share  note
        share_data = {'user_id': self.user.id}
        share_response = self.client.post(f'/api/notes/{create_response.data["id"]}/share/', share_data, format='json')
        self.assertEqual(share_response.status_code, status.HTTP_200_OK)

        # Get shared notes
        shared_notes_response = self.client.get('/api/shared-notes/')
        self.assertEqual(shared_notes_response.status_code, status.HTTP_200_OK)

    def test_search_notes(self):
        self.test_user_login()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Create note
        note_data = {'title': 'Searchable Note', 'content': 'This note is searchable.'}
        create_response = self.client.post('/api/notes', note_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Search 
        search_query = {'q': 'searchable'}
        search_response = self.client.get('/api/search/', search_query, format='json')
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
