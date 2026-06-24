'use client';

import { useEffect, useState } from 'react';
import { api } from '../../../services/api';
import { chatWithRepo } from "../../../services/chat";

interface IssueSummary {
    bugs?: number;
    warnings?: number;
    suggestions?: number;
}

interface DashboardData {
    repository_id: string;
    total_files?: number;
    engineering_score?: number;
    health_score?: number;
    languages?: string[];
    issues?: IssueSummary;
    ai_summary?: string;
}

interface SearchResult {
    path?: string;
    content?: string;
}

export default function RepositoryPage({
    params,
}: {
    params: { id: string };
}) {
    const [dashboard, setDashboard] =
        useState<DashboardData | null>(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState<string | null>(null);
    const [debugInfo, setDebugInfo] =
        useState<string>('');

    const [query, setQuery] = useState('');
    const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
    const [searchLoading, setSearchLoading] = useState(false);

    const [chatInput, setChatInput] = useState("");
    const [chatLoading, setChatLoading] = useState(false);
    const [chatMessages, setChatMessages] = useState<any[]>([]);

    const handleChat = async () => {
        if (!chatInput.trim()) return;

        const userMessage = {
            role: "user",
            content: chatInput,
        };

        setChatMessages((prev) => [...prev, userMessage]);

        const currentQuestion = chatInput;
        setChatInput("");

        try {
            setChatLoading(true);

            const response = await chatWithRepo(
                params.id,
                currentQuestion
            );

            const aiMessage = {
                role: "ai",
                content: response.answer,
                sources: response.sources,
            };

            setChatMessages((prev) => [...prev, aiMessage]);
        } catch (error) {
            console.error(error);
        } finally {
            setChatLoading(false);
        }
    };

    async function handleSearch() {
        if (!query.trim()) return;

        try {
            setSearchLoading(true);

            const response = await api.searchRepository(
                params.id,
                query
            );

            setSearchResults(
                response.results ||
                response.matches ||
                response.data ||
                []
            );
        } catch (error) {
            console.error(error);
        } finally {
            setSearchLoading(false);
        }
    }

    useEffect(() => {
        async function loadDashboard() {
            try {
                const data =
                    await api.getRepositoryDashboard(
                        params.id
                    );

                setDashboard(data);
            } catch (err) {
                console.error('Dashboard API Error:', err);
                setError('Failed to load dashboard');
                setDebugInfo(String(err));
            } finally {
                setLoading(false);
            }
        }

        loadDashboard();
    }, [params.id]);

    if (loading) {
        return (
            <div className='p-8'>
                Loading dashboard...
            </div>
        );
    }

    if (error) {
        return (
            <div className='p-8'>
                <h2>{error}</h2>
                <p>{debugInfo}</p>
            </div>
        );
    }

    return (
        <main className='p-8 space-y-8'>

            {/* HEADER */}
            <div>
                <h1 className='text-3xl font-bold'>
                    DevPilot Dashboard
                </h1>
                <p className='text-gray-500'>
                    AI-powered repository intelligence
                </p>
            </div>

            {/* TOP STATS */}
            <div className='grid grid-cols-1 md:grid-cols-4 gap-4'>
                <div className='border rounded-lg p-4'>
                    <h2 className='font-semibold'>Repository</h2>
                    <p>{dashboard?.repository_id}</p>
                </div>

                <div className='border rounded-lg p-4'>
                    <h2 className='font-semibold'>Files</h2>
                    <p>{dashboard?.total_files ?? 0}</p>
                </div>

                <div className='border rounded-lg p-4'>
                    <h2 className='font-semibold'>Engineering Score</h2>
                    <p>{dashboard?.engineering_score ?? 0}</p>
                </div>

                <div className='border rounded-lg p-4'>
                    <h2 className='font-semibold'>Health Score</h2>
                    <p>{dashboard?.health_score ?? 0}</p>
                </div>
            </div>

            {/* AI SUMMARY */}
            <div className='border rounded-lg p-5 bg-gray-50'>
                <h2 className='text-xl font-semibold mb-2'>
                    AI Repository Summary
                </h2>
                <p className='text-gray-700'>
                    {dashboard?.ai_summary || "No AI summary available yet"}
                </p>
            </div>

            {/* ISSUES */}
            <div className='border rounded-lg p-5'>
                <h2 className='text-xl font-semibold mb-4'>
                    Code Issues Overview
                </h2>

                <div className='grid grid-cols-3 gap-4 text-center'>
                    <div className='p-3 border rounded-lg'>
                        <p className='text-red-500 font-bold'>Bugs</p>
                        <p className='text-xl'>{dashboard?.issues?.bugs ?? 0}</p>
                    </div>

                    <div className='p-3 border rounded-lg'>
                        <p className='text-yellow-500 font-bold'>Warnings</p>
                        <p className='text-xl'>{dashboard?.issues?.warnings ?? 0}</p>
                    </div>

                    <div className='p-3 border rounded-lg'>
                        <p className='text-blue-500 font-bold'>Suggestions</p>
                        <p className='text-xl'>{dashboard?.issues?.suggestions ?? 0}</p>
                    </div>
                </div>
            </div>

            {/* SEARCH */}
            <div className='border rounded-lg p-4'>
                <h2 className='text-xl font-semibold mb-4'>
                    Repository Search
                </h2>

                <div className='flex gap-2 mb-4'>
                    <input
                        type='text'
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder='Search codebase...'
                        className='border rounded p-2 flex-1'
                    />

                    <button
                        onClick={handleSearch}
                        className='border rounded px-4 py-2'
                    >
                        Search
                    </button>
                </div>

                {searchLoading && (
                    <p>Searching...</p>
                )}

                <div className='space-y-4'>
                    {searchResults.map((result, index) => (
                        <div key={index} className='border rounded p-3'>
                            <p className='font-semibold'>
                                {result.path || 'Unknown File'}
                            </p>

                            <pre className='overflow-auto text-sm mt-2'>
                                {result.content || 'No Preview Available'}
                            </pre>
                        </div>
                    ))}
                </div>
            </div>

            {/* CHAT SECTION */}
            <div className="border rounded-lg p-4 mt-10">

                <h2 className="text-xl font-semibold mb-4">
                    Ask DevPilot AI
                </h2>

                <div className="h-80 overflow-y-auto border p-3 rounded mb-4 space-y-3">

                    {chatMessages.map((msg, idx) => (
                        <div key={idx}>
                            <p className={
                                msg.role === "user"
                                    ? "text-blue-600 font-semibold"
                                    : "text-green-700"
                            }>
                                {msg.role === "user" ? "You" : "AI"}
                            </p>

                            <p className="text-sm">
                                {msg.content}
                            </p>

                            {msg.sources && (
                                <p className="text-xs text-gray-500 mt-1">
                                    Sources: {msg.sources.join(", ")}
                                </p>
                            )}
                        </div>
                    ))}

                    {chatLoading && (
                        <p className="text-gray-500">
                            Thinking...
                        </p>
                    )}

                </div>

                <div className="flex gap-2">

                    <input
                        className="border flex-1 p-2 rounded"
                        value={chatInput}
                        onChange={(e) => setChatInput(e.target.value)}
                        placeholder="Ask something about this repo..."
                    />

                    <button
                        onClick={handleChat}
                        className="bg-black text-white px-4 rounded"
                    >
                        Send
                    </button>

                </div>

            </div>

        </main>
    );
}