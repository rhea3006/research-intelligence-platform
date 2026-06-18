import psycopg2
conn= psycopg2.connect(dbname="research_intelligence", user="rheamathur", host="localhost")
cursor=conn.cursor()
cursor.execute("Select * from papers;")
rows=cursor.fetchall()
for row in rows:
    print(row)
cursor.close()
conn.close()