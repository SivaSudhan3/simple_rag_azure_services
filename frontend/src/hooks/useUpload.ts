import { useState } from "react";
import { documentApi } from "../api/documentApi";

export function useUpload() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [jobId, setJobId] = useState<string | null>(null);

    const upload = async () => {
        if (!selectedFile) {
            setError("Please select a file.");
            return;
        }

        try {
            setError(null);
            setIsUploading(true);

            const response = await documentApi.uploadDocument(selectedFile);

            setJobId(response.job_id);
        } catch (err) {
            console.error(err);
            setError("Failed to upload document.");
        } finally {
            setIsUploading(false);
        }
    };

    return {
        selectedFile,
        setSelectedFile,
        upload,
        isUploading,
        error,
        jobId,
    };
}