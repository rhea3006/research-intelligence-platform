import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Mail, Lock, ArrowRight, FlaskConical } from "lucide-react";

import { register } from "../services/authService";

import "./RegisterPage.css";

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const navigate = useNavigate();

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();

        try {
            setError("");
            setSuccess("");

            await register(email, password);

            setSuccess("Account created successfully!");

            setTimeout(() => {
                navigate("/login");
            }, 1000);

        } catch (err) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError("Registration failed");
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
                        <h1>Create your account</h1>

                        <p>
                            Build your personal research workspace.
                        </p>
                    </div>

                    {error && (
                        <div className="auth-message auth-error">
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className="auth-message auth-success">
                            {success}
                        </div>
                    )}

                    <form
                        className="auth-form"
                        onSubmit={handleSubmit}
                    >

                        <div className="auth-field">
                            <label htmlFor="register-email">
                                Email
                            </label>

                            <div className="auth-input-wrapper">
                                <Mail size={18} />

                                <input
                                    id="register-email"
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
                            <label htmlFor="register-password">
                                Password
                            </label>

                            <div className="auth-input-wrapper">
                                <Lock size={18} />

                                <input
                                    id="register-password"
                                    type="password"
                                    placeholder="Create a password"
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
                            <span>Create Account</span>
                            <ArrowRight size={18} />
                        </button>

                    </form>

                    <div className="auth-divider">
                        <span>or</span>
                    </div>

                    <p className="auth-switch">
                        Already have an account?
                        <button
                            type="button"
                            onClick={() => navigate("/login")}
                        >
                            Login here
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