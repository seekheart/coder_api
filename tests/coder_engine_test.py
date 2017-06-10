import unittest

import data_engines.coder_engine as coder_engine


class CoderEngineTest(unittest.TestCase):
    def setUp(self):
        """Setup method for each test"""
        self.engine = coder_engine.CoderEngine()
        self.dummy_user = {'username': 'testUser', 'languages': ['testLang']}
        self.lookup = 'testUser'

    def tearDown(self):
        """Destroy method for cleaning up after each test"""
        self.engine.delete_one(self.lookup)
        self.engine = None

    def test_get_all(self):
        """Unit Test for testing getting all documents in a collection"""

        self.assertTrue(len(self.engine.get_all()) > 0)

    def test_get_one(self):
        """Unit Test for getting a single document"""

        self.assertNotEquals(self.engine.get_one('seekheart'), None)

    def test_add_one(self):
        """Unit test for adding a new document"""

        self.assertTrue(self.engine.add_one(self.dummy_user))

    def test_add_one_exists(self):
        """Unit test for testing adding a new document when it already exists"""
        self.engine.add_one(self.dummy_user)
        self.assertRaises(Exception, self.engine.add_one(self.dummy_user))

    def test_delete_one(self):
        """Unit test for deleting a single document from the collection"""

        self.engine.add_one(self.dummy_user)
        self.engine.delete_one(self.lookup)
        self.assertIsNone(self.engine.get_one(self.lookup))

    def test_update_one(self):
        """Unit test for updating a document"""

        self.engine.add_one(self.dummy_user)

        self.engine.update_one(self.lookup, {'username': 'foobar'})

        data = self.engine.get_one(self.lookup)

        self.assertIsNone(data)

        self.engine.delete_one('foobar')



if __name__ == '__main__':
    unittest.main()
