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

        try:
            self.db = pymongo.MongoClient(self._host, self._port)[self._db_name]
            self.db = self.db.get_collection(collection_name)
        except ConnectionError:
            print('Error connecting to database!')

    def get_one(self, lookup: str) -> dict:
        pass

    def get_all(self) -> list:
        pass

    def add_one(self, data: dict) -> bool:
        pass

    def delete_one(self, lookup: str) -> None:
        pass

    def update_one(self, lookup: str, field: dict) -> None:
        pass
