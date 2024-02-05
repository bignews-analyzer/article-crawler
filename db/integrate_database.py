import os
import random
import sqlite3

from db.static_sqlite import *

data_path = '../data'
datas = []
for dir_name in os.listdir(data_path):
    path = os.path.join(data_path, dir_name)
    if os.path.isfile(path):
        continue
    for name in os.listdir(path):
        conn = sqlite3.connect(os.path.join(data_path, dir_name, name))
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM article").fetchall()
        datas += result
        conn.close()

print(f'before total len: {len(datas)}')

u_data = dict()
for item in datas:
    u_data[item[1] + item[2]] = item

datas = list(u_data.values())

for i in range(len(datas)):
    datas[i] = list(datas[i])
    datas[i][0] = None

random.shuffle(datas)
print(f'total len: {len(datas)}')

conn = sqlite3.connect(os.path.join('../data', 'integrate_remove.db'))
cur = conn.cursor()
cur.execute(SQL_ARTICLE_TABLE_CREATE)
conn.commit()
cur.executemany("INSERT INTO article VALUES (?,?,?,?,?)", datas)
conn.commit()
conn.close()
