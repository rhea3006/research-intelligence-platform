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

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### Database
- PostgreSQL
- psycopg2

### Data Source
- arXiv API

### Version Control
- Git
- GitHub

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

```text
              arXiv API
                  │
                  ▼
        Ingestion Pipeline
                  │
                  ▼
          PostgreSQL Database
                  │
                  ▼
            FastAPI Backend
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
 Paper APIs   Search Engine  Recommendations
                  │
                  ▼
        Relevance Ranking
```

---

## ✅ Current Progress

### Implemented
- ✅ Research paper ingestion
- ✅ PostgreSQL database integration
- ✅ FastAPI REST API
- ✅ Intelligent keyword search
- ✅ Relevance-based search ranking
- ✅ Paper detail endpoint
- ✅ Related paper recommendation engine
- ✅ Search filtering
- ✅ Automated ingestion pipeline
- ✅ Backend architecture refactoring

---

## 🔮 Upcoming Features

- 🎨 Frontend web application
- 🧠 Semantic search using vector embeddings
- 🔀 Hybrid keyword + semantic search
- 📊 Research analytics dashboard
- ⭐ Bookmark & save papers
- 🤖 Personalized recommendations
- ☁️ Cloud deployment

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
