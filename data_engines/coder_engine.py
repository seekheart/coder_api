"""
Coder Database Engine
Mike Tung
"""

import data_engines


class CoderEngine(data_engines.MongoEngine):
    def __init__(self):
        """
        Constructor method for a Coder Engine"""

        super(CoderEngine, self).__init__('users')

        self._lookup_doc_template = 'username'
        self.document = {}
