import type { SearchResponse } from "../types/paper";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default API_BASE;

export async function searchPapers(
  query: string,
  category: string,
  author: string,
  year: string,
  sort: string,
  page = 1
): Promise<SearchResponse> {
  const response = await API_BASE.get("/hybrid-search", {
    params: {
      q: query,
      category: category || undefined,
      author: author || undefined,
      year: year ? Number(year) : undefined,
      sort,
      page,
    },
  });

  return response.data;
}

export const getPaper = async (arxivId: string) => {

    const response = await API_BASE.get(`/papers/${arxivId}`);

    return response.data;

};

export const summarizePaper = async (arxivId: string) => {
    const response = await API_BASE.post("/workspace/summarize", {
        arxiv_id: arxivId,
    });

    return response.data;
};

export type AnalysisType =
    | "methodology"
    | "literature_review"
    |"critical_evaluation" 
    | "applications"

export interface AnalyzeWorkspaceRequest {
    paper_ids: string[];
    analysis_type: AnalysisType;
    additional_prompt: string;
    analysis_depth: string;
    writing_style: string;
    output_format: string;
}

export interface AnalyzeWorkspaceResponse {
    analysis: string;
}


export const analyzeWorkspace = async (
    request: AnalyzeWorkspaceRequest
): Promise<AnalyzeWorkspaceResponse> => {

    const response = await API_BASE.post(
        "/workspace/analyze",
        request
    );

    return response.data;
};

export interface SaveAnalysisRequest {
    title?: string;
    paper_arxiv_ids: string[];
    analysis_type: AnalysisType;
    analysis_depth: string;
    writing_style: string;
    output_format: string;
    additional_instructions: string;
    generated_markdown: string;
}

export interface SaveAnalysisResponse {
    analysis_id: number;
    message: string;
}

export const saveAnalysis = async (
    request: SaveAnalysisRequest
): Promise<SaveAnalysisResponse> => {

    const response = await API_BASE.post(
        "/analyses",
        request
    );

    return response.data;
};

export interface AnalysisSummary {
    id: number;
    title: string;
    analysis_type: string;
    created_at: string;
}

export interface Analysis {
    id: number;
    title: string;
    paper_arxiv_ids: string[];
    analysis_type: string;
    analysis_depth: string;
    writing_style: string;
    output_format: string;
    additional_instructions: string;
    generated_markdown: string;
    created_at: string;
}

export const getAnalyses = async (): Promise<AnalysisSummary[]> => {
    const response = await API_BASE.get("/analyses");
    return response.data;
};

export const getAnalysis = async (
    id: number
): Promise<Analysis> => {
    const response = await API_BASE.get(`/analyses/${id}`);
    return response.data;
};

export const deleteAnalysis = async (id: number) => {
    const response = await API_BASE.delete(`/analyses/${id}`);
    return response.data;
};