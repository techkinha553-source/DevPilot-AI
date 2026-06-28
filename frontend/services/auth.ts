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

    const data = await res.json();

    console.log("SIGNUP STATUS:", res.status);
    console.log("SIGNUP RESPONSE:", data);

    return data;
};

export const login = async (
    email: string,
    password: string
) => {

    console.log("Trying login...");

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

    console.log("STATUS:", res.status);

    const data = await res.json();

    console.log("RESPONSE:", data);

    return data;
};