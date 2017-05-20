"""
Mongo database engine
Mike Tung
"""

import pymongo


class CoderEngine:
    def __init__(self, host, port, db_name, collection_name):
        """
        Constructor method for an engine to connect to mongo

        :argument
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

    def get_user(self, user_name):
        """
        A find one method to get all languages known by user queried

        Args:
        user_name - (string) user to be queried for

        Returns:
        json of user with programming languages known
        """

        return self.db.find_one({'username': user_name})

    def get_all_users(self):
        """
        A method to get all user data in a collection

        Returns:
            list of dicts of users

        """

        return [user for user in self.db.find()]

    def add_user(self, user_name, languages):
        """
        A method to add a new user and his/her known programming languages

        Args:
            user_name: (str) - user name
            languages: (list of str) - languages known by user

        Returns:
            None

        """

        document = {'username': user_name, 'languages': languages}
        self.db.insert_one(document)

    def delete_user(self, user_name):
        """
        A method to delete a user from the collection

        Args:
            user_name: (str) name of user to be deleted

        Returns:
            None

        """

        self.db.delete_one({'username': user_name})

    def update_user(self, user_name, field):
        """
        A method to update a user in collection
        Args:
            user_name: (str) - username to look up
            field: (dict) - field to edit in user collection

        Returns:
            None

        """

        print(field)

        self.db.update_one({'username': user_name}, {'$set': field})
