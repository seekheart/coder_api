import unittest

from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        """Setup method for spinning up a test instance of app"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.app.testing = True
        self.dummy_name = 'dummy'
        self.dummy_user = {'username': 'dummy', 'languages': ['testLang']}
        self.dummy_lang = {'name': 'dummy', 'users': ['No one']}

    def tearDown(self):
        """Teardown method to cleanup after each test"""
        self.app.delete('/users/dummy')
        self.app.delete('/languages/dummy')

    def test_home(self):
        """Unit test for home"""
        result = self.app.get('/')
        self.assertEquals(result.status_code, 200)

    def test_users(self):
        """Unit test for getting all users"""
        result = self.app.get('/users')
        self.assertEquals(result.status_code, 200)

    def test_get_single_user(self):
        """Unit test for getting a user"""
        result = self.app.get('/users/seekheart')
        self.assertEquals(result.status_code, 200)

    def test_post_single_user(self):
        """Unit test for adding users"""
        result = self.app.post('/users', data=self.dummy_user)
        self.assertEquals(result.status_code, 201)

    def test_post_bad_user(self):
        """Unit test for adding an existing user"""

        bad_user = {'usr': self.dummy_name, 'lang': 'x'}
        result = self.app.post('/users', data=bad_user)
        self.assertEquals(result.status_code, 400)

    def test_post_duplicate_user(self):
        """Unit test for adding a duplicate user"""

        duplicate = {"username": "seekheart",
                     "languages": ["js", "perl", "python"]
                     }
        result = self.app.post('/users', data=duplicate)

        self.assertEquals(result.status_code, 409)

    def test_patch_single_user(self):
        """Unit test for editing a user"""

        self.app.post('/users', data=self.dummy_user)
        result = self.app.patch('/users/dummy', data=self.dummy_user)
        self.assertEquals(result.status_code, 204)
