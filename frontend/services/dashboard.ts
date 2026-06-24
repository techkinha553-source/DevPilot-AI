export const getDashboard = async (
    email: string
) => {

    const res = await fetch(
        `http://localhost:8000/dashboard/${email}`
    );

    return await res.json();
};