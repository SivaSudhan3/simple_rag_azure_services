import { useEffect, useRef } from "react";

import MessageBubble from "./MessageBubble";
import ChatInput from "./chatInput";
import TypingIndicator from "./TypingIndicator";

import { useChat } from "../../hooks/useChat";

const ChatWindow = () => {

    const {
        messages,
        sendMessage,
        isThinking,
        isStreaming,
    } = useChat();

    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth",
        });

    }, [messages, isThinking]);

    return (

        <div className="rounded-lg border bg-white p-6 shadow">

            <h2 className="mb-4 text-xl font-semibold">
                Chat
            </h2>

            <div className="mb-4 h-[500px] overflow-y-auto rounded-lg border p-4">

                <div className="space-y-4">

                    {messages.map((message) => (

                        <MessageBubble
                            key={message.id}
                            message={message}
                            isStreaming={
                                isStreaming &&
                                message.id ===
                                    messages[messages.length - 1].id
                            }
                        />

                    ))}

                    {isThinking && (
                        <TypingIndicator />
                    )}

                    <div ref={bottomRef} />

                </div>

            </div>

            <ChatInput
                onSend={sendMessage}
                disabled={
                    isThinking || isStreaming
                }
            />

        </div>

    );

};

export default ChatWindow;