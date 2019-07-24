from tinydb import TinyDB, Query
import os
import time
import pprint

dirname = os.path.dirname(__file__)
db = TinyDB(f"{dirname}/../data/db.json")
DEFAUT_FREQUENCY = 86400

'''
{
    user_id: '123456789',
    reminded: 987654321,
    frequency: 86400
},
{
    ...
}
'''


def should_be_reminded(user_id):
    # print('')
    # print('DEBUG should_be_reminded: database content')
    # pprint.pprint(db.all())

    user_data = db.get(Query().user_id == user_id)
    return user_data is None or time.time() - user_data['reminded'] > user_data['frequency']


def reminded(user_id):
    # print('')
    # print('DEBUG reminded: database content before')
    # pprint.pprint(db.all())

    user_data = db.get(Query().user_id == user_id)
    if user_data is None:
        db.insert({'user_id': user_id, 'reminded': time.time(),
                   'frequency': DEFAUT_FREQUENCY})
    else:
        db.update({'reminded': time.time()}, Query().user_id == user_id)

    # print('DEBUG reminded: database content after')
    # pprint.pprint(db.all())


def set_frequency(user_id, frequency):
    # print('')
    # print('DEBUG set_frequency: database content before')
    # pprint.pprint(db.all())

    user_data = db.get(Query().user_id == user_id)
    if user_data is None:
        db.insert({'user_id': user_id, 'reminded': time.time(),
                   'frequency': frequency})
    else:
        db.update({'frequency': frequency}, Query().user_id == user_id)

    # print('DEBUG set_frequency: database content after')
    # pprint.pprint(db.all())
