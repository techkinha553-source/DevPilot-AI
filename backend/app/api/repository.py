from pathlib import Path
import shutil

from fastapi import APIRouter, HTTPException

from app.services.repository_metadata import load_metadata
from app.services.repository_stats import calculate_repository_stats
from app.services.repository_store import get_repository
from app.services.tech_stack import detect_tech_stack
from app.services.language_stats import detect_languages
from pathlib import Path
from app.services.documentation_generator import (
    generate_documentation
)
from app.services.api_doc_generator import (
    generate_api_docs
)
from app.services.test_case_generator import (
    generate_test_cases
)
from app.services.code_explainer import (
    explain_repository
)
from app.services.bug_fixer import generate_fixes
from app.services.architecture_report import (
    generate_architecture_report
)
from app.services.improvement_service import (
    generate_improvements
)
from app.services.engineering_score import (
    calculate_engineering_score
)
from app.services.executive_report import (
    generate_executive_report
)
from app.models.question import (
    RepositoryQuestion
)

from app.services.repository_qa import (
    answer_repository_question
)

from app.services.dashboard_summary import (
    generate_dashboard_summary
)

from app.models.search_request import (
    SearchRequest
)

from app.services.embedding_service import (
    create_embedding
)

from app.services.repository_search import (
    search_repository
)

from app.services.commit_message_generator import (
    generate_commit_messages
)

from app.services.pr_summary_generator import (
    generate_pr_summary
)

from app.services.release_notes_generator import (
    generate_release_notes
)

from app.services.repository_health import (
    generate_repository_health
)

from app.models.pr_review import (
    PRReviewRequest
)

from app.services.pr_reviewer import (
    review_pull_request
)

from app.services.bug_fix_planner import (
    generate_bug_fix_plan
)

from app.services.refactor_planner import (
    generate_refactor_plan
)

from app.services.dependency_analyzer import (
    analyze_dependencies
)

router = APIRouter()

UPLOAD_DIR = Path("app/uploads")


@router.get("/repositories")
def list_repositories():
    repositories = []

    if not UPLOAD_DIR.exists():
        return {"repositories": repositories}

    for repo_folder in UPLOAD_DIR.iterdir():
        if repo_folder.is_dir():
            try:
                metadata = load_metadata(repo_folder)
                repositories.append(metadata)
            except Exception:
                pass

    return {"repositories": repositories}


@router.get("/repository/{repository_id}")
def repository_info(repository_id: str):
    repo_path = UPLOAD_DIR / repository_id

    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found.")

    metadata = load_metadata(repo_path)
    stats = calculate_repository_stats(str(repo_path))

    return {
        "metadata": metadata,
        "stats": stats,
    }


@router.delete("/repository/{repository_id}")
def delete_repository(repository_id: str):
    repo_path = UPLOAD_DIR / repository_id

    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository not found.")

    shutil.rmtree(repo_path)

    zip_file = UPLOAD_DIR / f"{repository_id}.zip"
    if zip_file.exists():
        zip_file.unlink()

    return {
        "message": "Repository deleted successfully"
    }

@router.get("/repository/{repository_id}/stats")

def repository_stats(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:

        return {

            "error": "Repository not found"

        }

    return calculate_repository_stats(

        repo["documents"]

    )

@router.get("/repository/{repository_id}/tech-stack")
def repository_tech_stack(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return {
        "repository_id": repository_id,
        "tech_stack": detect_tech_stack(
            repo["documents"]
        )
    }

@router.get("/repository/{repository_id}/languages")
def repository_languages(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return {
        "repository_id": repository_id,
        "languages": detect_languages(
            repo["documents"]
        )
    }


# New endpoint: get largest files in repository
@router.get("/repository/{repository_id}/largest-files")
def largest_files(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    files = []

    for doc in repo["documents"]:

        content = doc.get("content", "")

        files.append({
            "path": doc.get("path", "Unknown"),
            "size": len(content)
        })

    files.sort(
        key=lambda x: x["size"],
        reverse=True
    )

    return {
        "repository_id": repository_id,
        "largest_files": files[:10]
    }


# New endpoint: get important files in repository
@router.get("/repository/{repository_id}/important-files")
def important_files(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    important_keywords = [
        "readme",
        "main.py",
        "app.py",
        "server.py",
        "package.json",
        "requirements.txt",
        "dockerfile",
        "docker-compose",
        "next.config",
        "vite.config",
        ".env.example"
    ]

    important = []

    for doc in repo["documents"]:

        path = doc.get("path", "")
        lower_path = path.lower()

        for keyword in important_keywords:

            if keyword in lower_path:

                important.append({
                    "path": path,
                    "reason": f"Matched '{keyword}'"
                })

                break

    return {
        "repository_id": repository_id,
        "important_files": important
    }


# New endpoint: get folder structure of repository
@router.get("/repository/{repository_id}/folder-structure")
def folder_structure(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    folders = {}

    for doc in repo["documents"]:

        path = doc.get("path", "")

        parts = path.split("/")

        current = folders

        for part in parts[:-1]:

            if part not in current:
                current[part] = {}

            current = current[part]

    return {
        "repository_id": repository_id,
        "folder_structure": folders
    }

@router.get("/repository/{repository_id}/insights")
def repository_insights(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    documents = repo["documents"]

    total_files = len(documents)

    largest_file = None
    largest_size = 0

    for doc in documents:

        size = len(doc.get("content", ""))

        if size > largest_size:
            largest_size = size
            largest_file = doc.get("path", "Unknown")

    insights = [
        f"Repository contains {total_files} files.",
        f"Largest file detected: {largest_file} ({largest_size} characters)."
    ]

    paths = [doc.get("path", "").lower() for doc in documents]

    if any("readme" in p for p in paths):
        insights.append("Project documentation is available.")
    else:
        insights.append("README file is missing.")

    if any("test" in p for p in paths):
        insights.append("Test files detected.")
    else:
        insights.append("No obvious test files detected.")

    return {
        "repository_id": repository_id,
        "insights": insights
    }


# New endpoint: get entry points in repository
@router.get("/repository/{repository_id}/entry-points")
def repository_entry_points(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    entry_point_names = [
        "main.py",
        "app.py",
        "server.py",
        "manage.py",
        "index.js",
        "index.ts",
        "main.ts",
        "main.tsx",
        "page.tsx"
    ]

    entry_points = []

    for doc in repo["documents"]:

        path = doc.get("path", "")
        filename = path.split("/")[-1].lower()

        if filename in entry_point_names:
            entry_points.append(path)

    return {
        "repository_id": repository_id,
        "entry_points": entry_points,
        "total_entry_points": len(entry_points)
    }


@router.get("/repository/{repository_id}/dependencies")
def repository_dependencies(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    dependencies = []

    dependency_files = [
        "requirements.txt",
        "package.json",
        "pyproject.toml"
    ]

    for doc in repo["documents"]:

        path = doc.get("path", "")
        filename = path.split("/")[-1].lower()

        if filename in dependency_files:

            dependencies.append({
                "file": path,
                "content_preview": doc.get("content", "")[:1000]
            })

    return {
        "repository_id": repository_id,
        "dependency_files": dependencies,
        "total_dependency_files": len(dependencies)
    }


@router.get("/repository/{repository_id}/architecture")
def repository_architecture(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    architecture = []

    for doc in repo["documents"]:

        path = doc.get("path", "").lower()
        content = doc.get("content", "").lower()

        if "fastapi" in content and "FastAPI Backend" not in architecture:
            architecture.append("FastAPI Backend")

        if "django" in content and "Django Backend" not in architecture:
            architecture.append("Django Backend")

        if "flask" in content and "Flask Backend" not in architecture:
            architecture.append("Flask Backend")

        if "next.config" in path and "Next.js Frontend" not in architecture:
            architecture.append("Next.js Frontend")

        if "react" in content and "React Frontend" not in architecture:
            architecture.append("React Frontend")

        if "express" in content and "Express.js Backend" not in architecture:
            architecture.append("Express.js Backend")

    return {
        "repository_id": repository_id,
        "architecture": architecture,
        "total_components": len(architecture)
    }


# New endpoint: get repository complexity
@router.get("/repository/{repository_id}/complexity")
def repository_complexity(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    total_lines = 0
    function_count = 0
    class_count = 0
    conditional_count = 0
    loop_count = 0

    for doc in repo["documents"]:

        content = doc.get("content", "")

        total_lines += len(content.splitlines())

        function_count += content.count("def ")
        function_count += content.count("function ")

        class_count += content.count("class ")

        conditional_count += content.count("if ")

        loop_count += content.count("for ")
        loop_count += content.count("while ")

    complexity_score = (
        function_count * 2
        + class_count * 3
        + conditional_count
        + loop_count * 2
    )

    return {
        "repository_id": repository_id,
        "total_lines": total_lines,
        "functions": function_count,
        "classes": class_count,
        "conditionals": conditional_count,
        "loops": loop_count,
        "complexity_score": complexity_score
    }


# New endpoint: get repository security issues
@router.get("/repository/{repository_id}/security")
def repository_security(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    security_issues = []

    suspicious_patterns = {
        "OpenAI API Key": "sk-",
        "GitHub Token": "ghp_",
        "AWS Access Key": "AKIA",
        "Password": "password=",
        "Secret": "secret=",
        "API Key": "api_key"
    }

    for doc in repo["documents"]:

        path = doc.get("path", "")
        content = doc.get("content", "")

        for issue_type, pattern in suspicious_patterns.items():

            if pattern.lower() in content.lower():

                security_issues.append({
                    "file": path,
                    "issue": issue_type,
                    "pattern": pattern
                })

    return {
        "repository_id": repository_id,
        "security_issues": security_issues,
        "total_issues": len(security_issues)
    }


# New endpoint: detect potential dead code
@router.get("/repository/{repository_id}/dead-code")
def repository_dead_code(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    dead_code = []

    for doc in repo["documents"]:

        path = doc.get("path", "")
        content = doc.get("content", "")

        if len(content.strip()) == 0:
            dead_code.append({
                "file": path,
                "reason": "Empty file"
            })

        filename = path.split("/")[-1].lower()

        if filename.startswith("old_") or filename.startswith("backup_"):
            dead_code.append({
                "file": path,
                "reason": "Possible backup file"
            })

    return {
        "repository_id": repository_id,
        "dead_code_candidates": dead_code,
        "total_candidates": len(dead_code)
    }


# New endpoint: AI-style repository review
@router.get("/repository/{repository_id}/review")
def repository_review(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    documents = repo["documents"]

    review = []

    paths = [doc.get("path", "").lower() for doc in documents]

    if any("readme" in p for p in paths):
        review.append("Documentation available via README.")
    else:
        review.append("README file is missing.")

    if any("test" in p for p in paths):
        review.append("Testing files detected.")
    else:
        review.append("No test files detected.")

    if any(".env.example" in p for p in paths):
        review.append("Environment template provided.")

    if len(documents) > 50:
        review.append("Large repository with many source files.")

    review.append("Repository successfully indexed by DevPilot AI.")

    return {
        "repository_id": repository_id,
        "review": review,
        "review_score": max(1, min(10, len(review) + 4))
    }


# New endpoint: detect code smells
@router.get("/repository/{repository_id}/code-smells")
def repository_code_smells(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    smells = []

    for doc in repo["documents"]:

        path = doc.get("path", "")
        content = doc.get("content", "")

        lines = content.splitlines()

        if len(lines) > 500:
            smells.append({
                "file": path,
                "smell": "Large File",
                "details": f"{len(lines)} lines"
            })

        function_count = (
            content.count("def ") +
            content.count("function ")
        )

        if function_count > 20:
            smells.append({
                "file": path,
                "smell": "Too Many Functions",
                "details": f"{function_count} functions detected"
            })

        conditional_count = content.count("if ")

        if conditional_count > 30:
            smells.append({
                "file": path,
                "smell": "Complex Conditional Logic",
                "details": f"{conditional_count} conditionals detected"
            })

        if "TODO" in content or "FIXME" in content:
            smells.append({
                "file": path,
                "smell": "Pending Work",
                "details": "Contains TODO or FIXME markers"
            })

    return {
        "repository_id": repository_id,
        "code_smells": smells,
        "total_smells": len(smells)
    }


# New endpoint: detect potential bugs
@router.get("/repository/{repository_id}/bugs")
def repository_bugs(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    bugs = []

    for doc in repo["documents"]:

        path = doc.get("path", "")
        content = doc.get("content", "")

        if "except:" in content:
            bugs.append({
                "file": path,
                "issue": "Bare Exception Handler",
                "severity": "Medium"
            })

        if "password =" in content.lower() or "password=" in content.lower():
            bugs.append({
                "file": path,
                "issue": "Hardcoded Password",
                "severity": "High"
            })

        if "api_key" in content.lower():
            bugs.append({
                "file": path,
                "issue": "Possible Hardcoded API Key",
                "severity": "High"
            })

        if ".get(" not in content and "[" in content and "]" in content:
            bugs.append({
                "file": path,
                "issue": "Possible Unsafe Dictionary Access",
                "severity": "Low"
            })

        if "todo" in content.lower() and "fix" in content.lower():
            bugs.append({
                "file": path,
                "issue": "Known Bug Marker Found",
                "severity": "Medium"
            })


    return {
        "repository_id": repository_id,
        "bugs": bugs,
        "total_bugs": len(bugs)
    }


# New endpoint: AI-style refactor suggestions
@router.get("/repository/{repository_id}/refactor")
def repository_refactor(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    suggestions = []

    for doc in repo["documents"]:

        path = doc.get("path", "")
        content = doc.get("content", "")

        line_count = len(content.splitlines())

        if line_count > 500:
            suggestions.append({
                "file": path,
                "suggestion": "Split large file into smaller modules",
                "priority": "High"
            })

        function_count = (
            content.count("def ") +
            content.count("function ")
        )

        if function_count > 20:
            suggestions.append({
                "file": path,
                "suggestion": "Extract functions into separate services/helpers",
                "priority": "Medium"
            })

        if content.count("if ") > 30:
            suggestions.append({
                "file": path,
                "suggestion": "Reduce nested conditional logic",
                "priority": "Medium"
            })

        if "TODO" in content or "FIXME" in content:
            suggestions.append({
                "file": path,
                "suggestion": "Resolve pending TODO/FIXME items",
                "priority": "Low"
            })

    return {
        "repository_id": repository_id,
        "refactor_suggestions": suggestions,
        "total_suggestions": len(suggestions)
    }


# New endpoint: repository quality score
@router.get("/repository/{repository_id}/quality-score")
def repository_quality_score(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    documents = repo["documents"]

    score = 100

    strengths = []
    weaknesses = []

    paths = [doc.get("path", "").lower() for doc in documents]

    if any("readme" in p for p in paths):
        strengths.append("Project documentation available")
    else:
        weaknesses.append("README missing")
        score -= 15

    if any("test" in p for p in paths):
        strengths.append("Test files detected")
    else:
        weaknesses.append("No test files detected")
        score -= 10

    total_smells = 0
    total_bugs = 0

    for doc in documents:

        content = doc.get("content", "")

        if len(content.splitlines()) > 500:
            total_smells += 1

        if "TODO" in content or "FIXME" in content:
            total_smells += 1

        if "except:" in content:
            total_bugs += 1

        if "password=" in content.lower():
            total_bugs += 1

    score -= total_smells * 2
    score -= total_bugs * 5

    score = max(0, min(100, score))

    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "D"

    return {
        "repository_id": repository_id,
        "quality_score": score,
        "grade": grade,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "code_smells_detected": total_smells,
        "bugs_detected": total_bugs
    }

@router.get("/repository/{repository_id}/documentation")
def repository_documentation(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    docs = generate_documentation(
        repo["documents"]
    )

    return {
        "repository_id": repository_id,
        "documentation": docs
    }

@router.get("/repository/{repository_id}/api-docs")
def repository_api_docs(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return {
        "repository_id": repository_id,
        "api_docs": generate_api_docs(
            repo["documents"]
        )
    }

@router.get("/repository/{repository_id}/tests")
def repository_tests(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return {
        "repository_id": repository_id,
        "tests": generate_test_cases(
            repo["documents"]
        )
    }

@router.get("/repository/{repository_id}/explain")
def repository_explain(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return {
        "repository_id": repository_id,
        "explanation": explain_repository(
            repo["documents"]
        )
    }

@router.get("/repository/{repository_id}/fixes")
def repository_fixes(repository_id: str):

    repo = get_repository(repository_id)

    if not repo:
        return {"error": "Repository not found"}

    return {
        "repository_id": repository_id,
        "fixes": generate_fixes(
            repo["documents"]
        )
    }

@router.get(
    "/repository/{repository_id}/architecture-report"
)
def architecture_report(
    repository_id: str
):

    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    return generate_architecture_report(
        repo
    )

@router.get("/repository/{repository_id}/improvements")
def repository_improvements(repository_id: str):
    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    return generate_improvements(repo)

@router.get("/repository/{repository_id}/engineering-score")
def repository_engineering_score(repository_id: str):
    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    return {
        "repository_id": repository_id,
        "engineering_score":
            calculate_engineering_score(repo)
    }

@router.get("/repository/{repository_id}/executive-report")
def repository_executive_report(repository_id: str):

    repo = get_repository(repository_id)
    if not repo:
        return {
            "error": "Repository not found"
        }
    return {
        "repository_id": repository_id,
        "report":
            generate_executive_report(repo)
    }

@router.post(
    "/repository/{repository_id}/ask"
)
def ask_repository(
    repository_id: str,
    request: RepositoryQuestion
):

    repo = get_repository(repository_id)

    if not repo:
        return {
            "error": "Repository not found"
        }

    answer = answer_repository_question(
        repo,
        request.question
    )

    return {
        "repository_id": repository_id,
        "question": request.question,
        "answer": answer
    }

@router.get(
    "/repository/{repository_id}/dashboard"
)
def repository_dashboard(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    dashboard = (
        generate_dashboard_summary(
            repo
        )
    )

    return {
        "repository_id": repository_id,
        **dashboard
    }


@router.post(
    "/repository/{repository_id}/search"
)
def repository_search(
    repository_id: str,
    request: SearchRequest
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    query_embedding = (
        create_embedding(
            request.query
        )
    )

    results = search_repository(
        repo["vector_store"],
        query_embedding
    )

    return {
        "repository_id": repository_id,
        "query": request.query,
        "results": results
    }

@router.get(
    "/repository/{repository_id}/commit-messages"
)
def repository_commit_messages(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    return {
        "repository_id": repository_id,
        "commit_messages":
            generate_commit_messages(
                repo
            )
    }

@router.get(
    "/repository/{repository_id}/pr-summary"
)
def repository_pr_summary(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    return {
        "repository_id": repository_id,
        "summary":
            generate_pr_summary(
                repo
            )
    }

@router.get(
    "/repository/{repository_id}/release-notes"
)
def repository_release_notes(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    return {
        "repository_id": repository_id,
        "release_notes":
            generate_release_notes(
                repo
            )
    }

@router.get(
    "/repository/{repository_id}/health"
)
def repository_health(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    return {
        "repository_id":
            repository_id,
        "health":
            generate_repository_health(
                repo
            )
    }

@router.post(
    "/repository/{repository_id}/pr-review"
)
def repository_pr_review(
    repository_id: str,
    request: PRReviewRequest
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    review = review_pull_request(
        repo,
        request.changed_files
    )

    return {
        "repository_id":
            repository_id,
        "review":
            review
    }

@router.get(
    "/repository/{repository_id}/bug-fixes"
)
def repository_bug_fixes(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    fixes = generate_bug_fix_plan(
        repo
    )

    return {
        "repository_id":
            repository_id,
        "bug_fixes":
            fixes,
        "total_fixes":
            len(fixes)
    }

@router.get(
    "/repository/{repository_id}/refactor-plan"
)
def repository_refactor_plan(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error": "Repository not found"
        }

    plan = generate_refactor_plan(
        repo
    )

    return {
        "repository_id":
            repository_id,
        "refactor_plan":
            plan,
        "total_actions":
            len(plan)
    }

@router.get(
    "/repository/{repository_id}/dependency-analysis"
)
def repository_dependency_analysis(
    repository_id: str
):

    repo = get_repository(
        repository_id
    )

    if not repo:
        return {
            "error":
                "Repository not found"
        }

    return {
        "repository_id":
            repository_id,
        "dependency_analysis":
            analyze_dependencies(
                repo
            )
    }
