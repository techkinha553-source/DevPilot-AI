export const signup = async (
    email: string,
    password: string
) => {

    const res = await fetch(
        "http://localhost:8000/signup",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        }
    );

    return await res.json();
};

export const login = async (
    email: string,
    password: string
) => {

    const res = await fetch(
        "http://localhost:8000/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        }
    );

    return await res.json();
};