import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Mail, Lock, ArrowRight, FlaskConical } from "lucide-react";

import { login } from "../services/authService.ts";
import { useAuth } from "../auth/Authcontext.tsx";

import "./LoginPage.css";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const { login: saveLogin } = useAuth();

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();

        try {
            setError("");

            const data = await login(email, password);

            saveLogin(data);

            navigate("/");
        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError("Login failed");
            }
        }
    }

    return (
        <div className="auth-page">
            <div className="auth-background">
                <div className="auth-glow auth-glow-one" />
                <div className="auth-glow auth-glow-two" />
            </div>

            <main className="auth-container">

                <div className="auth-brand">
                    <div className="auth-brand-icon">
                        <FlaskConical size={24} strokeWidth={1.8} />
                    </div>

                    <span>Research Intelligence Platform</span>
                </div>

                <section className="auth-card">

                    <div className="auth-header">
                        <h1>Welcome back</h1>

                        <p>
                            Sign in to continue your research workflow.
                        </p>
                    </div>

                    {error && (
                        <div className="auth-message auth-error">
                            {error}
                        </div>
                    )}

                    <form
                        className="auth-form"
                        onSubmit={handleSubmit}
                    >

                        <div className="auth-field">
                            <label htmlFor="email">
                                Email
                            </label>

                            <div className="auth-input-wrapper">
                                <Mail size={18} />

                                <input
                                    id="email"
                                    type="email"
                                    placeholder="you@example.com"
                                    value={email}
                                    onChange={(e) =>
                                        setEmail(e.target.value)
                                    }
                                    required
                                />
                            </div>
                        </div>

                        <div className="auth-field">
                            <label htmlFor="password">
                                Password
                            </label>

                            <div className="auth-input-wrapper">
                                <Lock size={18} />

                                <input
                                    id="password"
                                    type="password"
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(e) =>
                                        setPassword(e.target.value)
                                    }
                                    required
                                />
                            </div>
                        </div>

                        <button
                            className="auth-submit"
                            type="submit"
                        >
                            <span>Login</span>
                            <ArrowRight size={18} />
                        </button>

                    </form>

                    <div className="auth-divider">
                        <span>or</span>
                    </div>

                    <p className="auth-switch">
                        New user?
                        <button
                            type="button"
                            onClick={() => navigate("/register")}
                        >
                            Register here
                        </button>
                    </p>

                </section>

                <p className="auth-footer">
                    Explore. Analyze. Understand research.
                </p>

            </main>
        </div>
    );
}