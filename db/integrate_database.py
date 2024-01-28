import os
import random
import sqlite3

from db.static_sqlite import *

data_path = '../data/2024_01_28_01_03_28'
datas = []
for name in os.listdir(data_path):
    conn = sqlite3.connect(os.path.join(data_path, name))
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM article").fetchall()
    datas += result
    conn.close()

for i in range(len(datas)):
    datas[i] = list(datas[i])
    datas[i][0] = None

random.shuffle(datas)
print(f'total len: {len(datas)}')

conn = sqlite3.connect(os.path.join('../data', '2024_01_28_01_03_28_integrate.db'))
cur = conn.cursor()
cur.execute(SQL_ARTICLE_TABLE_CREATE)
conn.commit()
cur.executemany("INSERT INTO article VALUES (?,?,?,?,?)", datas)
conn.commit()
conn.close()
