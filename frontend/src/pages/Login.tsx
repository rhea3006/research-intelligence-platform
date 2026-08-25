import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { login } from "../services/authService";
import { useAuth } from '../auth/Authcontext.tsx'


export default function Login() {

    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [error, setError] =
        useState("");


    const navigate = useNavigate();

    const { login: saveLogin } =
        useAuth();



    async function handleSubmit(
        e: React.FormEvent
    ) {

        e.preventDefault();

        try {

            setError("");

            const data =
                await login(
                    email,
                    password
                );


            saveLogin(data);


            navigate("/");

        } catch (err) {

            if (err instanceof Error) {
                setError(err.message);
            }
            else {
                setError(
                    "Login failed"
                );
            }
        }
    }



    return (
        <div>

            <h1>
                Login
            </h1>


            {error && (
                <p>
                    {error}
                </p>
            )}


            <form
                onSubmit={handleSubmit}
            >

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) =>
                        setEmail(
                            e.target.value
                        )
                    }
                />


                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) =>
                        setPassword(
                            e.target.value
                        )
                    }
                />


                <button type="submit">
                    Login
                </button>

            </form>

        </div>
    );
}