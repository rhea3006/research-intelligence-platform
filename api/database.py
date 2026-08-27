from pgvector.psycopg2 import register_vector
from fastapi import HTTPException
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    register_vector(conn)
    return conn


# Papers table 
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

def search_papers(q, limit, offset, category= None, author= None, year= None,
                   sort="relevance"):
    conn= get_connection()
    cursor=conn.cursor()

    search_term = f"%{q}%"
    params = [search_term] * 8
    params.extend([limit, offset])

    filters=[]

    count_query = """SELECT COUNT(*) FROM papers WHERE (title ILIKE %s OR abstract ILIKE %s
        OR authors ILIKE %s OR categories ILIKE %s)"""

    if sort == "newest":
        order_by = "published_date DESC"
    elif sort == "oldest":
        order_by = "published_date ASC"
    else:
        order_by = "relevance_score DESC"

    query="""SELECT arxiv_id,title,abstract,authors,categories,published_date,
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
        END) AS relevance_score FROM papers
        WHERE (title ILIKE %s OR abstract ILIKE %s OR authors ILIKE %s 
        OR categories ILIKE %s )
        ORDER BY ORDER_BY_PLACEHOLDER LIMIT %s OFFSET %s"""
    
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
        query = query.replace("ORDER BY ORDER_BY_PLACEHOLDER",
            f"AND {' AND '.join(filters)} ORDER BY ORDER_BY_PLACEHOLDER")

    if filters:
        count_query += f" AND {' AND '.join(filters)}"

    query = query.replace("ORDER_BY_PLACEHOLDER",order_by)

   
    cursor.execute(query, params)
    
    results=cursor.fetchall()
   
    count_params = [search_term] * 4
    if category:
        count_params.append(f"%{category}%")

    if author:
        count_params.append(f"%{author}%")

    if year:
        count_params.append(year)

    cursor.execute(count_query, count_params)
    
    total = cursor.fetchone()[0]
   
    cursor.close()
    conn.close()

    print(f"Found {len(results)} papers")        

    return results, total

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

    cursor.execute("""SELECT arxiv_id, title, abstract FROM papers""")
    results = cursor.fetchall()

    cursor.close()

    conn.close()

    return results

def update_embedding_vector(arxiv_id, embedding):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE papers
        SET embedding_vector = %s
        WHERE arxiv_id = %s
        """,
        (embedding, arxiv_id),
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_all_embeddings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
    """
    SELECT
        arxiv_id,
        title,
        authors,
        published_date,
        embedding_vector
    FROM papers
    WHERE embedding_vector IS NOT NULL
    """
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results


def semantic_search_db(query_embedding,limit=10,category=None,author=None,year=None,):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            arxiv_id,
            title,
            authors,
            categories,
            published_date,
            0 AS relevance_score,
            1 - (embedding_vector <=> %s::vector) AS similarity
        FROM papers
        WHERE embedding_vector IS NOT NULL
    """

    params = [query_embedding]

    if category:
        query += " AND categories ILIKE %s"
        params.append(f"%{category}%")

    if author:
        query += " AND authors ILIKE %s"
        params.append(f"%{author}%")

    if year:
        query += " AND EXTRACT(YEAR FROM published_date) = %s"
        params.append(year)

    query += """
        ORDER BY embedding_vector <=> %s::vector
        LIMIT %s
    """

    params.append(query_embedding)
    params.append(limit)

    cursor.execute(query, params)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def paper_exists(cursor, arxiv_id):
    cursor.execute(
        """
        SELECT 1
        FROM papers
        WHERE arxiv_id = %s
        """,
        (arxiv_id,),
    )

    return cursor.fetchone() is not None

def get_workspace_papers(arxiv_ids: list[str]):
    """
    Fetch the papers selected in the AI Workspace.
    Returns only the fields required for AI analysis.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            arxiv_id,
            title,
            abstract,
            authors,
            categories,
            published_date
        FROM papers
        WHERE arxiv_id = ANY(%s)
        """,
        (arxiv_ids,),
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def save_analysis(user_id, title, paper_arxiv_ids, analysis_type, analysis_depth,
                  writing_style, output_format, additional_instructions,
                  generated_markdown):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Insert the analysis
        cursor.execute(
            """
            INSERT INTO analyses (
            user_id,
            title,
            analysis_type,
            analysis_depth,
            writing_style,
            output_format,
            additional_instructions,
            generated_markdown
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (user_id,title,analysis_type,analysis_depth,writing_style,output_format,
             additional_instructions,generated_markdown,),
        )

        analysis_id = cursor.fetchone()[0]

        # Link all selected papers
        for arxiv_id in paper_arxiv_ids:
            cursor.execute(
                """
                INSERT INTO analysis_papers (
                    analysis_id,
                    paper_arxiv_id
                )
                VALUES (%s, %s)
                """,
                (
                    analysis_id,
                    arxiv_id,
                ),
            )

        conn.commit()
        return analysis_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

def get_all_analyses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                id,
                title,
                analysis_type,
                created_at
            FROM analyses
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "analysis_type": row[2],
                "created_at": row[3],
            }
            for row in rows
        ]

    finally:
        cursor.close()
        conn.close()

def get_analysis_by_id(analysis_id,user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                a.id,
                a.title,
                a.analysis_type,
                a.analysis_depth,
                a.writing_style,
                a.output_format,
                a.additional_instructions,
                a.generated_markdown,
                a.created_at,
                ap.paper_arxiv_id
            FROM analyses a
            LEFT JOIN analysis_papers ap
                ON a.id = ap.analysis_id
            WHERE a.id = %s AND a.user_id = %s
            """,
            (analysis_id,user_id),
        )

        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404,detail="Analysis not found")

        first = rows[0]

        return {
            "id": first[0],
            "title": first[1],
            "analysis_type": first[2],
            "analysis_depth": first[3],
            "writing_style": first[4],
            "output_format": first[5],
            "additional_instructions": first[6],
            "generated_markdown": first[7],
            "created_at": first[8],
            "paper_arxiv_ids": [
                row[9] for row in rows if row[9] is not None
            ],
        }

    finally:
        cursor.close()
        conn.close()

def delete_analysis(analysis_id,user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM analyses
            WHERE id = %s
            AND user_id = %s
            RETURNING id
            """,
            (analysis_id,user_id),
        )

        deleted = cursor.fetchone()

        conn.commit()

        if not deleted:
            raise HTTPException(status_code=404,detail="Analysis not found")

        return {"message": "Analysis deleted successfully"}

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

# Saved Papers table 

def get_saved_papers(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                p.arxiv_id,
                p.title,
                p.abstract,
                p.authors,
                p.categories,
                p.published_date
            FROM saved_papers sp
            JOIN papers p
                ON sp.paper_arxiv_id = p.arxiv_id
            WHERE sp.user_id = %s
            ORDER BY sp.created_at DESC
            """,
            (user_id,),
        )

        rows = cursor.fetchall()

        return [
            {
                "arxiv_id": row[0],
                "title": row[1],
                "abstract": row[2],
                "authors": row[3],
                "categories": row[4],
                "published_date": row[5],
            }
            for row in rows
        ]

    finally:
        cursor.close()
        conn.close()


def save_paper_for_user(user_id, arxiv_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO saved_papers (user_id, paper_arxiv_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, paper_arxiv_id)
            DO NOTHING
            """,
            (user_id, arxiv_id),
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def remove_saved_paper(user_id, arxiv_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM saved_papers
            WHERE user_id = %s
            AND paper_arxiv_id = %s
            """,
            (user_id, arxiv_id),
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    