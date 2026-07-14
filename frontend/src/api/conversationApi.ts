import apiClient from "./axios";

import type {
    Conversation,
    ConversationHistory,
} from "../types/conversation";

export const conversationApi = {

    async getConversations(): Promise<Conversation[]> {

        const response =
            await apiClient.get("/conversations");

        return response.data;

    },

    async getConversation(
        id: string
    ): Promise<ConversationHistory> {

        const response =
            await apiClient.get(
                `/conversations/${id}`
            );

        return response.data;

    },

    async deleteConversation(
        id: string
    ) {

        await apiClient.delete(
            `/conversations/${id}`
        );

    },

};