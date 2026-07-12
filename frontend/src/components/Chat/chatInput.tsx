import { useState } from "react";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

const ChatInput = ({
    onSend,
    disabled = false,
}: ChatInputProps) => {
    const [message, setMessage] = useState("");

    const handleSend = () => {
        if (!message.trim()) return;

        onSend(message);

        setMessage("");
    };

    return (
        <div className="flex gap-3">

            <input
                className="flex-1 border rounded-lg px-4 py-2"
                placeholder="Type your question..."
                value={message}
                disabled={disabled}
                onChange={(e) =>
                    setMessage(e.target.value)
                }
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                        handleSend();
                    }
                }}
            />

            <button
                onClick={handleSend}
                disabled={disabled}
                className="
                    bg-blue-600
                    hover:bg-blue-700
                    disabled:bg-gray-400
                    text-white
                    px-5
                    rounded-lg
                "
            >
                Send
            </button>

        </div>
    );
};

export default ChatInput;