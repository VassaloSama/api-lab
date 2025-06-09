import unittest
from api.index import app
from flask_jwt_extended import decode_token
import json

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'API is running', response.data)

    def test_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data['items'], list)

    def test_login_and_token(self):
        response = self.client.post('/login')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

        
        token = data['access_token']

        with app.app_context():
            decoded = decode_token(token)
            self.assertEqual(decoded['sub'], 'user')

    def test_protected_route_without_token(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_with_token(self):
        # Primeiro, gera um token
        login_response = self.client.post('/login')
        token = json.loads(login_response.data)['access_token']

        # Usa o token para acessar rota protegida
        response = self.client.get(
            '/protected',
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Protected route', response.data)

if __name__ == '__main__':
    unittest.main()
