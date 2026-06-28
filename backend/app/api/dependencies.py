from fastapi import APIRouter, HTTPException
from app.services.repository_store import repositories
import re

router = APIRouter()

@router.get("/repository/{repository_id}/dependencies")
def get_dependencies(repository_id: str):

    repo = repositories.get(repository_id)

    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    dependencies = []
    all_files = []

    for doc in repo.get("documents", []):

        content = doc.page_content
        filename = doc.metadata.get(
            "source",
            "Unknown"
        )
        all_files.append(filename)

        imports = []

        # Python imports
        imports.extend(
            re.findall(
                r"import\s+([a-zA-Z0-9_\.]+)",
                content
            )
        )

        imports.extend(
            re.findall(
                r"from\s+([a-zA-Z0-9_\.]+)\s+import",
                content
            )
        )

        # TypeScript imports
        imports.extend(
            re.findall(
                r"from\s+['\"]([^'\"]+)['\"]",
                content
            )
        )

        dependencies.append({
            "file": filename,
            "dependsOn": list(set(imports))
        })

    circular_count = 0

    for node in dependencies:
        current = node["file"]

        for dep in node["dependsOn"]:

            for target in dependencies:

                if target["file"] == dep:

                    if current in target["dependsOn"]:
                        circular_count += 1

    if circular_count == 0:
        risk_level = "Low"
    elif circular_count < 3:
        risk_level = "Medium"
    else:
        risk_level = "High"

    referenced_modules = set()

    for node in dependencies:
        for dep in node["dependsOn"]:
            referenced_modules.add(dep.split(".")[-1])

    orphan_files = []

    for file_name in all_files:

        base_name = file_name.split("/")[-1]
        module_name = base_name.split(".")[0]

        if module_name not in referenced_modules:
            orphan_files.append(file_name)

    maintainability_score = max(
        0,
        100 - (circular_count * 10) - (len(orphan_files) * 2)
    )

    large_files = []
    hotspot_files = []
    technical_debt_score = 0

    for doc in repo.get("documents", []):

        filename = doc.metadata.get(
            "source",
            "Unknown"
        )

        content = doc.page_content
        lines = len(content.splitlines())

        if lines > 300:
            large_files.append(filename)
            technical_debt_score += 10

        if (
            content.count("if ") > 20 or
            content.count("for ") > 15 or
            content.count("while ") > 5
        ):
            hotspot_files.append(filename)
            technical_debt_score += 5

    technical_debt_score = min(
        100,
        technical_debt_score
    )

    refactoring_candidates = []

    for file_name in large_files:
        refactoring_candidates.append({
            "file": file_name,
            "reason": "Large file size",
            "priority": "High"
        })

    for file_name in hotspot_files:

        already_added = False

        for item in refactoring_candidates:
            if item["file"] == file_name:
                already_added = True
                break

        if not already_added:
            refactoring_candidates.append({
                "file": file_name,
                "reason": "High complexity hotspot",
                "priority": "Medium"
            })

    refactoring_candidates = refactoring_candidates[:5]

    modernization_roadmap = [
        "Break large files into smaller modules",
        "Reduce nested conditions and loops",
        "Add unit tests for critical logic",
        "Improve documentation and typing",
        "Remove unused/orphan files"
    ]

    return {
        "dependencies": dependencies,
        "circular_dependencies": circular_count,
        "architecture_risk": risk_level,
        "orphan_files": orphan_files,
        "maintainability_score": maintainability_score,
        "technical_debt_score": technical_debt_score,
        "large_files": large_files,
        "hotspot_files": hotspot_files,
        "refactoring_candidates": refactoring_candidates,
        "modernization_roadmap": modernization_roadmap
    }
