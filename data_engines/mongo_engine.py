"""
Base class for all mongodb data engines
Mike Tung
"""

import pymongo

import settings


class MongoEngine:
    def __init__(self, collection_name: str) -> None:
        """Constructor for mongodb connection

        Args:
            collection_name: name of collection to operate on
        """

        self._host = settings.MONGO_HOST
        self._port = settings.MONGO_PORT
        self._db_name = settings.MONGO_DB
        self.document = {}
        self._lookup_doc_template = ''
        try:
            self.db = pymongo.MongoClient(self._host, self._port)[self._db_name]
            self.db = self.db.get_collection(collection_name)
        except ConnectionError:
            print('Error connecting to database!')


    def get_one(self, lookup: str) -> dict:
        """
        Find one method for document in collection

        Args:
            lookup: a term for looking up a document that is unique

        Returns:
             A json document matching the lookup or an empty json if no match
        """

        self.document[self._lookup_doc_template] = lookup
        return self.db.find_one(self.document)

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
        except ValueError:
            return False
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

        self.document[self._lookup_doc_template] = lookup

        self.db.delete_one(self.document)

    def update_one(self, lookup: str, field: dict) -> None:
        """
        A method to update a user in collection

        Args:
            lookup: lookup term
            field: field to edit in collection document

        Returns:
            None

        """

        self.document[self._lookup_doc_template] = lookup
        self.db.update_one(self.document, {'$set': field})
