export const getCurrentUser = () => {

    if (typeof window === "undefined") {
        return null;
    }

    const user = localStorage.getItem(
        "devpilot_user"
    );

    return user
        ? JSON.parse(user)
        : null;
};

export const logout = () => {

    localStorage.removeItem(
        "devpilot_user"
    );

    window.location.href = "/login";
};