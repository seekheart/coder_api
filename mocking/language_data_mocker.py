"""
Coding Language Data Mocker
Mike Tung
"""

import json

test_data = [
    {
        'name': 'python',
        'users': ['seekheart', 'foo', 'user2', 'test']
    },
    {
        'name': 'javascript',
        'users': ['seekheart', 'foobar']
    }
]

with open('test_data_lang.json', 'w') as out:
    json.dump(test_data, out, indent=2)
