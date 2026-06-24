

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function request(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        },
        ...options
    });

    if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
}

export const api = {
    getRepositoryDashboard: (repositoryId: string) =>
        request(`/repository/${repositoryId}/dashboard`),

    searchRepository: (
        repositoryId: string,
        query: string
    ) =>
        request(`/repository/${repositoryId}/search`, {
            method: 'POST',
            body: JSON.stringify({ query })
        }),

    getHealth: (repositoryId: string) =>
        request(`/repository/${repositoryId}/health`),

    getRiskReport: (repositoryId: string) =>
        request(`/repository/${repositoryId}/risk-report`),

    getBugFixes: (repositoryId: string) =>
        request(`/repository/${repositoryId}/bug-fixes`),

    getRefactorPlan: (repositoryId: string) =>
        request(`/repository/${repositoryId}/refactor-plan`),

    getDependencyAnalysis: (repositoryId: string) =>
        request(`/repository/${repositoryId}/dependency-analysis`),

    getReleaseNotes: (repositoryId: string) =>
        request(`/repository/${repositoryId}/release-notes`),

    getPRSummary: (repositoryId: string) =>
        request(`/repository/${repositoryId}/pr-summary`)
};