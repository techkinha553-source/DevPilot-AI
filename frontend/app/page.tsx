"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getRepositories } from "../services/repositories";
import { useRouter } from "next/navigation";
import { getCurrentUser } from "../lib/auth";
import { logout } from "../lib/auth";

export default function Home() {

    const [repos, setRepos] = useState<any[]>([]);

    useEffect(() => {

        const user = getCurrentUser();

        if (!user) {
            router.push("/login");
            return;
        }

        loadRepos();

    }, []);

    const loadRepos = async () => {
        const user = getCurrentUser();
        const data = await getRepositories(user.email);
        setRepos(data);
    };

    const router = useRouter();

    return (
        <main className="p-8">
            <div className="flex justify-between items-center mb-6">

                <h1 className="text-3xl font-bold">
                    DevPilot Repositories
                </h1>

                <button
                    onClick={logout}
                    className="bg-red-500 text-white px-4 py-2 rounded"
                >
                    Logout
                </button>

            </div>

            <div className="space-y-4">

                {repos.map((repo) => (
                    <Link
                        key={repo.repository_id}
                        href={`/repository/${repo.repository_id}`}
                    >
                        <div className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer">

                            <h2 className="font-semibold">
                                {repo.repository_id}
                            </h2>

                            <p>
                                Files: {repo.total_files}
                            </p>

                        </div>
                    </Link>
                ))}

            </div>
        </main>
    );
}