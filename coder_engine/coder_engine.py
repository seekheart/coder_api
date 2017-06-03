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

    # TODO refactor if else statements
    def get_one(self, lookup: str) -> dict:
        """
        Find one method for a given collection

        Args:
            lookup: a unique term to search a collection for specific document

        Returns:
             A json document matching the lookup or an empty json if no match
        """

        if not lookup:
            raise ValueError('Lookup cannot be Null!')
        document = {}

        if self.selected_collection == 'users':
            document = {'username': lookup}
        elif self.selected_collection == 'languages':
            document = {'name': lookup}
        return self.db.find_one(document)

    def get_all(self):
        """
        A method to get all documents in the collection

        Returns:
            collection of documents

        """

        return [doc for doc in self.db.find()]

    def add_one(self, lookup, data):
        """
        A method to add a new document to the collection

        Args:
            lookup: (str) - a string that is unique for look ups
            data: (list of str) - data to be entered for this look up

        Returns:
            None

        """

        document = {}

        if self.selected_collection == 'users':
            document = {'username': lookup, 'languages': data}
        elif self.selected_collection == 'languages':
            document = {'name': lookup, 'users': data}
        self.db.insert_one(document)

    def delete_one(self, lookup):
        """
        A method to delete a user from the collection

        Args:
            lookup: (str) lookup term that is unique to delete on

        Returns:
            None

        """

        document = {}

        if self.selected_collection == 'users':
            document = {'username': lookup}
        elif self.selected_collection == '':
            document = {'name': lookup}
        self.db.delete_one(document)

    def update_one(self, lookup, field):
        """
        A method to update a user in collection
        Args:
            lookup: (str) - lookup term
            field: (dict) - field to edit in collection document

        Returns:
            None

        """

        document = {}

        if self.selected_collection == 'users':
            document = {'username': lookup}
        elif self.selected_collection == 'languages':
            document = {'name': lookup}
        self.db.update_one(document, {'$set': field})
