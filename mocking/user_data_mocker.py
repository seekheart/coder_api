"""
A json fake data generator
Mike Tung
"""

"""
[{
  username: "seekheart",
  languages: [
               'python', 'perl', 'angular'
             ]
},
{
  username: "sam",
  languages: [
               'python', 'c++', 'rust'
             ]
}]
"""

import json

test_data = [
    {
        'username': 'seekheart',
        'languages': ['python', 'angular', 'perl']
    },
    {
        'username': 'PrimitiveDerivative',
        'languages': ['java', 'c', 'c++']
    },
    {
        'username': 'Samoxive',
        'languages': ['python', 'c', 'java']
    },
    {
        'username': 'Nelthorim',
        'languages': ['python', 'haskell', 'java']
    }
]

with open('test_data.json', 'w') as out:
    json.dump(test_data, out, indent=4)
