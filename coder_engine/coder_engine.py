"""
Mongo database engine
Mike Tung
"""

import pymongo


class CoderEngine:
    def __init__(self, host: str, port: int, db_name: str, collections: dict,
                 selected_collection: str = 'users'):
        """
        Constructor method for a Mongo Database Coder Engine

        Args:
            host: hostname for mongo to connect on
            port: port mongo is listening on
            db_name: name of database in mongo
            collections: collections available in the database
            selected_collection: collection currently set to be used by engine
            defaults to users

        Returns:
            Instance of the coder engine
        """

        self._host = host
        self._port = port
        self.db_name = db_name
        self.collections = collections
        self.selected_collection = selected_collection
        self._client = pymongo.MongoClient(host, port)

        try:
            self.db = self._client[self.db_name] \
                .get_collection(selected_collection)
        except ConnectionError as e:
            print('Error unable to connect to {} in {}'.format(
                selected_collection, db_name))

    def _get_document_keys(self) -> list:
        """
        Private method to make documents for fetching/adding

        Returns:
            list of document key(s) depending on search flag

        """

        document_keys = {
            'users': ['username', 'languages'],
            'languages': ['name', 'users']
        }

        document = []

        try:
            document = document_keys[self.selected_collection]
        except KeyError as e:
            print(e)

        return document

    def get_one(self, lookup: str) -> dict:
        """
        Find one method for a given collection

        Args:
            lookup: a unique term to search a collection for specific document

        Returns:
             A json document matching the lookup or an empty json if no match
        """

        doc_key = self._get_document_keys().copy()
        del doc_key[-1]
        doc_val = [lookup]
        document = dict(zip(doc_key, doc_val))

        return self.db.find_one(document)

    def get_all(self) -> list:
        """
        A method to get all documents in the collection

        Returns:
            collection of documents

        """

        return [doc for doc in self.db.find()]

    def add_one(self, lookup: str, data: dict) -> None:
        """
        A method to add a new document to the collection

        Args:
            lookup: A unique key to search on
            data: data to be entered for this look up

        Returns:
            None

        """

        if lookup is None:
            raise TypeError('Lookup must be string!')
        if self.get_one(lookup):
            raise ValueError('Error {} already exists'.format(lookup))

        doc_key = self._get_document_keys()
        doc_val = [lookup, data]
        document = dict(zip(doc_key, doc_val))

        self.db.insert_one(document)

    def delete_one(self, lookup: str) -> None:
        """
        A method to delete a user from the collection

        Args:
            lookup: lookup term that is unique to delete on

        Returns:
            None

        """

        doc_key = self._get_document_keys()
        doc_val = [lookup]
        document = dict(zip(doc_key, doc_val))

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

        doc_key = self._get_document_keys()
        doc_val = [lookup]
        document = dict(zip(doc_key, doc_val))
        self.db.update_one(document, {'$set': field})
