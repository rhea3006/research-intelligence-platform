const API_URL = "http://127.0.0.1:8000";


export async function apiClient(
    endpoint: string,
    options: RequestInit = {}
) {

    const token =
        localStorage.getItem("access_token");


    const headers = {
        "Content-Type": "application/json",

        ...(token && {
            Authorization: `Bearer ${token}`,
        }),

        ...options.headers,
    };


    const response = await fetch(
        `${API_URL}${endpoint}`,
        {
            ...options,
            headers,
        }
    );


    if (!response.ok) {

        const error =
            await response.json();

        throw new Error(
            error.detail ||
            "API request failed"
        );
    }


    return response.json();
}