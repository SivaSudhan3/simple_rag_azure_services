import { useCallback, useState } from "react";
import { v4 as uuid } from "uuid";

import UploadCard from "../components/Upload/UploadCard";
import ChatWindow from "../components/Chat/ChatWindow";
import Sidebar from "../components/Sidebar/Sidebar";

import { useChat } from "../hooks/useChat";
import { useConversations } from "../hooks/useConversation";

import type { ChatMessage } from "../types/chat";

const Home = () => {

    const [messages, setMessages] = useState<ChatMessage[]>([
        {
            id: uuid(),
            role: "assistant",
            content: "Hello! Upload a document and ask questions.",
        },
    ]);

    const [conversationId, setConversationId] =
        useState<string>();

    const chat = useChat({
        messages,
        setMessages,
        conversationId,
        setConversationId,
    });

    const conversations = useConversations();

    const handleConversationSelect = useCallback(
        async (id: string) => {

            const history =
                await conversations.loadConversation(id);

            chat.loadConversation(
                id,
                history.messages
            );

            setConversationId(id);

            conversations.setSelectedConversation(id);

        },
        [chat, conversations]
    );

    const handleNewChat = () => {

        chat.newConversation();

        setConversationId(undefined);

        conversations.setSelectedConversation(undefined);

    };

    const handleDeleteConversation = async (
        id: string
    ) => {

        await conversations.deleteConversation(id);

        if (conversationId === id) {

            chat.newConversation();

            setConversationId(undefined);

            conversations.setSelectedConversation(undefined);

        }

    };

    return (

        <div className="flex h-screen bg-gray-100">

            <Sidebar
                conversations={
                    conversations.conversations
                }
                selectedConversation={
                    conversations.selectedConversation
                }
                loading={
                    conversations.loading
                }
                onSelect={
                    handleConversationSelect
                }
                onNewChat={
                    handleNewChat
                }
                onDelete={
                    handleDeleteConversation
                }
            />

            <main className="flex-1 overflow-y-auto">

                <div className="max-w-5xl mx-auto p-6 space-y-6">

                    <UploadCard />

                    <ChatWindow
                        messages={messages}
                        sendMessage={chat.sendMessage}
                        isThinking={chat.isThinking}
                        isStreaming={chat.isStreaming}
                    />

                </div>

            </main>

        </div>

    );

};

export default Home;