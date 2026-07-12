import apiClient from "./axios";
import type { UploadResponse } from "../types/document";

export const documentApi = {
    async uploadDocument(file: File): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append("file", file);

        const response = await apiClient.post<UploadResponse>(
            "/documents/upload",
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        );

        return response.data;
    },
};