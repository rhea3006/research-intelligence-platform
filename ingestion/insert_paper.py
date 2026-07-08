from api.database import get_connection

if __name__ == "__main__":
    conn= get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO papers(arxiv_id, title, abstract, published_date)VALUES('9999.9999','Paper Inserted By Python',
        'This paper was added programmatically',CURRENT_DATE);""")
    conn.commit()
    print("Paper inserted successfully!")
    cursor.close()
    conn.close()