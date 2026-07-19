export interface Paper {
  arxiv_id: string;
  title: string;
  abstract?: string;
  authors: string;
  categories: string;
  published_date: string;

  relevance_score: number;
  semantic_score: number;
  hybrid_score: number;
}

export interface PaperDetail {
    arxiv_id: string;
    title: string;
    authors: string;
    abstract: string;
    categories: string;
    published_date: string;
    arxiv_url: string;
}

export interface SearchResponse {
    results: Paper[];
    page: number;
    limit: number;
    total: number;
    total_pages: number;
}