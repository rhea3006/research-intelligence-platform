import type { SearchResponse } from "../types/paper";
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export default api;

export async function searchPapers(
  query: string,
  category: string,
  author: string,
  year: string,
  sort: string,
  page = 1
): Promise<SearchResponse> {
  const response = await api.get("/hybrid-search", {
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

    const response = await api.get(`/papers/${arxivId}`);

    return response.data;

};

export const summarizePaper = async (arxivId: string) => {
    const response = await api.post("/workspace/summarize", {
        arxiv_id: arxivId,
    });

    return response.data;
};

export type AnalysisType =
    | "compare"
    | "literature_review"
    | "research_gap"
    | "beginner";

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

    const response = await api.post(
        "/workspace/analyze",
        request
    );

    return response.data;
};