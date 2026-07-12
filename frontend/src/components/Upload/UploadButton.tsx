interface UploadButtonProps {
    onClick: () => void;
    disabled?: boolean;
    isUploading?: boolean;
}

const UploadButton = ({
    onClick,
    disabled = false,
    isUploading = false,
}: UploadButtonProps) => {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className="
                bg-blue-600
                hover:bg-blue-700
                disabled:bg-gray-400
                disabled:cursor-not-allowed
                text-white
                font-medium
                px-5
                py-2
                rounded-lg
                transition
            "
        >
            {isUploading ? "Uploading..." : "Upload"}
        </button>
    );
};

export default UploadButton;