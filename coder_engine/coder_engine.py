"""
Mongo database engine
Mike Tung
"""

import pymongo


class CoderEngine:
    def __init__(self, host, port, db_name, collection_name):
        """
        Constructor method for an engine to connect to mongo

        Args:
        host - (str) host for the database usually localhost or some ip
        port - (int) port number to connect/listen on usually 27017
        db_name - (str) name of db to connect to on mongo
        collection_name (str) - name of mongo collection to query on
        """

        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name

        self.client = pymongo.MongoClient(self.host, self.port)

        try:
            self.db = self.client[self.db_name].get_collection(self.collection_name)
        except:
            print('Error unable to connect to {} in {}'.format(collection_name, db_name))

    def get_one(self, lookup):
        """
        A find one method to get a specific document of a collection

        Args:
        lookup - (str) a unique term to identify a single document

        Returns:
        json document
        """

        if not lookup:
            raise ValueError('Lookup cannot be Null!')
        document = {}

        if self.collection_name == 'users':
            document = {'username': lookup}
        elif self.collection_name == 'languages':
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

        if self.collection_name == 'users':
            document = {'username': lookup, 'languages': data}
        elif self.collection_name == 'languages':
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

        if self.collection_name == 'users':
            document = {'username': lookup}
        elif self.collection_name == '':
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

        if self.collection_name == 'users':
            document = {'username': lookup}
        elif self.collection_name == 'languages':
            document = {'name': lookup}
        self.db.update_one(document, {'$set': field})
