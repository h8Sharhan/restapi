import base64
import unittest
from json import loads
from mock import patch

import external_api_exceptions
from app import app


class AppTestCase(unittest.TestCase):

    def test_random_word(self):
        tester = app.test_client(self)

        response = tester.get('/api/v1.0/random_word')
        self.assertEqual(response.status_code, 401)

        response = tester.get('/api/v1.0/random_word',
                              headers={'Authorization': 'Basic %s' % base64.b64encode(bytes("user:qwe123"))})
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        with patch('helper_functions.get_random_word') as get_random_word_mock:
            get_random_word_mock.side_effect = external_api_exceptions.ExternalApiFetchError
            response = tester.get('/api/v1.0/random_word',
                                  headers={'Authorization': 'Basic %s' % base64.b64encode(bytes("user:qwe123"))})
            self.assertEqual(response.status_code, 503)

    def test_wiki(self):
        tester = app.test_client(self)

        response = tester.get('/api/v1.0/wiki/Ninja')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = tester.get('/api/v1.0/wiki/Ninjasaur')
        self.assertEqual(response.status_code, 404)

        with patch('helper_functions.get_wiki_article') as get_wiki_article_mock:
            get_wiki_article_mock.side_effect = external_api_exceptions.ExternalApiFetchError
            response = tester.get('/api/v1.0/wiki/Ninja')
            self.assertEqual(response.status_code, 503)

    def test_most_popular(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1.0/wiki/most_popular/3')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(len(data.get('result')), 3)

    def test_joke(self):
        tester = app.test_client(self)

        response = tester.get('/api/v1.0/joke')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = tester.get('/api/v1.0/joke?firstName=Vasili')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = tester.get('/api/v1.0/joke?lastName=Dou')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        response = tester.get('/api/v1.0/joke?firstName=Vasili&lastName=Dou')
        self.assertEqual(response.status_code, 200)
        data = loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertTrue(data.get('result'))

        with patch('helper_functions.get_chuck_norris_joke') as get_chuck_norris_joke_mock:
            get_chuck_norris_joke_mock.side_effect = external_api_exceptions.ExternalApiFetchError
            response = tester.get('/api/v1.0/joke')
            self.assertEqual(response.status_code, 503)

if __name__ == '__main__':
    unittest.main()