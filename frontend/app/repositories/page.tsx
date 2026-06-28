"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { getMyRepositories } from "../../services/repositories";

export default function RepositoriesPage() {
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("name");
  const searchInputRef = useRef<HTMLInputElement>(null);

  const loadRepositories = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getMyRepositories();
      setRepositories(data);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadRepositories();
  }, [loadRepositories]);

  const filteredRepositories = useMemo(() => {
    const lowerSearch = search.toLowerCase();

    const filtered = repositories.filter(
      (repo) =>
        repo.repository_id.toLowerCase().includes(lowerSearch) ||
        (repo.summary && repo.summary.toLowerCase().includes(lowerSearch))
    );

    return filtered.sort((a, b) => {
      if (sortBy === "files") {
        return (b.total_files || 0) - (a.total_files || 0);
      }
      return a.repository_id.localeCompare(b.repository_id);
    });
  }, [repositories, search, sortBy]);

  const stats = useMemo(() => {
    return {
      totalRepositories: repositories.length,
      totalFiles: repositories.reduce(
        (sum, repo) => sum + (repo.total_files || 0),
        0
      )
    };
  }, [repositories]);

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">My Repositories</h1>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div className="border rounded-md p-4 bg-white shadow-sm">
          <p className="text-sm text-gray-500">Repositories</p>
          <p className="text-2xl font-bold">{stats.totalRepositories}</p>
        </div>
        <div className="border rounded-md p-4 bg-white shadow-sm">
          <p className="text-sm text-gray-500">Files Analyzed</p>
          <p className="text-2xl font-bold">{stats.totalFiles}</p>
        </div>
        <div className="border rounded-md p-4 bg-white shadow-sm">
          <p className="text-sm text-gray-500">Search Results</p>
          <p className="text-2xl font-bold">{filteredRepositories.length}</p>
        </div>
      </div>
      <input
        type="text"
        placeholder="Search repositories..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full mb-6 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        ref={searchInputRef}
      />
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="border rounded-md px-3 py-2"
        >
          <option value="name">Sort by Name</option>
          <option value="files">Sort by Files</option>
        </select>

        <button
          onClick={() => {
            setSearch("");
            searchInputRef.current?.focus();
          }}
          className="border rounded-md px-4 py-2 hover:bg-gray-100"
        >
          Clear Search
        </button>
      </div>
      {loading ? (
        <p>Loading repositories...</p>
      ) : filteredRepositories.length === 0 ? (
        <div className="border rounded-md p-6 text-center text-gray-600">
          <p className="mb-2 font-semibold">No repositories found.</p>
          <p>Upload your first repository to begin AI analysis.</p>
        </div>
      ) : (
        <>
          <div className="flex justify-between items-center mb-4">
            <p className="text-sm text-gray-500">
              Showing {filteredRepositories.length} repositories
            </p>
            <button
              onClick={loadRepositories}
              className="px-4 py-2 border rounded hover:bg-gray-100"
            >
              Refresh
            </button>
          </div>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filteredRepositories.map((repo) => (
              <div
                key={repo.repository_id}
                className="border rounded-md p-6 hover:shadow-md transition-shadow"
              >
                <h2 className="font-bold text-lg mb-2">{repo.repository_id}</h2>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                    Healthy
                  </span>
                  <span className="text-xs text-gray-500">
                    {repo.total_files} files
                  </span>
                </div>
                <div className="text-xs text-gray-500 mb-3">
                  Last analyzed: Just now
                </div>
                <p className="mb-1 text-sm text-gray-600">
                  AI Summary
                </p>
                <p className="mb-4 text-gray-700">
                  {repo.summary || "No summary available."}
                </p>
                <div className="flex gap-2 mt-4">
                  <Link
                    href={`/repository/${repo.repository_id}`}
                    className="flex-1 text-center px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                  >
                    Open
                  </Link>
                  <button
                    disabled
                    className="px-4 py-2 border rounded text-gray-400 cursor-not-allowed"
                  >
                    Coming Soon
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
