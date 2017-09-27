import base64
import unittest
from json import loads
from mock import patch

import external_api_exceptions
from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client(self)

    def test_random_word(self):
        response = self.client.get('/api/v1.0/random_word')
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/api/v1.0/random_word',
                                   headers={'Authorization': 'Basic %s' % base64.b64encode(bytes("user:qwe123"))})
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        with patch('helper_functions.get_random_word', side_effect=external_api_exceptions.ExternalApiFetchError):
            response = self.client.get('/api/v1.0/random_word',
                                       headers={'Authorization': 'Basic %s' % base64.b64encode(bytes("user:qwe123"))})
            self.assertEqual(response.status_code, 503)

    def test_wiki(self):
        response = self.client.get('/api/v1.0/wiki/Ninja')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = self.client.get('/api/v1.0/wiki/Ninjasaur')
        self.assertEqual(response.status_code, 404)

        with patch('helper_functions.get_wiki_article', side_effect=external_api_exceptions.ExternalApiFetchError):
            response = self.client.get('/api/v1.0/wiki/Ninja')
            self.assertEqual(response.status_code, 503)

    def test_most_popular(self):
        self.client = app.test_client(self)
        response = self.client.get('/api/v1.0/wiki/most_popular/3')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(len(data.get('result')), 3)

    def test_joke(self):
        response = self.client.get('/api/v1.0/joke')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = self.client.get('/api/v1.0/joke?firstName=Vasili')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = self.client.get('/api/v1.0/joke?lastName=Dou')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = self.client.get('/api/v1.0/joke?firstName=Vasili&lastName=Dou')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        with patch('helper_functions.get_chuck_norris_joke',
                   side_effect=external_api_exceptions.ExternalApiFetchError):
            response = self.client.get('/api/v1.0/joke')
            self.assertEqual(response.status_code, 503)


if __name__ == '__main__':
    unittest.main()