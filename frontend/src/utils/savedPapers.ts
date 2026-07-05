import type { Paper } from "../types/paper";

const STORAGE_KEY = "savedPapers";

export function getSavedPapers(): Paper[] {
  const papers = localStorage.getItem(STORAGE_KEY);

  return papers ? JSON.parse(papers) : [];
}

export function savePaper(paper: Paper) {
  const papers = getSavedPapers();

  if (!papers.some((p) => p.arxiv_id === paper.arxiv_id)) {
    papers.push(paper);
    }

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(papers)
  );
}

export function removePaper(arxiv_id: string) {
  const papers = getSavedPapers().filter(
    (paper) => paper.arxiv_id !== arxiv_id
  );

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(papers)
  );
}

export function isPaperSaved(arxiv_id: string) {
  return getSavedPapers().some(
    (paper) => paper.arxiv_id === arxiv_id
  );
}