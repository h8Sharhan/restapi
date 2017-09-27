import base64
import json
import unittest

from app import app


class AppTestCase(unittest.TestCase):

    def test_random_word(self):
        tester = app.test_client(self)

        response = tester.get('/api/v1.0/random_word')
        self.assertEqual(response.status_code, 401)

        response = tester.get('/api/v1.0/random_word',
                              headers={'Authorization': 'Basic %s' % base64.b64encode(bytes("user:qwe123"))})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')

    def test_wiki(self):
        tester = app.test_client(self)

        response = tester.get('/api/v1.0/wiki/Ninja')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')

        response = tester.get('/api/v1.0/wiki/Ninjasaur')
        self.assertEqual(response.status_code, 404)

    def test_most_popular(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1.0/wiki/most_popular/3')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(len(data.get('result')), 3)

    def test_joke(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1.0/joke')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')

        response = tester.get('/api/v1.0/joke?firstName=Vasili')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')

        response = tester.get('/api/v1.0/joke?lastName=Dou')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')

        response = tester.get('/api/v1.0/joke?firstName=Vasili&lastName=Dou')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'success')


if __name__ == '__main__':
    unittest.main()