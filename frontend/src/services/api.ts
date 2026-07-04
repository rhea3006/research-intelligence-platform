import axios from "axios";

const api = axios.create({
  baseURL: "https://research-intelligence-platform.onrender.com",
});

export default api;

export async function searchPapers(query: string) {
  const response = await api.get("/search", {
    params: {
      q: query,
    },
  });

  return response.data;
}

export const getPaper = async (arxivId: string) => {

    const response = await api.get(`/papers/${arxivId}`);

    return response.data;

};