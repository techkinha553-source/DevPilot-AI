def generate_refactor_plan(repo):

    plans = []

    for doc in repo["documents"]:

        path = doc.get("path", "")
        content = doc.get("content", "")

        line_count = len(content.splitlines())

        if line_count > 500:
            plans.append({
                "file": path,
                "issue": "Large File",
                "priority": "High",
                "action":
                    "Split file into smaller modules"
            })

        function_count = (
            content.count("def ")
            + content.count("function ")
        )

        if function_count > 20:
            plans.append({
                "file": path,
                "issue": "Too Many Functions",
                "priority": "Medium",
                "action":
                    "Move logic into services/helpers"
            })

        class_count = content.count("class ")

        if class_count > 10:
            plans.append({
                "file": path,
                "issue": "Too Many Classes",
                "priority": "Medium",
                "action":
                    "Separate domain models"
            })

        if content.count("if ") > 30:
            plans.append({
                "file": path,
                "issue": "Complex Logic",
                "priority": "Medium",
                "action":
                    "Reduce nested conditions"
            })

        if "TODO" in content or "FIXME" in content:
            plans.append({
                "file": path,
                "issue": "Pending Work",
                "priority": "Low",
                "action":
                    "Resolve TODO/FIXME items"
            })

    return plans