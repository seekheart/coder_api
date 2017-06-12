"""
Programming language Engine
Mike Tung
"""

import data_engines


class LanguageEngine(data_engines.MongoEngine):
    def __init__(self):
        """Constructor method for language engine"""

        super(LanguageEngine, self).__init__('languages')
        self._lookup_doc_template = 'name'
        self.document = {}
