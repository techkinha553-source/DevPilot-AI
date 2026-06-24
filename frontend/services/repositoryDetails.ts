export const getRepositoryDetails = async (
    repositoryId: string
) => {

    const response = await fetch(
        `http://localhost:8000/repository/${repositoryId}`
    );
    return await response.json();

};