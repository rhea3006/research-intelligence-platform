-- ============================================================
-- Research Intelligence Platform
-- Database Schema
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;


-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE users (
    id INTEGER NOT NULL,
    email VARCHAR NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE,

    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
);


-- ============================================================
-- PAPERS
-- ============================================================

CREATE TABLE papers (
    id INTEGER NOT NULL,
    arxiv_id VARCHAR(50),
    title TEXT,
    abstract TEXT,
    published_date DATE,
    authors TEXT,
    categories TEXT,
    arxiv_url TEXT,
    updated_date DATE,
    embedding_vector vector,

    CONSTRAINT papers_pkey PRIMARY KEY (id),
    CONSTRAINT papers_arxiv_id_key UNIQUE (arxiv_id)
);


-- ============================================================
-- ANALYSES
-- ============================================================

CREATE TABLE analyses (
    id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    analysis_type VARCHAR NOT NULL,
    analysis_depth VARCHAR NOT NULL,
    writing_style VARCHAR NOT NULL,
    output_format VARCHAR NOT NULL,
    additional_instructions TEXT,
    generated_markdown TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    user_id INTEGER,

    CONSTRAINT analyses_pkey PRIMARY KEY (id),

    CONSTRAINT analyses_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES users(id)
);


-- ============================================================
-- ANALYSIS PAPERS
-- ============================================================

CREATE TABLE analysis_papers (
    analysis_id INTEGER NOT NULL,
    paper_arxiv_id VARCHAR NOT NULL,

    CONSTRAINT analysis_papers_pkey
        PRIMARY KEY (analysis_id, paper_arxiv_id),

    CONSTRAINT analysis_papers_analysis_id_fkey
        FOREIGN KEY (analysis_id)
        REFERENCES analyses(id),

    CONSTRAINT analysis_papers_paper_arxiv_id_fkey
        FOREIGN KEY (paper_arxiv_id)
        REFERENCES papers(arxiv_id)
);