'use client';

import { useEffect, useState } from 'react';
import { api } from '../../../services/api';
import { chatWithRepo } from "../../../services/chat";
import { getRepositoryDetails } from '../../../services/repositoryDetails';
import { getFileContent } from '../../../services/fileContent';
import { getAudit } from "../../../services/audit";
import jsPDF from 'jspdf';

interface RepositoryDetails {
    repository_id: string;
    summary?: string;
    total_files?: number;
    files?: string[];
    health_score?: number;
}

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
    const [repositoryDetails, setRepositoryDetails] =
        useState<RepositoryDetails | null>(null);
    const [selectedFile, setSelectedFile] = useState<string | null>(null);
    const [fileContent, setFileContent] = useState<string>('');
    const [fileExplanation, setFileExplanation] = useState<string>('');
    const [explainingFile, setExplainingFile] = useState(false);
    const [fileReview, setFileReview] = useState<string>('');
    const [reviewingFile, setReviewingFile] = useState(false);
    const [audit, setAudit] = useState<any>(null);
    const [qualityMetrics, setQualityMetrics] = useState({
        healthScore: 0,
        maintainabilityScore: 0,
        technicalDebtScore: 0,
        architectureRisk: 'Low'
    });
    const [architectureData] = useState({
        layers: [
            'Frontend',
            'API Layer',
            'Services',
            'Repository Store'
        ]
    });

    const [advancedInsights, setAdvancedInsights] = useState({
        orphanFiles: [] as string[],
        largeFiles: [] as string[],
        hotspotFiles: [] as string[],
        refactoringCandidates: [] as any[],
        modernizationRoadmap: [] as string[],
    });

    const [executiveReport, setExecutiveReport] = useState({
        strengths: [] as string[],
        risks: [] as string[],
        nextActions: [] as string[],
    });

    const [ctoVerdict, setCtoVerdict] = useState({
        verdict: 'Unknown',
        productionReadiness: 0,
        securityRisk: 'Low',
        testCoverage: 'Unknown',
    });

    const [projectGrade, setProjectGrade] = useState({
        grade: 'C',
        hiringReadiness: 0,
        openSourceReadiness: 0,
        readmeSuggestions: [] as string[],
    });

    const [deploymentReadiness, setDeploymentReadiness] = useState({
        ciCdReady: false,
        documentationReady: false,
        testingReady: false,
        deploymentScore: 0,
    });

    const [collaborationCenter] = useState({
        shareableLink:
            typeof window !== 'undefined'
                ? window.location.href
                : '',
        pdfExportReady: true,
        githubIntegration: 'Available',
        teamWorkspace: 'Planned',
        githubConnected: false,
    });

    const connectGithub = () => {
        alert(
            'GitHub OAuth integration placeholder. Backend OAuth flow will be connected in a later phase.'
        );
    };

    const exportAuditPdf = () => {
        const pdf = new jsPDF();

        pdf.setFontSize(18);
        pdf.text('DevPilot Repository Audit Report', 20, 20);

        pdf.setFontSize(12);

        pdf.text(
            `Repository: ${dashboard?.repository_id || 'Unknown'}`,
            20,
            40
        );

        pdf.text(
            `Health Score: ${qualityMetrics.healthScore}%`,
            20,
            50
        );

        pdf.text(
            `Maintainability: ${qualityMetrics.maintainabilityScore}%`,
            20,
            60
        );

        pdf.text(
            `Architecture Risk: ${qualityMetrics.architectureRisk}`,
            20,
            70
        );

        pdf.text(
            `CTO Verdict: ${ctoVerdict.verdict}`,
            20,
            80
        );

        pdf.text(
            `Production Readiness: ${ctoVerdict.productionReadiness}%`,
            20,
            90
        );

        pdf.text(
            `Project Grade: ${projectGrade.grade}`,
            20,
            100
        );

        pdf.text('Recommended Actions:', 20, 120);

        executiveReport.nextActions.forEach((action, index) => {
            pdf.text(`- ${action}`, 25, 130 + index * 10);
        });

        pdf.save(`devpilot-${params.id}-report.pdf`);
    };

    const [dependencyGraph, setDependencyGraph] = useState<any[]>([]);
    const [architectureMetrics, setArchitectureMetrics] = useState({
        circularDependencies: 0,
        riskLevel: 'Low',
        mostConnectedFile: 'N/A'
    });

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

        getRepositoryDetails(params.id)
            .then(setRepositoryDetails)
            .catch(console.error);

        getAudit(params.id)
            .then((data) => {
                setAudit(data);

                setQualityMetrics({
                    healthScore: data.health_score || 0,
                    maintainabilityScore: data.maintainability_score || 0,
                    technicalDebtScore: data.technical_debt_score || 0,
                    architectureRisk: data.architecture_risk || 'Low'
                });

                setAdvancedInsights({
                    orphanFiles: data.orphan_files || [],
                    largeFiles: data.large_files || [],
                    hotspotFiles: data.hotspot_files || [],
                    refactoringCandidates: data.refactoring_candidates || [],
                    modernizationRoadmap: data.modernization_roadmap || [],
                });

                setExecutiveReport({
                    strengths: [
                        `Health Score: ${data.health_score || 0}%`,
                        `Maintainability: ${data.maintainability_score || 0}%`,
                        `Architecture Risk: ${data.architecture_risk || 'Low'}`,
                    ],
                    risks: [
                        `${(data.orphan_files || []).length} orphan files detected`,
                        `${(data.large_files || []).length} large files detected`,
                        `${(data.hotspot_files || []).length} complexity hotspots detected`,
                    ],
                    nextActions: data.modernization_roadmap || [],
                });

                // CTO Verdict logic
                const health = data.health_score || 0;

                let verdict = 'Needs Improvement';

                if (health >= 90) {
                    verdict = 'Excellent';
                } else if (health >= 75) {
                    verdict = 'Good';
                }

                setCtoVerdict({
                    verdict,
                    productionReadiness: Math.min(
                        100,
                        (data.health_score || 0)
                    ),
                    securityRisk:
                        (data.hotspot_files || []).length > 3
                            ? 'Medium'
                            : 'Low',
                    testCoverage:
                        (data.total_files || 0) > 0
                            ? 'Not Yet Measured'
                            : 'Unknown',
                });

                // Project Grade logic
                let grade = 'C';

                if ((data.health_score || 0) >= 90) {
                    grade = 'A+';
                } else if ((data.health_score || 0) >= 80) {
                    grade = 'A';
                } else if ((data.health_score || 0) >= 70) {
                    grade = 'B';
                }

                setProjectGrade({
                    grade,
                    hiringReadiness: Math.min(100, data.health_score || 0),
                    openSourceReadiness: Math.min(
                        100,
                        (data.maintainability_score || 0)
                    ),
                    readmeSuggestions: [
                        'Add project architecture diagram',
                        'Add installation guide',
                        'Add API documentation',
                        'Add contribution guidelines',
                        'Add deployment instructions'
                    ]
                });

                setDeploymentReadiness({
                    ciCdReady: (data.health_score || 0) >= 80,
                    documentationReady:
                        (data.maintainability_score || 0) >= 70,
                    testingReady:
                        (data.technical_debt_score || 100) < 40,
                    deploymentScore: Math.round(
                        ((data.health_score || 0) +
                        (data.maintainability_score || 0)) / 2
                    ),
                });
            })
            .catch(console.error);

        fetch(`http://localhost:8000/repository/${params.id}/dependencies`)
            .then((res) => res.json())
            .then((data) => {
                const deps = data.dependencies || [];

                setDependencyGraph(deps);

                let mostConnectedFile = 'N/A';
                let maxConnections = 0;

                deps.forEach((node: any) => {
                    const count = node.dependsOn?.length || 0;

                    if (count > maxConnections) {
                        maxConnections = count;
                        mostConnectedFile = node.file;
                    }
                });

                setArchitectureMetrics({
                    circularDependencies: data.circular_dependencies || 0,
                    riskLevel: data.architecture_risk || 'Low',
                    mostConnectedFile,
                });
            })
            .catch(console.error);
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

            {/* REPOSITORY DETAILS */}
            {repositoryDetails && (
                <div className='border rounded-lg p-5 bg-white'>

                    <h2 className='text-xl font-semibold mb-4'>
                        Repository Details
                    </h2>

                    <p>
                        <strong>ID:</strong> {repositoryDetails.repository_id}
                    </p>

                    <p>
                        <strong>Total Files:</strong> {repositoryDetails.total_files ?? 0}
                    </p>

                    <p>
                        <strong>Health Score:</strong> {repositoryDetails.health_score ?? 0}%
                    </p>

                    <div className='mt-4'>
                        <h3 className='font-semibold mb-2'>Summary</h3>
                        <p>
                            {repositoryDetails.summary || 'No summary available'}
                        </p>
                    </div>

                    <div className='mt-4'>
                        <h3 className='font-semibold mb-2'>Files</h3>

                        <ul className='list-disc pl-6'>
                            {(repositoryDetails.files || []).map((file, index) => (
                                <li key={index}>{file}</li>
                            ))}
                        </ul>
                    </div>

                </div>
            )}

            {audit && (

                <div className="border rounded-lg p-5 bg-white">

                    <h2 className="text-xl font-semibold mb-4">
                        Repository Audit
                    </h2>

                    <p>
                        Health Score: {audit.health_score}%
                    </p>

                    <p>
                        Files: {audit.total_files}
                    </p>

                    <p>
                        Total Lines: {audit.total_lines}
                    </p>

                    <p>
                        Warnings: {audit.warnings}
                    </p>

                    <h3 className="mt-4 font-semibold">
                        Risky Files
                    </h3>

                    <ul>
                        {audit.risky_files.map(
                            (file: any, index: number) => (
                                <li key={index}>
                                    {file.file} ({file.issues} issues)
                                </li>
                            )
                        )}
                    </ul>

                </div>

            )}

            {/* QUALITY DASHBOARD */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    Repository Quality Dashboard
                </h2>

                <div className='grid md:grid-cols-4 gap-4'>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Health Score</p>
                        <p className='text-2xl font-bold'>
                            {qualityMetrics.healthScore}%
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Maintainability</p>
                        <p className='text-2xl font-bold'>
                            {qualityMetrics.maintainabilityScore}%
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Technical Debt</p>
                        <p className='text-2xl font-bold'>
                            {qualityMetrics.technicalDebtScore}
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Architecture Risk</p>
                        <p className='text-2xl font-bold'>
                            {qualityMetrics.architectureRisk}
                        </p>
                    </div>

                </div>

            </div>

            {/* ADVANCED ENGINEERING INSIGHTS */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    Engineering Insights
                </h2>

                <div className='grid md:grid-cols-2 gap-4'>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold mb-2'>
                            Refactoring Candidates
                        </h3>

                        {advancedInsights.refactoringCandidates.length === 0 ? (
                            <p>No refactoring candidates detected.</p>
                        ) : (
                            advancedInsights.refactoringCandidates.map((item: any, idx: number) => (
                                <div key={idx} className='mb-2'>
                                    <strong>{item.file}</strong>
                                    <div>{item.reason}</div>
                                    <div className='text-sm text-gray-500'>
                                        Priority: {item.priority}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold mb-2'>
                            Complexity Hotspots
                        </h3>

                        <ul className='list-disc pl-5'>
                            {advancedInsights.hotspotFiles.map((file, idx) => (
                                <li key={idx}>{file}</li>
                            ))}
                        </ul>
                    </div>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold mb-2'>
                            Large Files
                        </h3>

                        <ul className='list-disc pl-5'>
                            {advancedInsights.largeFiles.map((file, idx) => (
                                <li key={idx}>{file}</li>
                            ))}
                        </ul>
                    </div>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold mb-2'>
                            Orphan Files
                        </h3>

                        <ul className='list-disc pl-5'>
                            {advancedInsights.orphanFiles.map((file, idx) => (
                                <li key={idx}>{file}</li>
                            ))}
                        </ul>
                    </div>

                </div>

                <div className='mt-4 border-t pt-4'>
                    <h3 className='font-semibold mb-2'>
                        Modernization Roadmap
                    </h3>

                    <ol className='list-decimal pl-5'>
                        {advancedInsights.modernizationRoadmap.map((step, idx) => (
                            <li key={idx}>{step}</li>
                        ))}
                    </ol>
                </div>

            </div>

            {/* EXECUTIVE AI REPORT */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    Executive AI Report
                </h2>

                <div className='grid md:grid-cols-3 gap-4'>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold mb-2'>Repository Strengths</h3>
                        <ul className='list-disc pl-5'>
                            {executiveReport.strengths.map((item, idx) => (
                                <li key={idx}>{item}</li>
                            ))}
                        </ul>
                    </div>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold mb-2'>Key Risks</h3>
                        <ul className='list-disc pl-5'>
                            {executiveReport.risks.map((item, idx) => (
                                <li key={idx}>{item}</li>
                            ))}
                        </ul>
                    </div>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold mb-2'>Recommended Actions</h3>
                        <ol className='list-decimal pl-5'>
                            {executiveReport.nextActions.map((item, idx) => (
                                <li key={idx}>{item}</li>
                            ))}
                        </ol>
                    </div>

                </div>

            </div>

            {/* CTO FINAL VERDICT */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    CTO Repository Verdict
                </h2>

                <div className='grid md:grid-cols-4 gap-4'>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Verdict</p>
                        <p className='text-xl font-bold'>
                            {ctoVerdict.verdict}
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Production Readiness</p>
                        <p className='text-xl font-bold'>
                            {ctoVerdict.productionReadiness}%
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Security Risk</p>
                        <p className='text-xl font-bold'>
                            {ctoVerdict.securityRisk}
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Test Coverage</p>
                        <p className='text-xl font-bold'>
                            {ctoVerdict.testCoverage}
                        </p>
                    </div>

                </div>

            </div>

            {/* PROJECT READINESS REPORT */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    Project Readiness Report
                </h2>

                <div className='grid md:grid-cols-3 gap-4 mb-4'>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Project Grade</p>
                        <p className='text-2xl font-bold'>
                            {projectGrade.grade}
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Hiring Readiness</p>
                        <p className='text-2xl font-bold'>
                            {projectGrade.hiringReadiness}%
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Open Source Readiness</p>
                        <p className='text-2xl font-bold'>
                            {projectGrade.openSourceReadiness}%
                        </p>
                    </div>

                </div>

                <div className='border rounded-lg p-4'>
                    <h3 className='font-semibold mb-2'>README Improvement Suggestions</h3>

                    <ul className='list-disc pl-5'>
                        {projectGrade.readmeSuggestions.map((item, idx) => (
                            <li key={idx}>{item}</li>
                        ))}
                    </ul>
                </div>

            </div>

            {/* DEPLOYMENT & COLLABORATION */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    Deployment & Collaboration Center
                </h2>

                <div className='grid md:grid-cols-4 gap-4 mb-4'>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Deployment Score</p>
                        <p className='text-2xl font-bold'>
                            {deploymentReadiness.deploymentScore}%
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>CI/CD Ready</p>
                        <p className='font-bold'>
                            {deploymentReadiness.ciCdReady ? 'Yes' : 'No'}
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Documentation</p>
                        <p className='font-bold'>
                            {deploymentReadiness.documentationReady ? 'Ready' : 'Needs Work'}
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Testing</p>
                        <p className='font-bold'>
                            {deploymentReadiness.testingReady ? 'Ready' : 'Needs Work'}
                        </p>
                    </div>

                </div>

                <div className='border rounded-lg p-4'>
                    <h3 className='font-semibold mb-2'>Deployment Checklist</h3>

                    <ul className='list-disc pl-5'>
                        <li>README completed</li>
                        <li>Environment variables documented</li>
                        <li>CI/CD pipeline configured</li>
                        <li>Testing strategy defined</li>
                        <li>Production deployment plan prepared</li>
                    </ul>
                </div>

            </div>

            {/* REPORT SHARING CENTER */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    Report Sharing Center
                </h2>

                <div className='grid md:grid-cols-4 gap-4 mb-4'>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>PDF Export</p>
                        <p className='font-bold mb-2'>
                            {collaborationCenter.pdfExportReady ? 'Ready' : 'Unavailable'}
                        </p>

                        <button
                            onClick={exportAuditPdf}
                            className='border rounded px-3 py-1 text-sm'
                        >
                            Download PDF
                        </button>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>GitHub Integration</p>

                        <p className='font-bold mb-2'>
                            {collaborationCenter.githubIntegration}
                        </p>

                        <button
                            onClick={connectGithub}
                            className='border rounded px-3 py-1 text-sm'
                        >
                            Connect GitHub
                        </button>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Team Workspace</p>
                        <p className='font-bold'>
                            {collaborationCenter.teamWorkspace}
                        </p>
                    </div>

                    <div className='border rounded-lg p-4 text-center'>
                        <p className='text-sm text-gray-500'>Share Audit</p>
                        <button
                            onClick={() => {
                                navigator.clipboard.writeText(
                                    collaborationCenter.shareableLink
                                );
                                alert('Repository link copied');
                            }}
                            className='border rounded px-3 py-1 mt-2'
                        >
                            Copy Link
                        </button>
                    </div>

                </div>

                <div className='border rounded-lg p-4'>
                    <h3 className='font-semibold mb-2'>Upcoming Collaboration Features</h3>

                    <ul className='list-disc pl-5'>
                        <li>PDF Audit Export</li>
                        <li>Shareable Public Reports</li>
                        <li>GitHub OAuth Connection</li>
                        <li>Pull Request Review Assistant</li>
                        <li>Team Collaboration Workspace</li>
                    </ul>
                </div>

            </div>

            {/* GITHUB INTEGRATION CENTER */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    GitHub Integration Center
                </h2>

                <div className='grid md:grid-cols-3 gap-4'>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold'>OAuth Status</h3>
                        <p className='text-sm mt-2'>
                            Not Connected
                        </p>
                    </div>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold'>Pull Request Reviews</h3>
                        <p className='text-sm mt-2'>
                            Planned Feature
                        </p>
                    </div>

                    <div className='border rounded-lg p-4'>
                        <h3 className='font-semibold'>Repository Sync</h3>
                        <p className='text-sm mt-2'>
                            Planned Feature
                        </p>
                    </div>

                </div>

            </div>

            {/* ARCHITECTURE OVERVIEW */}
            <div className='border rounded-lg p-5 bg-white'>

                <h2 className='text-xl font-semibold mb-4'>
                    Architecture Overview
                </h2>

                <p className='text-gray-600 mb-4'>
                    Repository dependency and architecture mapping.
                </p>

                <div className='grid md:grid-cols-4 gap-3'>

                    {architectureData.layers.map((layer, index) => (
                        <div
                            key={index}
                            className='border rounded-lg p-4 text-center'
                        >
                            <p className='font-semibold'>
                                {layer}
                            </p>
                        </div>
                    ))}

                </div>

                <div className='mt-4 border-t pt-4'>
                    <h3 className='font-semibold mb-4'>
                        Dependency Graph
                    </h3>

                    <div className='space-y-3 mb-6'>
                        {dependencyGraph.map((node, index) => (
                            <div
                                key={index}
                                className='border rounded-lg p-3'
                            >
                                <p className='font-semibold'>
                                    {node.file}
                                </p>
                                <p className='text-sm text-gray-600'>
                                    Depends on:
                                    {
                                        node.dependsOn.length
                                            ? ` ${node.dependsOn.join(', ')}`
                                            : ' None'
                                    }
                                </p>
                            </div>
                        ))}
                    </div>

                    <div className='grid grid-cols-2 md:grid-cols-4 gap-3 mb-4'>
                        <div className='border rounded p-3 text-center'>
                            <p className='text-sm'>Nodes</p>
                            <p className='font-bold'>{dependencyGraph.length}</p>
                        </div>
                        <div className='border rounded p-3 text-center'>
                            <p className='text-sm'>Connections</p>
                            <p className='font-bold'>
                                {dependencyGraph.reduce(
                                    (total, node) => total + (node.dependsOn?.length || 0),
                                    0
                                )}
                            </p>
                        </div>
                        <div className='border rounded p-3 text-center'>
                            <p className='text-sm'>Circular Dependencies</p>
                            <p className='font-bold'>
                                {architectureMetrics.circularDependencies}
                            </p>
                        </div>
                        <div className='border rounded p-3 text-center'>
                            <p className='text-sm'>Architecture Risk</p>
                            <p className='font-bold'>
                                {architectureMetrics.riskLevel}
                            </p>
                        </div>
                    </div>

                    <div className='border rounded-lg p-3 mb-4'>
                        <p>
                            <strong>Most Connected File:</strong>
                            {' '}
                            {architectureMetrics.mostConnectedFile}
                        </p>
                    </div>

                    <h3 className='font-semibold mb-2'>
                        Planned Dependency Graph
                    </h3>

                    <p className='text-sm text-gray-600'>
                        Phase 22 will automatically analyze imports,
                        module relationships, service dependencies,
                        and generate a real architecture graph.
                    </p>
                </div>

            </div>

            {/* FILE EXPLORER */}
            {repositoryDetails && (
                <div className='border rounded-lg p-5 bg-white'>

                    <h2 className='text-xl font-semibold mb-4'>
                        File Explorer
                    </h2>

                    <div className='grid md:grid-cols-3 gap-4'>

                        <div className='border rounded p-3'>
                            <h3 className='font-semibold mb-2'>Files</h3>

                            {(repositoryDetails.files || []).map((file, index) => (
                                <button
                                    key={index}
                                    onClick={async () => {
                                        setSelectedFile(file);

                                        try {
                                            const response = await getFileContent(
                                                params.id,
                                                file
                                            );

                                            setFileContent(
                                                response.content || 'No content available'
                                            );
                                        } catch (error) {
                                            console.error(error);
                                            setFileContent('Failed to load file content');
                                        }
                                    }}
                                    className='block w-full text-left border rounded p-2 mb-2 hover:bg-gray-50'
                                >
                                    {file}
                                </button>
                            ))}
                        </div>

                        <div className='md:col-span-2 border rounded p-3'>

                            <h3 className='font-semibold mb-2'>
                                {selectedFile || 'Select a file'}
                            </h3>

                            {selectedFile && (
                                <>
                                <button
                                    onClick={async () => {
                                        setExplainingFile(true);
                                        try {
                                            const response = await fetch(
                                                `http://localhost:8000/repository/${params.id}/explain-file`,
                                                {
                                                    method: 'POST',
                                                    headers: {
                                                        'Content-Type': 'application/json',
                                                    },
                                                    body: JSON.stringify({
                                                        file_name: selectedFile,
                                                    }),
                                                }
                                            );

                                            const data = await response.json();

                                            setFileExplanation(
                                                data.explanation || 'No explanation available'
                                            );
                                        } catch (error) {
                                            console.error(error);
                                            setFileExplanation(
                                                'Failed to generate AI explanation'
                                            );
                                        } finally {
                                            setExplainingFile(false);
                                        }
                                    }}
                                    className='mb-3 border rounded px-3 py-2'
                                >
                                    Explain This File
                                </button>
                                <button
                                    onClick={async () => {
                                        if (!selectedFile) return;

                                        setReviewingFile(true);

                                        try {
                                            const response = await fetch(
                                                `http://localhost:8000/repository/${params.id}/review-file`,
                                                {
                                                    method: 'POST',
                                                    headers: {
                                                        'Content-Type': 'application/json',
                                                    },
                                                    body: JSON.stringify({
                                                        file_name: selectedFile,
                                                    }),
                                                }
                                            );

                                            const data = await response.json();

                                            setFileReview(
                                                data.review || 'No review available'
                                            );
                                        } catch (error) {
                                            console.error(error);

                                            setFileReview(
                                                'Failed to generate code review'
                                            );
                                        } finally {
                                            setReviewingFile(false);
                                        }
                                    }}
                                    className='mb-3 ml-2 border rounded px-3 py-2'
                                >
                                    Detect Bugs & Improvements
                                </button>
                                </>
                            )}

                            <pre className='overflow-auto text-sm whitespace-pre-wrap'>
                                {fileContent || 'Choose a file from the left panel.'}
                            </pre>

                            {explainingFile && (
                                <p className='mt-3 text-gray-500'>
                                    Analyzing file...
                                </p>
                            )}

                            {fileExplanation && (
                                <div className='mt-4 border-t pt-4'>
                                    <h4 className='font-semibold mb-2'>
                                        AI File Explanation
                                    </h4>

                                    <pre className='whitespace-pre-wrap text-sm'>
                                        {fileExplanation}
                                    </pre>
                                </div>
                            )}

                            {reviewingFile && (
                                <p className='mt-3 text-gray-500'>
                                    Running code review...
                                </p>
                            )}

                            {fileReview && (
                                <div className='mt-4 border-t pt-4'>
                                    <h4 className='font-semibold mb-2'>
                                        Bug Detection & Improvement Suggestions
                                    </h4>

                                    <pre className='whitespace-pre-wrap text-sm'>
                                        {fileReview}
                                    </pre>
                                </div>
                            )}

                        </div>

                    </div>

                </div>
            )}

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