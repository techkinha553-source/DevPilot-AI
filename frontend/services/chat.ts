export const chatWithRepo = async (
    repository_id: string,
    question: string
) => {
    const res = await fetch(
        "http://localhost:8000/chat",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                repository_id,
                question,
            }),
        }
    );

    return await res.json();
};
