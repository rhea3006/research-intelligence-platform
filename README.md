# 📚 Research Intelligence Platform

A research paper discovery platform built using **FastAPI**, **PostgreSQL**, and the **arXiv API**. The platform enables users to ingest, search, filter, and discover research papers through intelligent ranking and recommendation features.

---

## 🚀 Features

### 📥 Research Paper Ingestion
- Fetches research papers from the arXiv API.
- Stores paper metadata in PostgreSQL.
- Prevents duplicate insertions using arXiv IDs.
- Supports incremental ingestion of newly published papers.

### 🔍 Intelligent Search

Search across:
- Title
- Abstract
- Authors
- Categories

Custom relevance scoring:

| Match Type | Score |
|------------|------:|
| Title | **4** |
| Abstract | **3** |
| Category | **2** |
| Author | **1** |

Results are automatically ranked by their relevance score.

---

### 📄 Paper Details

Retrieve complete metadata including:
- Title
- Abstract
- Authors
- Categories
- Published Date
- Updated Date
- arXiv URL

---

### 🎯 Related Paper Recommendations

Discover similar papers based on shared research categories.

Features:
- Dynamic similarity scoring
- Ranked recommendations
- Category-overlap recommendation engine

---

### 🗂️ Search Filtering

Filter search results by:
- Categories
- Publication Year
- Authors

---

## 🌐 REST API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/papers` | List research papers |
| GET | `/papers/{arxiv_id}` | Retrieve paper details |
| GET | `/papers/{arxiv_id}/related` | Get related papers |
| GET | `/search` | Intelligent paper search |

---

## 🛠 Tech Stack

### Frontend
- React
- TypeScript
- Axios
- CSS

### Backend
- FastAPI
- Python
- APScheduler

### Database
- PostgreSQL
- Neon Database
- pgvector

### AI / Search
- Sentence Transformers (all-MiniLM-L6-v2)
- Hybrid Search (Keyword + Semantic)
- HNSW Vector Indexing

### Deployment
- Render

---

## 📂 Project Structure

```text
research-intelligence-platform/
│
├── api/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── services/
│
├── ingestion/
│   ├── ingest_paper.py
│   ├── insert_paper.py
│   ├── test_arxiv.py
│   └── test_db.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🏗️ System Architecture


                +----------------------+
                |      React UI        |
                +----------+-----------+
                           |
                           v
                 FastAPI REST API
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
 Keyword Search                    Semantic Search
 (ILIKE + Ranking)             (Sentence Transformers)
        |                                     |
        +------------------+------------------+
                           |
                    Hybrid Ranking
                           |
                           v
                 PostgreSQL + pgvector
                           |
                           v
                   Automated arXiv Ingestion

---


## ✨ Features

- 🔍 Hybrid Search combining keyword and semantic retrieval
- 🧠 Semantic Search powered by Sentence Transformers
- ⚡ High-performance vector search using PostgreSQL + pgvector
- 📚 Automated research paper ingestion from arXiv
- 🗂 Advanced filtering by category, author, publication year, and relevance
- 📄 Detailed paper pages with metadata and related papers
- 🔄 Scheduled ingestion pipeline for keeping the database up to date
- 🌐 RESTful API built with FastAPI
- 💻 Modern React + TypeScript frontend

---

## 🔎 Search Pipeline

The platform uses a hybrid retrieval approach:

1. User submits a search query.
2. Keyword search retrieves relevant papers using PostgreSQL text matching.
3. The query is converted into a sentence embedding using Sentence Transformers.
4. pgvector performs semantic nearest-neighbor search using cosine similarity.
5. Keyword and semantic results are combined using weighted score fusion.
6. The final ranked papers are returned to the frontend.

---

## 🔮 Upcoming Features

- User authentication
- Saved papers & bookmarks
- AI-generated paper summaries
- Citation network visualization
- Cross-encoder reranking
- Personalized recommendations

---

## 📖 Future Scope

The long-term goal is to build an AI-powered research discovery platform capable of:

- Semantic paper search using embeddings
- Intelligent recommendation systems
- Automated research ingestion
- Large-scale research indexing
- Personalized research exploration

---

## 👩‍💻 Author

**Rhea Mathur**

B.Tech Computer Science (Data Science)
