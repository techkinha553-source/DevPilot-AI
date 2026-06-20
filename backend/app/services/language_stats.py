from collections import Counter


def detect_languages(documents):

    languages = Counter()

    for doc in documents:

        path = doc.get("path", "").lower()

        if path.endswith(".py"):
            languages["Python"] += 1

        elif path.endswith(".js"):
            languages["JavaScript"] += 1

        elif path.endswith(".ts"):
            languages["TypeScript"] += 1

        elif path.endswith(".java"):
            languages["Java"] += 1

        elif path.endswith(".cpp"):
            languages["C++"] += 1

    return dict(languages)