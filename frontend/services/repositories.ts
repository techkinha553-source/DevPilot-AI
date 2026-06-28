export const getRepositories = async (
    email: string
) => {

    const res = await fetch(
        `http://localhost:8000/repositories/${email}`
    );

    return await res.json();
};

export const getMyRepositories = async () => {
    const user = JSON.parse(
        localStorage.getItem("devpilot_user") || "null"
    );

    if (!user?.email) {
        return [];
    }

    return await getRepositories(user.email);
};