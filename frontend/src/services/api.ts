import axios from "axios";

const api = axios.create({
  baseURL: "https://research-intelligence-platform.onrender.com",
});

export default api;

export async function searchPapers(
  query: string,
  category: string,
  author: string,
  year: string,
  sort: string
) {
  const response = await api.get("/search", {
    params: {
      q: query,
      category,
      author,
      year,
      sort,
    },
  });

  return response.data;
}

export const getPaper = async (arxivId: string) => {

    const response = await api.get(`/papers/${arxivId}`);

    return response.data;

};