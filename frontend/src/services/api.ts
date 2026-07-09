import type { SearchResponse } from "../types/paper";
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export default api;

export async function searchPapers(
  query: string,
  category: string,
  author: string,
  year: string,
  sort: string,
  page: number
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