import ReactMarkdown from "react-markdown";
import { FaRobot, FaUserCircle } from "react-icons/fa";

import type { ChatMessage } from "../../types/chat";

interface MessageBubbleProps {
    message: ChatMessage;
    isStreaming?: boolean;
}

const MessageBubble = ({
    message,
    isStreaming = false,
}: MessageBubbleProps) => {

    const isUser = message.role === "user";

    return (

        <div
            className={`flex gap-3 ${
                isUser
                    ? "justify-end"
                    : "justify-start"
            }`}
        >

            {!isUser && (
                <div className="mt-1 shrink-0">
                    <FaRobot
                        size={32}
                        className="text-blue-600"
                    />
                </div>
            )}

            <div
                className={`max-w-[80%] rounded-2xl px-5 py-4 shadow-sm ${
                    isUser
                        ? "bg-blue-600 text-white"
                        : "border bg-gray-50 text-gray-900"
                }`}
            >

                <div className="prose prose-sm max-w-none">

                    <ReactMarkdown>
                        {message.content}
                    </ReactMarkdown>

                    {!isUser && isStreaming && (

                        <span
                            className="
                                ml-1
                                inline-block
                                h-5
                                w-[2px]
                                animate-pulse
                                bg-gray-800
                                align-middle
                            "
                        />

                    )}

                </div>

                {!isUser &&
                    message.citations &&
                    message.citations.length > 0 && (

                        <div className="mt-5 border-t pt-4">

                            <p className="mb-3 text-sm font-semibold text-gray-700">

                                📚 Sources

                            </p>

                            <div className="space-y-2">

                                {message.citations.map(
                                    (citation) => (

                                        <div
                                            key={citation.id}
                                            className="
                                                cursor-pointer
                                                rounded-lg
                                                border
                                                bg-white
                                                p-3
                                                transition
                                                hover:border-blue-500
                                                hover:bg-blue-50
                                                hover:shadow
                                            "
                                        >

                                            <div className="font-medium">

                                                📄 {citation.file}

                                            </div>

                                            {citation.page !== null && (

                                                <div className="mt-1 text-xs text-gray-500">

                                                    Page {citation.page}

                                                </div>

                                            )}

                                        </div>

                                    )
                                )}

                            </div>

                        </div>

                    )}

            </div>

            {isUser && (
                <div className="mt-1 shrink-0">
                    <FaUserCircle
                        size={32}
                        className="text-blue-600"
                    />
                </div>
            )}

        </div>

    );

};

export default MessageBubble;