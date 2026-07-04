export interface Paper {
  arxiv_id: string;
  title: string;
  authors: string;
  published_date: string;
  relevance_score: number;
}

export interface PaperDetail {
    arxiv_id: string;
    title: string;
    authors: string;
    abstract: string;
    categories: string;
    published_date: string;
}