from fastapi import APIRouter

router = APIRouter()

@router.post("/repository/{repository_id}/generate")
def generate_code(
    repository_id: str,
    request: dict
):

    feature = request["feature"]

    generated_code = f"""
# Generated Feature

Feature:
{feature}

# AI generated code here
"""

    return {
        "repository_id": repository_id,
        "generated_code": generated_code
    }
