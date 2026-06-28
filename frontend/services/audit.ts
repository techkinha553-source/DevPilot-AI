export const getAudit = async (
repositoryId: string
) => {

    const response = await fetch(
        `http://localhost:8000/repository/${repositoryId}/audit`
    );
    return await response.json();

};