import { streamChat, type StreamCallbacks } from "../services/sse";

export const chatApi = {
    async stream(
        question: string,
        conversationId: string | undefined,
        callbacks: StreamCallbacks
    ) {
        return streamChat(
            {
                question,
                conversation_id: conversationId,
            },
            callbacks
        );
    },
};