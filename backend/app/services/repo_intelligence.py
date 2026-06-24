from typing import List, Dict
from app.services.openai_service import ask_codebase


def generate_ai_summary(documents: List[Dict]) -> str:
    context = "\n\n".join(
        doc["content"][:2000] for doc in documents
    )

    prompt = f"""
You are an expert software architect.

Analyze this repository and give a short summary:

- What the project does
- Architecture style
- Code quality overview
- Risks or issues

CODEBASE:
{context}
"""

    return ask_codebase(prompt, documents)


def classify_issues(documents: List[Dict]) -> Dict:
    text = "\n".join(doc["content"] for doc in documents)

    prompt = f"""
Analyze this code and return ONLY JSON:

{{
  "bugs": number,
  "warnings": number,
  "suggestions": number
}}

CODE:
{text[:4000]}
"""

    result = ask_codebase(prompt, documents)

    try:
        import json
        return json.loads(result)
    except:
        return {
            "bugs": 0,
            "warnings": 0,
            "suggestions": 0
        }


def calculate_health_score(issues: Dict) -> int:
    bugs = issues.get("bugs", 0)
    warnings = issues.get("warnings", 0)
    suggestions = issues.get("suggestions", 0)

    score = 100 - (bugs * 15 + warnings * 5 + suggestions * 2)

    return max(0, min(100, score))