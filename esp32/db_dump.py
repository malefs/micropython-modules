import btree

f = open('btree.db', 'r+b')
db = btree.open(f)

for key in db:
    print(key.decode('utf-8'), db[key].decode('utf-8'))

