from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)

db = client['instaparser']              # database

# ДЛЯ ПРОВЕРКИ:  выбрать одну из коллекций и одну из подгрупп follow_type (подписки/подписчики)
col = db.ecofest_gatchina               # collection
# col = db.rsbor_gatchina               # collection
follow_type = 'follower'
# follow_type = 'following'

res = []

for doc in col.find({'follow_type': follow_type}):
    res.append(doc.get('follow_name'))
    'BREAK'

pprint(res)
print(f'len={len(res)}')
