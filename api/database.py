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

def search_papers(q, limit, offset, category= None, author= None, year= None):
    conn= get_connection()
    cursor=conn.cursor()

    search_term = f"%{q}%"
    params = [search_term] * 8
    params.extend([limit, offset])

    filters=[]

    query="""Select arxiv_id, title, authors, published_date, 
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
                   END) AS relevance_score from papers 
                   WHERE (title ILIKE %s OR abstract ILIKE %s OR authors ILIKE %s 
                   OR categories ILIKE %s )
                   ORDER BY relevance_score DESC
                   LIMIT %s
                   OFFSET %s"""
    
    
    if category:
        filters.append("categories ILIKE %s")
        params.insert(-2, f"%{category}%")
    
    if author:
        filters.append("authors ILIKE %s")
        params.insert(-2, f"%{author}%")

    if year:
        filters.append("EXTRACT(YEAR FROM published_date) = %s")
        params.insert(-2, year)

    if filters:
        query = query.replace("ORDER BY relevance_score DESC",
                               f"AND {' AND '.join(filters)} ORDER BY relevance_score DESC")

    cursor.execute(query, params)
    results=cursor.fetchall()
    cursor.close()
    conn.close()

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

def get_papers_for_embedding():
    conn= get_connection()
    cursor=conn.cursor()

    cursor.execute("""SELECT arxiv_id, title, abstract FROM papers WHERE embedding IS NULL""")
    results = cursor.fetchall()

    cursor.close()

    conn.close()

    return results

def update_embedding(arxiv_id, embedding):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""UPDATE papers SET embedding = %s WHERE arxiv_id = %s""",
                   (embedding, arxiv_id))

    conn.commit()

    cursor.close()
    conn.close()

def get_all_embeddings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT arxiv_id,title, authors, published_date, embedding FROM papers
                   WHERE embedding IS NOT NULL""")

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results