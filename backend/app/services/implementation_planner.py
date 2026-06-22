def create_plan(feature):

    return {
        "feature": feature,
        "steps": [
            "Create authentication service",
            "Create JWT handler",
            "Protect routes",
            "Write tests",
            "Update documentation"
        ]
    }