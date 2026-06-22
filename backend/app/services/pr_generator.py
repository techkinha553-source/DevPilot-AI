def generate_pr(
    title,
    changes
    ):
    return {
        "title": title,
        "description": f"""

Summary

{changes}

Testing

* Manual testing completed
* API verified
"""
    }