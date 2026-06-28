"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { logout } from "../../lib/auth";
import { getCurrentUser } from "../../lib/auth";
import { getDashboard } from "../../services/dashboard";
import { getActivity } from "../../services/activity";

export default function Dashboard() {

    const [stats, setStats] = useState<any>({});
    const [activities, setActivities] = useState<any[]>([]);
    const [userEmail, setUserEmail] = useState("User");

    useEffect(() => {
        const user = getCurrentUser();
        if (user?.email) {
            setUserEmail(user.email);
        }
        loadDashboard();
        loadActivities();
    }, []);

    const loadDashboard = async () => {

        const user = getCurrentUser();

        if (!user || !user.email) {
            console.error("No logged in user found");
            return;
        }

        const data = await getDashboard(
            user.email
        );

        setStats(data);
    };

    const loadActivities = async () => {

        const data = await getActivity();

        setActivities(data.reverse());
    };

    return (
        <main className="min-h-screen bg-gray-100 flex">

            <aside className="w-64 bg-white shadow-lg p-6 min-h-screen">

                <h2 className="text-2xl font-bold mb-8">
                    DevPilot
                </h2>

                <nav className="flex flex-col gap-4">

                    <Link href="/dashboard" className="hover:text-blue-600">
                        Dashboard
                    </Link>

                    <Link href="/repositories" className="hover:text-blue-600">
                        Repositories
                    </Link>

                    <Link href="/upload" className="hover:text-blue-600">
                        Upload Repository
                    </Link>

                    <Link href="/chat" className="hover:text-blue-600">
                        AI Chat
                    </Link>

                    <Link href="/settings" className="hover:text-blue-600">
                        Settings
                    </Link>

                    <button
                        onClick={logout}
                        className="text-left text-red-500 hover:text-red-700 mt-4"
                    >
                        Logout
                    </button>

                </nav>

            </aside>

            <div className="flex-1 p-8">

                <div className="bg-white rounded-xl shadow px-6 py-4 mb-8 flex justify-between items-center">

                    <div>
                        <h1 className="text-4xl font-bold">
                            DevPilot Dashboard
                        </h1>
                        <p className="text-gray-600 mt-2">
                            Personal analytics and repository insights
                        </p>
                    </div>

                    <div className="flex items-center gap-4">

                        <button
                            className="px-4 py-2 rounded-lg border hover:bg-gray-100"
                        >
                            🌙 Dark Mode
                        </button>

                        <div className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium">
                            {userEmail}
                        </div>

                    </div>

                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

                    <div className="bg-white rounded-xl shadow p-6">
                        <h2 className="text-sm text-gray-500">
                            Repositories
                        </h2>
                        <p className="text-3xl font-bold mt-2">
                            {stats.repositories || 0}
                        </p>
                    </div>

                    <div className="bg-white rounded-xl shadow p-6">
                        <h2 className="text-sm text-gray-500">
                            Files Analyzed
                        </h2>
                        <p className="text-3xl font-bold mt-2">
                            {stats.files_analyzed || 0}
                        </p>
                    </div>

                    <div className="bg-white rounded-xl shadow p-6">
                        <h2 className="text-sm text-gray-500">
                            Questions Asked
                        </h2>
                        <p className="text-3xl font-bold mt-2">
                            {stats.questions_asked || 0}
                        </p>
                    </div>

                    <div className="bg-white rounded-xl shadow p-6">
                        <h2 className="text-sm text-gray-500">
                            Health Score
                        </h2>
                        <p className="text-3xl font-bold mt-2">
                            {stats.avg_health_score || 0}%
                        </p>
                    </div>

                </div>

                <div className="bg-white rounded-xl shadow p-6">
                    <h2 className="text-2xl font-semibold mb-4">
                        Recent Activity
                    </h2>

                    {/* <ul className="space-y-3 text-gray-700">
                        <li>Repository uploads will appear here.</li>
                        <li>AI chat activity will appear here.</li>
                        <li>Health analysis history will appear here.</li>
                    </ul> */}

                    <ul className="space-y-3 text-gray-700">
                            {activities.map(
                                (activity, index) => (
                                    <li key={index}>
                                        {activity.message}
                                    </li>
                                )
                            )}
                    </ul>
                </div>

            </div>

        </main>
    );
}
