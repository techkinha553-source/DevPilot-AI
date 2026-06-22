from app.services.tech_stack import detect_tech_stack
from app.services.language_stats import detect_languages
from app.services.engineering_score import calculate_engineering_score
from app.services.improvement_service import generate_improvements

def generate_executive_report(repo):

    documents = repo["documents"]
    tech_stack = detect_tech_stack(documents)
    languages = detect_languages(documents)
    engineering = calculate_engineering_score(repo)
    improvements = generate_improvements(repo)
    strengths = []
    weaknesses = []
    paths = [
        doc.get("path", "").lower()
        for doc in documents
    ]
    if any("readme" in p for p in paths):
        strengths.append(
            "Repository contains documentation"
        )
    else:
        weaknesses.append(
            "README missing"
        )
    if any("test" in p for p in paths):
        strengths.append(
            "Testing infrastructure detected"
        )
    else:
        weaknesses.append(
            "No testing infrastructure detected"
        )
    return {
        "summary":
            f"Repository contains {len(documents)} files.",
        "tech_stack": tech_stack,
        "languages": languages,
        "engineering_score": engineering,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations":
            improvements["improvements"]
    }
