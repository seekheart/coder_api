"""
Programming language Engine
Mike Tung
"""

import data_engines.mongo_engine as mongo_engine


class LanguageEngine(mongo_engine.MongoEngine):
    def __init__(self):
        """Constructor method for language engine"""

        super(LanguageEngine, self).__init__('languages')
        self._lookup_doc_template = 'name'
        self.document = {}
