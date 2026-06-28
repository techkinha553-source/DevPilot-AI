"use client";

import React, { useEffect, useState, useRef } from "react";
import { getMyRepositories } from "../../services/repositories";

export default function ChatPage() {
  const [repositories, setRepositories] = useState<any[]>([]);
  const [selectedRepository, setSelectedRepository] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);

  const [messages, setMessages] = useState<{
    role: "user" | "assistant";
    content: string;
    sources?: string[];
    timestamp?: string;
  }[]>([]);
  const CHAT_STORAGE_KEY = "devpilot_chat_history";

  const [question, setQuestion] = useState("");
  const [sending, setSending] = useState(false);
  const [githubConnected, setGithubConnected] = useState(false);
  const [githubUsername, setGithubUsername] = useState("");
  // GitHub repositories state for upcoming browsing support
  const [githubRepositories, setGithubRepositories] = useState<string[]>([]);
  const [selectedGithubRepository, setSelectedGithubRepository] = useState("");

  // Phase 28.1 - GitHub Branch Support
  const [githubBranches, setGithubBranches] = useState<string[]>([]);

  const [selectedGithubBranch, setSelectedGithubBranch] =
    useState("main");

  const [analysisStatus, setAnalysisStatus] = useState<"idle" | "analyzing" | "complete">("idle");

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function fetchRepositories() {
      setLoading(true);
      try {
        const repos = await getMyRepositories();
        setRepositories(repos || []);
        if (repos && repos.length > 0) {
          setSelectedRepository(repos[0].repository_id);
        }
      } catch (err) {
        setRepositories([]);
      } finally {
        setLoading(false);
      }
    }
    fetchRepositories();
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem(CHAT_STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setMessages(parsed);
      } catch {
        // ignore parse errors
      }
    }
  }, []);

  useEffect(() => {
    const githubData = localStorage.getItem("devpilot_github");
    if (githubData) {
      try {
        const parsed = JSON.parse(githubData);
        if (parsed.connected === true && typeof parsed.username === "string") {
          setGithubConnected(true);
          setGithubUsername(parsed.username);
          if (Array.isArray(parsed.repositories)) {
            setGithubRepositories(parsed.repositories);
            if (parsed.repositories.length > 0) {
                setSelectedGithubRepository(parsed.repositories[0]);
                fetchGithubBranches(parsed.repositories[0]);
            }
          }
        }
      } catch {
        // ignore parse errors
      }
    }
  }, []);

  // Phase 27.8: Handle GitHub OAuth redirect query parameters
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const connected = params.get("connected");
    const username = params.get("username");
    const avatar_url = params.get("avatar_url");
    const repositories = params.get("repositories");
    if (connected === "true") {
      const repoArray =
        typeof repositories === "string" && repositories.length > 0
          ? repositories.split(",")
          : [];
      const githubObj = {
        connected: true,
        username,
        avatar_url,
        repositories: repoArray,
      };
      localStorage.setItem("devpilot_github", JSON.stringify(githubObj));
      setGithubConnected(true);
      setGithubUsername(username || "");
      setGithubRepositories(repoArray);
      if (repoArray.length > 0) {
        setSelectedGithubRepository(repoArray[0]);
      }
      window.history.replaceState({}, document.title, "/chat");
    }
  }, []);

  useEffect(() => {
    // Scroll to bottom of messages when messages change
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  useEffect(() => {
    localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  const useSuggestedPrompt = (prompt: string) => {
    setQuestion(prompt);
  };

  const connectGithub = () => {
    window.location.href = "http://localhost:8000/auth/github";
  };

  const fetchGithubBranches = async (repository: string, refresh = false) => {
    if (!repository || !githubUsername) return;

    try {
      const response = await fetch(
        `http://localhost:8000/github/branches?username=${githubUsername}&repository=${repository}&refresh=${refresh}`
      );

      if (!response.ok) {
        throw new Error("Unable to fetch branches");
      }

      const data = await response.json();

      setGithubBranches(data.branches || []);

      if (data.branches?.length > 0) {
        setSelectedGithubBranch(data.branches[0]);
      }
    } catch (error) {
      console.error(error);
    }
  };

  // Phase 27.9: Allow direct GitHub repository analysis from the chat page
  const importGithubRepository = async () => {
    if (!selectedGithubRepository) return;

    try {
      setAnalysisStatus("analyzing");
      const response = await fetch("http://localhost:8000/github/import", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repository: selectedGithubRepository,
          username: githubUsername,
          branch: selectedGithubBranch,
        }),
      });

      if (!response.ok) {
        throw new Error("Import failed");
      }

      setAnalysisStatus("complete");
      alert("Repository imported successfully. Refreshing repository list...");

      const repos = await getMyRepositories();
      setRepositories(repos || []);
      if (repos && repos.length > 0) {
        setSelectedRepository(repos[0].repository_id);
      }
    } catch (err) {
      setAnalysisStatus("idle");
      alert("Unable to import the selected GitHub repository.");
    }
  };

  const newChat = () => {
    setMessages([]);
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem(CHAT_STORAGE_KEY);
  };

  async function sendMessage() {
    if (question.trim() === "" || !selectedRepository) return;
    const userQuestion = question;
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      },
    ]);
    setQuestion("");
    setSending(true);
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          repository_id: selectedRepository,
          question: userQuestion,
          repository_context: repositoryContext,
        }),
      });
      // Phase 26.3: Using a normal JSON response.
      // In Phase 26.4 this will be replaced with streaming once the backend
      // exposes a streaming endpoint such as POST /chat/stream.
      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer || data.response || "No response received.",
          sources: data.sources || [],
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Unable to contact the AI service.",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  const selectedRepo = repositories.find(
    (repo) => repo.repository_id === selectedRepository
  );

  const repositoryContext = selectedRepo
    ? {
        name: selectedRepo.repository_id,
        files: selectedRepo.total_files,
        summary: selectedRepo.summary || "No summary available.",
      }
    : null;

  const renderMessage = (content: string) => {
    return content.split("\n").map((line, index) => {
      if (line.startsWith("### ")) {
        return <h3 key={index} className="text-lg font-bold mt-3 mb-1">{line.replace("### ", "")}</h3>;
      }
      if (line.startsWith("## ")) {
        return <h2 key={index} className="text-xl font-bold mt-3 mb-1">{line.replace("## ", "")}</h2>;
      }
      if (line.startsWith("# ")) {
        return <h1 key={index} className="text-2xl font-bold mt-3 mb-2">{line.replace("# ", "")}</h1>;
      }
      if (line.startsWith("- ")) {
        return <li key={index} className="ml-5 list-disc">{line.substring(2)}</li>;
      }
      if (line.startsWith("`") && line.endsWith("`") && line.length > 2) {
        return <code key={index} className="bg-gray-800 text-green-300 px-2 py-1 rounded font-mono">{line.slice(1, -1)}</code>;
      }
      return <p key={index} className="mb-1 whitespace-pre-wrap">{line}</p>;
    });
  };

  const copyMessage = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {}
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4 py-8">
      <div className="w-full max-w-2xl">
        <h1 className="text-3xl font-bold text-center mb-8">DevPilot AI Chat</h1>
        <div className="mb-6 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-lg font-semibold">GitHub Integration</h2>
              <p className="text-sm text-gray-600">
                Connect your GitHub account to import repositories directly.
              </p>
              {githubConnected && githubRepositories.length > 0 && (
                <div className="mt-4">
                  <label className="mb-1 block text-sm font-medium">GitHub Repository</label>
                  <select
                    value={selectedGithubRepository}
                    onChange={(e) => {
                      const repo = e.target.value;
                      setSelectedGithubRepository(repo);
                      fetchGithubBranches(repo);
                    }}
                    className="w-full rounded border px-3 py-2"
                  >
                    {githubRepositories.map((repo) => (
                      <option key={repo} value={repo}>
                        {repo}
                      </option>
                    ))}
                  </select>

                  <label className="mt-3 mb-1 block text-sm font-medium">
                    Branch
                  </label>

                  <select
                    value={selectedGithubBranch}
                    onChange={(e) => setSelectedGithubBranch(e.target.value)}
                    className="w-full rounded border px-3 py-2"
                  >
                    {githubBranches.map((branch) => (
                      <option
                        key={branch}
                        value={branch}
                      >
                        {branch}
                      </option>
                    ))}
                  </select>

                  {/* Phase 27.9: Import GitHub repository button */}
                  <button
                    onClick={importGithubRepository}
                    className="mt-3 rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
                  >
                    Import Repository
                  </button>
                  <button
                    onClick={() => fetchGithubBranches(selectedGithubRepository, true)}
                    className="mt-2 rounded border border-gray-300 px-4 py-2 hover:bg-gray-100"
                  >
                    Refresh Branches
                  </button>
                  <p className="mt-2 text-xs text-gray-500">
                    Repository import from GitHub will be enabled after backend OAuth synchronization.
                  </p>
                </div>
              )}
            </div>
            {githubConnected ? (
              <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
                Connected as {githubUsername || "GitHub User"}
              </span>
            ) : (
              <button
                onClick={connectGithub}
                className="rounded bg-black px-4 py-2 text-center text-white hover:bg-gray-800"
              >
                Connect GitHub
              </button>
            )}
          </div>
        </div>
        <div className="flex justify-end gap-2 mb-4">
          <button
            onClick={newChat}
            className="px-3 py-2 border rounded hover:bg-gray-100"
          >
            New Chat
          </button>
          <button
            onClick={clearChat}
            className="px-3 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Clear Chat
          </button>
        </div>
        <div className="mb-6 flex flex-col md:flex-row md:items-center gap-4">
          <label htmlFor="repo-select" className="font-medium min-w-[120px]">
            Repository
          </label>
          <select
            id="repo-select"
            className="flex-1 border rounded px-3 py-2"
            value={selectedRepository}
            disabled={repositories.length === 0 || loading}
            onChange={(e) => setSelectedRepository(e.target.value)}
          >
            {repositories.map((repo) => (
              <option key={repo.repository_id} value={repo.repository_id}>
                {repo.repository_id}
              </option>
            ))}
          </select>
        </div>
        <p className="mb-4 text-xs text-gray-500">
          Future versions will automatically sync repositories and branches from GitHub.
        </p>

        {repositories.length === 0 && !loading ? (
          <div className="border border-yellow-400 bg-yellow-50 rounded p-6 mb-8 flex flex-col items-center">
            <div className="text-yellow-700 font-semibold mb-2">
              No repositories available. Upload a repository before using AI Chat.
            </div>
            <a
              href="/upload"
              className="mt-2 inline-block px-4 py-2 bg-yellow-400 text-white rounded hover:bg-yellow-500 font-medium"
            >
              Go to Upload
            </a>
          </div>
        ) : (
          <div className="border border-blue-300 bg-blue-50 rounded p-6 mb-8">
            <div className="mb-2">
              <span className="font-semibold">Selected Repository:</span>{" "}
              {selectedRepo?.repository_id || "-"}
            </div>
            <div className="mb-2">
              <span className="font-semibold">Total Files:</span>{" "}
              {selectedRepo?.total_files ?? "-"}
            </div>
            <div>
              <span className="font-semibold">Summary:</span>{" "}
              {selectedRepo?.summary
                ? selectedRepo.summary
                : "No summary available."}
            </div>
            <div className="mt-4 border-t pt-4">
              <h3 className="font-semibold mb-2">Repository Context</h3>
              <div className="text-sm text-gray-700 space-y-1">
                <p><strong>Name:</strong> {repositoryContext?.name}</p>
                <p><strong>Indexed Files:</strong> {repositoryContext?.files}</p>
                <p className="text-gray-600">
                  This context will automatically be used to answer AI questions.
                </p>
                <div className="mt-4 rounded border bg-gray-50 p-3">
                  <h4 className="font-semibold mb-2">Repository Analysis</h4>
                  {analysisStatus === "idle" && (
                    <p className="text-sm text-gray-600">No analysis running.</p>
                  )}
                  {analysisStatus === "analyzing" && (
                    <p className="text-sm text-blue-600">Analyzing repository, indexing files, and preparing AI context...</p>
                  )}
                  {analysisStatus === "complete" && (
                    <p className="text-sm text-green-600">Analysis complete. Repository is ready for AI questions.</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Chat UI */}
        <div className="border border-gray-300 bg-white rounded-lg p-4 flex flex-col min-h-[340px]">
          <div className="mb-3 rounded border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">
            AI is currently answering questions using the selected repository context.
          </div>
          <div className="flex flex-col flex-1 overflow-y-auto mb-4 max-h-72">
            {messages.length === 0 && (
              <div className="text-gray-500 text-center mt-4 mb-4">
                <h2 className="text-2xl font-bold mb-2">Welcome to DevPilot AI</h2>
                <p>
                  Select a repository and start asking questions about your code.
                </p>
              </div>
            )}
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex mb-2 ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`rounded px-4 py-2 max-w-[80%] break-words ${
                    msg.role === "user"
                      ? "bg-blue-500 text-white self-end"
                      : "bg-gray-200 text-gray-800 self-start"
                  }`}
                >
                  {msg.role === "assistant" ? renderMessage(msg.content) : msg.content}
                  <div className="mt-2 flex items-center justify-between text-[11px] text-gray-500">
                    <span>{msg.timestamp}</span>
                    {msg.role === "assistant" && (
                      <button
                        onClick={() => copyMessage(msg.content)}
                        className="hover:text-blue-600"
                      >
                        Copy
                      </button>
                    )}
                  </div>
                  {msg.role === "assistant" && msg.sources && msg.sources.length > 0 && (
                    <div className="mt-3 border-t pt-2">
                      <p className="text-xs font-semibold text-gray-600 mb-1">Sources</p>
                      <ul className="text-xs text-blue-700 space-y-1">
                        {msg.sources.map((source, index) => (
                          <li key={index}>📄 {source}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {sending && (
              <div className="flex justify-start mb-2">
                <div className="rounded px-4 py-2 bg-gray-200 text-gray-600 italic">
                  DevPilot AI is thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="text-xs text-gray-500 text-center mb-3">
            AI answers can include the repository files used to generate each response.
          </div>
          <div className="text-sm font-medium text-gray-600 mb-2">
            Suggested Prompts
          </div>
          <div className="flex gap-3 mb-3 flex-wrap justify-center">
            <button
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded font-medium hover:bg-gray-300 transition-colors"
              onClick={() => useSuggestedPrompt("Explain this project architecture.")}
            >
              Explain Project
            </button>
            <button
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded font-medium hover:bg-gray-300 transition-colors"
              onClick={() => useSuggestedPrompt("Find potential bugs and code smells.")}
            >
              Find Bugs
            </button>
            <button
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded font-medium hover:bg-gray-300 transition-colors"
              onClick={() => useSuggestedPrompt("Generate documentation for this repository.")}
            >
              Generate Documentation
            </button>
          </div>
          <textarea
            className="w-full border rounded p-3 resize-none text-gray-800 bg-white mb-2"
            rows={3}
            placeholder="Ask a question about your code..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                if (!sending && selectedRepository) {
                  sendMessage();
                }
              }
            }}
            disabled={sending || !selectedRepository}
          />
          <button
            className={`w-full py-2 rounded font-semibold ${
              sending || !selectedRepository
                ? "bg-blue-200 text-white cursor-not-allowed"
                : "bg-blue-600 text-white hover:bg-blue-700"
            }`}
            onClick={sendMessage}
            disabled={sending || !selectedRepository}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}