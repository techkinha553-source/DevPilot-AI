"use client";

import { useState } from "react";
import { getCurrentUser } from "../../lib/auth";

export default function UploadPage() {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");

    const handleUpload = async () => {

        if (!file) {
            alert("Please select a ZIP file");
            return;
        }

        setUploading(true);

        const user = getCurrentUser();

        if (!user || !user.email) {
            setMessage("Please log in first");
            setUploading(false);
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("owner_email", user.email);

        try {

            const response = await fetch(
                "http://localhost:8000/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            setMessage("Repository uploaded successfully");

            setTimeout(() => {
                window.location.href = "/";
            }, 1500);

        } catch (error) {

            console.error(error);
            setMessage("Upload failed");

        } finally {

            setUploading(false);

        }
    };

    return (
        <main className="min-h-screen bg-gray-100 flex items-center justify-center">

            <div className="bg-white shadow-xl rounded-xl p-8 w-full max-w-xl">

                <h1 className="text-3xl font-bold mb-6">
                    Upload Repository
                </h1>

                <input
                    type="file"
                    accept=".zip"
                    onChange={(e) =>
                        setFile(
                            e.target.files?.[0] || null
                        )
                    }
                    className="mb-4"
                />

                <button
                    onClick={handleUpload}
                    disabled={uploading}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg"
                >
                    {uploading
                        ? "Uploading..."
                        : "Upload Repository"}
                </button>

                {message && (
                    <p className="mt-4">
                        {message}
                    </p>
                )}

            </div>

        </main>
    );
}