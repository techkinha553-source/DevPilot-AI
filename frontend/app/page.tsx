"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getCurrentUser } from "../lib/auth";
import { logout } from "../lib/auth";

export default function Home() {

    const router = useRouter();

    useEffect(() => {
        const user = getCurrentUser();

        if (!user) {
            router.replace("/login");
            return;
        }

        router.replace("/dashboard");
    }, []);

    return (
        <main className="flex items-center justify-center min-h-screen">
            <p className="text-lg">Redirecting...</p>
        </main>
    );
}