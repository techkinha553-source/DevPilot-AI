export const getFileContent = async (
    repositoryId: string,
    filePath: string
) => {

    const response = await fetch(
        `http://localhost:8000/repository/${repositoryId}/file?path=${encodeURIComponent(filePath)}`
    );

    return await response.json();
};