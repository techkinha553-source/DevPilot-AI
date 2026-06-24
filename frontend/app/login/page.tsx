"use client";

import { useState } from "react";
import { login } from "../../services/auth";
import { useEffect } from "react";
import { getCurrentUser } from "../../lib/auth";

export default function LoginPage() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    useEffect(() => {

        const user = getCurrentUser();

        if (user) {
            window.location.href = "/";
        }

    }, []);

    const handleLogin = async () => {

        const result = await login(
            email,
            password
        );

        if (result.email) {

            localStorage.setItem(
                "devpilot_user",
                JSON.stringify(result)
            );

            window.location.href = "/";
        }

        alert(result.message);
    };

    return (
        <main className="p-8 max-w-md mx-auto">

            <h1 className="text-3xl font-bold mb-6">
                Login
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
                onClick={handleLogin}
                className="bg-black text-white px-4 py-2 rounded"
            >
                Login
            </button>

        </main>
    );
}