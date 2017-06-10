"""
Programming language Engine
Mike Tung
"""

import pymongo

import data_engines.mongo_engine as mongo_engine


class LanguageEngine(mongo_engine.MongoEngine):
    def __init__(self):
        """Constructor method for language engine"""

        super(LanguageEngine, self).__init__('languages')
        self._lookup_doc_template = ['name']

    def get_one(self, lookup: str) -> dict:
        """
        Find one method for a language in the database

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
        except ValueError:
            return False
        except pymongo.errors.DuplicateKeyError:
            return False

        return True

    def delete_one(self, lookup: str) -> None:
        """
        A method to delete a language from the collection

        Args:
            lookup: lookup term that is unique to delete on

        Returns:
            None

        """

        document = dict(zip(self._lookup_doc_template, [lookup]))

        self.db.delete_one(document)

    def update_one(self, lookup: str, field: dict) -> None:
        """
        A method to update a language in collection

        Args:
            lookup: lookup term
            field: field to edit in collection document

        Returns:
            None

        """

        document = dict(zip(self._lookup_doc_template, [lookup]))
        self.db.update_one(document, {'$set': field})
