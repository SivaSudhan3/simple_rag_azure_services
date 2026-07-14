export interface Conversation {
    id: string;
    title: string;
    updated_at: string;
}

export interface ConversationHistory {
    id: string;
    title: string;
    updated_at: string;
    messages: {
        role: "user" | "assistant";
        content: string;
    }[];
}