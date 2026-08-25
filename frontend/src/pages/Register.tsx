import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { register } from "../services/authService";


export default function Register() {

    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [error, setError] =
        useState("");

    const [success, setSuccess] =
        useState("");


    const navigate = useNavigate();



    async function handleSubmit(
        e: React.FormEvent
    ) {

        e.preventDefault();


        try {

            setError("");
            setSuccess("");


            await register(
                email,
                password
            );


            setSuccess(
                "Account created successfully!"
            );


            setTimeout(() => {
                navigate("/login");
            }, 1000);



        } catch(err) {

            if(err instanceof Error) {
                setError(err.message);
            }
            else {
                setError(
                    "Registration failed"
                );
            }

        }

    }



    return (

        <div>

            <h1>
                Create Account
            </h1>


            {error && (
                <p>
                    {error}
                </p>
            )}


            {success && (
                <p>
                    {success}
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
                    Register
                </button>


            </form>

        </div>

    );
}