import {
    createContext,
    useContext,
    useState,
    useEffect,
} from "react";

import type { ReactNode } from "react";


interface User {
    id: number;
    email: string;
    created_at: string;
}


interface AuthContextType {

    user: User | null;

    token: string | null;

    login: (data: LoginData) => void;

    logout: () => void;

    isAuthenticated: boolean;
}


interface LoginData {

    access_token: string;

    token_type: string;

    user: User;
}



const AuthContext = createContext<
    AuthContextType | undefined
>(undefined);



interface AuthProviderProps {
    children: ReactNode;
}

function isTokenExpired(token: string): boolean {
    try {
        const payload = JSON.parse(
            atob(token.split(".")[1])
        );

        return payload.exp * 1000 < Date.now();

    } catch {
        return true;
    }
}


export function AuthProvider({
    children,
}: AuthProviderProps) {


    const [user, setUser] =
        useState<User | null>(null);


    const [token, setToken] = useState<string | null>(() => {
    const storedToken = localStorage.getItem("access_token");

    if (!storedToken || isTokenExpired(storedToken)) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        return null;
    }

    return storedToken;
    });



    useEffect(() => {

        const storedUser =
            localStorage.getItem(
                "user"
            );


        if (storedUser) {

            setUser(
                JSON.parse(storedUser)
            );

        }

    }, []);




    const login = (
        data: LoginData
    ) => {


        localStorage.setItem(
            "access_token",
            data.access_token
        );


        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );



        setToken(
            data.access_token
        );


        setUser(
            data.user
        );
    };





    const logout = () => {


        localStorage.removeItem(
            "access_token"
        );


        localStorage.removeItem(
            "user"
        );



        setToken(null);

        setUser(null);

    };





    return (

        <AuthContext.Provider
            value={{
                user,
                token,
                login,
                logout,
                isAuthenticated:
                    !!token,
            }}
        >

            {children}

        </AuthContext.Provider>

    );
}




export function useAuth() {

    const context =
        useContext(AuthContext);


    if (!context) {

        throw new Error(
            "useAuth must be used inside AuthProvider"
        );

    }


    return context;
}