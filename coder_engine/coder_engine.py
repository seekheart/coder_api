"""
Mongo database engine
Mike Tung
"""

import pymongo

class CoderEngine:
    def __init__(self, host: str, port: int, db_name: str):
        """
        Constructor method for a Mongo Database Coder Engine

        Args:
            host: hostname for mongo to connect on
            port: port mongo is listening on
            db_name: name of database in mongo

        Returns:
            Instance of the coder engine
        """

        self._host = host
        self._port = port
        self.db_name = db_name
        self._client = pymongo.MongoClient(host, port)
        self._lookup_doc_template = ['username']
        try:
            self.db = self._client[self.db_name].get_collection('users')
        except ConnectionError:
            print('Error unable to connect to {} in {}'.format(
                'users', db_name))

    def get_one(self, lookup: str) -> dict:
        """
        Find one method for a coder in the database

        Args:
            lookup: a term for looking up a document that is unique

        Returns:
             A json document matching the lookup or an empty json if no match
        """

        document = dict(zip(self._lookup_doc_template, [lookup]))
        return self.db.find_one(document)

    def get_all(self) -> list:
        """
        A method to get all documents in the collection

        Returns:
            collection of documents

        """

        return [doc for doc in self.db.find()]

    def add_one(self, data: dict) -> bool:
        """
        A method to add a new document to the collection

        Args:
            data: data to be entered for this look up

        Returns:
            bool for success or failure of adding new document

        """
        try:
            self.db.insert_one(data)
        except pymongo.errors.DuplicateKeyError:
            return False
        return True

    def delete_one(self, lookup: str) -> None:
        """
        A method to delete a user from the collection

        Args:
            lookup: lookup term that is unique to delete on

        Returns:
            None

        """

        document = dict(zip(self._lookup_doc_template, [lookup]))

        self.db.delete_one(document)

    def update_one(self, lookup: str, field: dict) -> None:
        """
        A method to update a user in collection

        Args:
            lookup: lookup term
            field: field to edit in collection document

        Returns:
            None

        """

        document = dict(zip(self._lookup_doc_template, [lookup]))
        self.db.update_one(document, {'$set': field})
