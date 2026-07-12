import UploadButton from "./UploadButton";
import { useUpload } from "../../hooks/useUpload";

const UploadCard = () => {
    const {
        selectedFile,
        setSelectedFile,
        upload,
        isUploading,
        error,
        jobId,
    } = useUpload();

    return (
        <div className="bg-white rounded-lg shadow border p-6">

            <h2 className="text-xl font-semibold mb-4">
                Upload Document
            </h2>

            <div className="flex flex-col gap-4">

                <input
                    type="file"
                    onChange={(e) => {
                        const file = e.target.files?.[0] ?? null;
                        setSelectedFile(file);
                    }}
                />

                {selectedFile && (
                    <p className="text-sm text-gray-600">
                        Selected: {selectedFile.name}
                    </p>
                )}

                <UploadButton
                    onClick={upload}
                    disabled={!selectedFile || isUploading}
                    isUploading={isUploading}
                />

                {error && (
                    <p className="text-red-600 text-sm">
                        {error}
                    </p>
                )}

                {jobId && (
                    <div className="rounded bg-green-100 p-3 text-green-700 text-sm">
                        Upload started successfully.
                        <br />
                        Job ID: {jobId}
                    </div>
                )}

            </div>

        </div>
    );
};

export default UploadCard;