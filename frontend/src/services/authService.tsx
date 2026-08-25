const API_URL = "http://localhost:8000";


interface LoginResponse {
    message: string;
    access_token: string;
    token_type: string;
    user: {
        id: number;
        email: string;
        created_at: string;
    };
}


interface RegisterResponse {
    message: string;
    user: {
        id: number;
        email: string;
        created_at: string;
    };
}


export async function login(
    email: string,
    password: string
): Promise<LoginResponse> {

    const response = await fetch(
        `${API_URL}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email,
                password,
            }),
        }
    );


    if (!response.ok) {
        const error = await response.json();
        throw new Error(
            error.detail || "Login failed"
        );
    }


    return await response.json();
}



export async function register(
    email: string,
    password: string
): Promise<RegisterResponse> {

    const response = await fetch(
        `${API_URL}/auth/register`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email,
                password,
            }),
        }
    );


    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail || "Registration failed"
        );
    }


    return await response.json();
}