export interface Citation {
    id: string;
    file: string;
    page: number | null;
}

export interface ChatMessage {
    id: string;
    role: "user" | "assistant";
    content: string;
    citations?: Citation[];
}