import json

# ebook 정보가 담긴 json파일 읽기
with open('Section3-1/ebook_list.json','r') as file:
  data = json.load(file)
data

import psycopg2

host = "jelani.db.elephantsql.com"
user = "dbmjodhp"
password = "ZBkJSjivgLQ9ffvcmUm_lZulOvyCmfO6"
database = "dbmjodhp"

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = connection.cursor()

# ebook 이라는 테이블이 존재하면 삭제하기
cur.execute("DROP TABLE IF EXISTS ebook;")

# ebook 테이블 생성하기
cur.execute("""CREATE TABLE ebook (
  id INTEGER PRIMARY KEY,
  title VARCHAR,
  author VARCHAR, 
  publisher VARCHAR, 
  category1 VARCHAR, 
  category2 VARCHAR, 
  price VARCHAR, 
  rate FLOAT, 
  product_link VARCHAR, 
  img_link VARCHAR, 
  introduce TEXT );""")
    
connection.commit()

# 데이터 삽입하기
for i in range(len(data)) :
  values = list(data[i].values())
  values.insert(0,i+1)
  cur.execute("INSERT INTO ebook VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", values)

connection.commit()

connection.close() 