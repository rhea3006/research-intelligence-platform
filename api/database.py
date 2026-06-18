import psycopg2

def get_connection():
    return psycopg2.connect(dbname="research_intelligence", user="rheamathur",host="localhost")

def get_all_papers(limit,offset):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""Select arxiv_id, title from papers limit %s offset %s""",(limit,offset))

    results=cursor.fetchall()
    cursor.close()
    conn.close()

    return results

def get_paper_by_id(arxiv_id):
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute(""" SELECT * FROM papers WHERE arxiv_id = %s""",(arxiv_id,))
    
    paper=cursor.fetchone()

    if paper is None:
        cursor.close()
        conn.close()
        return None 
    
    cursor.close()
    conn.close()

    return paper

def search_papers(q, limit, offset):
    conn= get_connection()
    cursor=conn.cursor()

    cursor.execute("""Select arxiv_id, title, authors, published_date, 
                   (CASE
                        WHEN title ILIKE %s THEN 4
                        ELSE 0
                   END
                   +
                   CASE
                        WHEN abstract ILIKE %s THEN 3
                        ELSE 0
                    END
                   +
                    CASE
                        WHEN categories ILIKE %s THEN 2
                        ELSE 0
                   END
                   +
                   CASE
                        WHEN authors ILIKE %s THEN 1
                        ELSE 0 
                   END) AS relevance_score from papers WHERE 
                   title ILIKE %s OR abstract ILIKE %s OR authors ILIKE %s 
                   OR categories ILIKE %s 
                   ORDER BY relevance_score DESC
                   LIMIT %s
                   OFFSET %s""",
                   (f"%{q}%",f"%{q}%",f"%{q}%",f"%{q}%",f"%{q}%",f"%{q}%", f"%{q}%",f"%{q}%",
                    limit,offset))
    
    results=cursor.fetchall()

    return results

def get_related_papers(arxiv_id):
    conn= get_connection()
    cursor=conn.cursor()

    cursor.execute(""" Select categories from papers where arxiv_id = %s """,(arxiv_id,))
    categories_row= cursor.fetchone()

    if categories_row is None:
        cursor.close()
        conn.close()
        return []

    categories = categories_row[0]
    categories_list = categories.split(", ")

    score_conditions=[]
    where_conditions=[]

    for category in categories_list:
        score_conditions.append("""
                                CASE
                                WHEN categories ILIKE %s
                                THEN 1
                                ELSE 0
                                END""")
        where_conditions.append("categories ILIKE %s")
    
    score_clause = " + ".join(score_conditions)
    where_clause= " OR ".join(where_conditions)
    
    params = [f"%{category}%" for category in categories_list]
    score_params = params.copy()
    where_params = params.copy()
    where_params.append(arxiv_id)
    all_params = score_params + where_params

    print(score_clause)
    print(where_clause)
    print(all_params)
    
    cursor.execute(f"""SELECT arxiv_id, title, authors, published_date,
                   ({score_clause}) AS similarity_score FROM papers WHERE ({where_clause})
                   AND arxiv_id != %s ORDER BY similarity_score DESC LIMIT 10""", all_params)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results


