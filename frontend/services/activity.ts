export const getActivity = async () => {

    const response = await fetch(
        "http://localhost:8000/activity"
    );

    return await response.json();
};