"use client";

import { useState } from "react";
import { signup } from "../../services/auth";

export default function SignupPage() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSignup = async () => {

        const result = await signup(
            email,
            password
        );

        if (result?.email) {
            alert("Signup successful. Please login.");
            window.location.href = "/login";
            return;
        }

        const errorMessage =
            result?.message ||
            result?.detail ||
            "Signup failed";

        alert(errorMessage);

        if (
            errorMessage.toLowerCase().includes("already") ||
            errorMessage.toLowerCase().includes("exists")
        ) {
            window.location.href = "/login";
        }
    };

    return (
        <main className="p-8 max-w-md mx-auto">

            <h1 className="text-3xl font-bold mb-6">
                Sign Up
            </h1>

            <input
                className="border p-2 w-full mb-3"
                placeholder="Email"
                value={email}
                onChange={(e) =>
                    setEmail(e.target.value)
                }
            />

            <input
                type="password"
                className="border p-2 w-full mb-3"
                placeholder="Password"
                value={password}
                onChange={(e) =>
                    setPassword(e.target.value)
                }
            />

            <button
                onClick={handleSignup}
                className="bg-black text-white px-4 py-2 rounded"
            >
                Sign Up
            </button>

        </main>
    );
}