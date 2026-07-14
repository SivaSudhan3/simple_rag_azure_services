import { useCallback, useEffect, useState } from "react";

import { conversationApi } from "../api/conversationApi";

import type {
    Conversation,
    ConversationHistory,
} from "../types/conversation";

export function useConversations() {

    const [conversations, setConversations] =
        useState<Conversation[]>([]);
    
    const [selectedConversation, setSelectedConversation] =
    useState<string | undefined>();

   
    const [loading, setLoading] =
        useState(false);

    const loadConversations = useCallback(async () => {

        try {

            setLoading(true);

            const data =
                await conversationApi.getConversations();

            setConversations(data);

        } finally {

            setLoading(false);

        }

    }, []);

    const loadConversation = async (
        id: string
    ): Promise<ConversationHistory> => {

        const history =
            await conversationApi.getConversation(id);

        setSelectedConversation(id);

        return history;

    };

    const deleteConversation = async (
        id: string
    ) => {

        await conversationApi.deleteConversation(id);

        await loadConversations();

    };

    useEffect(() => {

        loadConversations();

    }, [loadConversations]);

    return {

        conversations,

        selectedConversation,

        setSelectedConversation,

        loading,

        loadConversations,

        loadConversation,

        deleteConversation,

    };

}