import { useState } from "react";
import { v4 as uuid } from "uuid";

import type { ChatMessage } from "../types/chat";
import { chatApi } from "../api/chatApi";

interface UseChatProps {
    messages: ChatMessage[];
    setMessages: React.Dispatch<
        React.SetStateAction<ChatMessage[]>
    >;
    conversationId?: string;
    setConversationId: React.Dispatch<
        React.SetStateAction<string | undefined>
    >;
}

export function useChat({
    messages,
    setMessages,
    conversationId,
    setConversationId,
}: UseChatProps) {

    const [isThinking, setIsThinking] =
        useState(false);

    const [isStreaming, setIsStreaming] =
        useState(false);

    const sendMessage = async (question: string) => {

        if (!question.trim()) return;

        const userMessage: ChatMessage = {
            id: uuid(),
            role: "user",
            content: question,
        };

        const assistantId = uuid();

        const assistantMessage: ChatMessage = {
            id: assistantId,
            role: "assistant",
            content: "",
        };

        setMessages(prev => [
            ...prev,
            userMessage,
            assistantMessage,
        ]);

        setIsThinking(true);
        setIsStreaming(false);

        let receivedFirstToken = false;

        try {

            await chatApi.stream(
                question,
                conversationId,
                {

                    onStart(data) {

                        setConversationId(
                            data.conversation_id
                        );

                    },

                    onToken(token) {

                        if (!receivedFirstToken) {

                            receivedFirstToken = true;

                            setIsThinking(false);
                            setIsStreaming(true);

                        }

                        setMessages(prev =>
                            prev.map(message =>
                                message.id === assistantId
                                    ? {
                                          ...message,
                                          content:
                                              message.content +
                                              token,
                                      }
                                    : message
                            )
                        );

                    },

                    onBlocked(message) {

                        setIsThinking(false);
                        setIsStreaming(false);

                        setMessages(prev =>
                            prev.map(m =>
                                m.id === assistantId
                                    ? {
                                          ...m,
                                          content: message,
                                      }
                                    : m
                            )
                        );

                    },

                    onDone(data) {

                        setConversationId(
                            data.conversation_id
                        );

                        setMessages(prev =>
                            prev.map(message =>
                                message.id === assistantId
                                    ? {
                                          ...message,
                                          citations:
                                              Object.values(
                                                  data.citations ??
                                                      {}
                                              ),
                                      }
                                    : message
                            )
                        );

                        setIsThinking(false);
                        setIsStreaming(false);

                    },

                    onError(error) {

                        throw error;

                    },

                }

            );

        } catch (error) {

            setIsThinking(false);
            setIsStreaming(false);

            const message =
                error instanceof Error &&
                error.message ===
                    "Unauthorized"

                    ? "🔒 Your session has expired. Please sign in again."

                    : "⚠️ Unable to reach the server. Please try again.";

            setMessages(prev =>
                prev.map(m =>
                    m.id === assistantId
                        ? {
                              ...m,
                              content: message,
                          }
                        : m
                )
            );

        }

    };

    const loadConversation = (
        conversationId: string,
        history: {
            role: "user" | "assistant";
            content: string;
        }[],
    ) => {

        setConversationId(conversationId);

        setMessages(

            history.map(message => ({

                id: uuid(),

                role: message.role,

                content: message.content,

            }))

        );

    };

    const newConversation = () => {

        setConversationId(undefined);

        setMessages([
            {
                id: uuid(),
                role: "assistant",
                content:
                    "Hello! Upload a document and ask questions.",
            },
        ]);

    };

    return {

        messages,

        conversationId,

        sendMessage,

        loadConversation,

        newConversation,

        isThinking,

        isStreaming,

    };

}