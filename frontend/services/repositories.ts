export const getRepositories = async (
    email: string
) => {

    const res = await fetch(
        `http://localhost:8000/repositories/${email}`
    );

    return await res.json();
};