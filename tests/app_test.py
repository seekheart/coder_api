import base64
import unittest

from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        """Setup method for spinning up a test instance of app"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app.testing = True
        self.authorization = {
            'Authorization': "Basic {user}".format(
                user=base64.b64encode(b"test:asdf").decode("ascii")
            )
        }
        self.dummy_name = 'dummy'
        self.dummy_user = {'username': 'dummy', 'languages': ['testLang']}
        self.dummy_lang = {'name': 'dummy', 'users': ['No one']}

    def tearDown(self):
        """Teardown method to cleanup after each test"""
        self.app.delete('/users/dummy', headers=self.authorization)
        self.app.delete('/languages/dummy', headers=self.authorization)

    # Control test
    def test_home(self):
        """Unit test for home"""
        result = self.app.get('/')
        self.assertEquals(result.status_code, 200)

    # Authorization test
    def test_auth_401(self):
        """Unit test for forbidden access"""
        result = self.app.get('/users')
        self.assertEquals(result.status_code, 401)

    # Users tests
    def test_users(self):
        """Unit test for getting all users"""
        result = self.app.get('/users', headers=self.authorization)
        self.assertEquals(result.status_code, 200)

    def test_get_single_user(self):
        """Unit test for getting a user"""
        result = self.app.get('/users/seekheart', headers=self.authorization)
        self.assertEquals(result.status_code, 200)

    def test_post_single_user(self):
        """Unit test for adding users"""
        result = self.app.post('/users',
                               data=self.dummy_user,
                               headers=self.authorization)
        self.assertEquals(result.status_code, 201)

    def test_post_bad_user(self):
        """Unit test for adding an existing user"""

        bad_user = {'usr': self.dummy_name, 'lang': 'x'}
        result = self.app.post('/users', data=bad_user,
                               headers=self.authorization)
        self.assertEquals(result.status_code, 400)

    def test_post_duplicate_user(self):
        """Unit test for adding a duplicate user"""

        duplicate = {"username": "seekheart",
                     "languages": ["js", "perl", "python"]
                     }
        result = self.app.post('/users', data=duplicate,
                               headers=self.authorization)

        self.assertEquals(result.status_code, 409)

    def test_patch_single_user(self):
        """Unit test for editing a user"""

        self.app.post('/users', data=self.dummy_user,
                      headers=self.authorization)
        result = self.app.patch('/users/dummy', data=self.dummy_user,
                                headers=self.authorization)
        self.assertEquals(result.status_code, 204)

    # Language tests
    def test_languages(self):
        """Unit test for getting all languages"""
        result = self.app.get('/languages', headers=self.authorization)
        self.assertEquals(result.status_code, 200)

    def test_get_single_language(self):
        """Unit test for getting a user"""
        result = self.app.get('/languages/angular', headers=self.authorization)
        self.assertEquals(result.status_code, 200)

    def test_post_single_language(self):
        """Unit test for adding languages"""
        result = self.app.post('/languages',
                               headers=self.authorization,
                               data=self.dummy_lang)
        self.assertEquals(result.status_code, 201)

    def test_post_bad_language(self):
        """Unit test for adding an existing language"""

        bad_language = {'usr': self.dummy_name, 'lang': 'x'}
        result = self.app.post('/languages', data=bad_language,
                               headers=self.authorization)
        self.assertEquals(result.status_code, 400)

    def test_post_duplicate_language(self):
        """Unit test for adding a duplicate language"""

        duplicate = {
            "name": "javascript",
            "users": [
                "seekheart",
                "foobar"
            ]
        }
        result = self.app.post('/languages', data=duplicate,
                               headers=self.authorization)

        self.assertEquals(result.status_code, 409)

    def test_patch_single_language(self):
        """Unit test for editing a language"""

        self.app.post('/languages', data=self.dummy_lang,
                      headers=self.authorization)
        result = self.app.patch('/languages/dummy', data=self.dummy_lang,
                                headers=self.authorization)
        self.assertEquals(result.status_code, 204)
