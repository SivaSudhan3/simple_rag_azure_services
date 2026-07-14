import {
    FaPlus,
    FaComments,
    FaTrash,
} from "react-icons/fa";

import type { Conversation } from "../../types/conversation";

interface SidebarProps {
    conversations: Conversation[];

    selectedConversation?: string;

    loading: boolean;

    onSelect: (id: string) => void;

    onNewChat: () => void;

    onDelete: (id: string) => void;
}

const Sidebar = ({
    conversations,
    selectedConversation,
    loading,
    onSelect,
    onNewChat,
    onDelete,
}: SidebarProps) => {

    return (

        <aside
            className="
                w-72
                border-r
                bg-white
                flex
                flex-col
                h-screen
            "
        >

            <div className="p-4 border-b">

                <button
                    onClick={onNewChat}
                    className="
                        flex
                        items-center
                        justify-center
                        gap-2
                        w-full
                        rounded-lg
                        bg-blue-600
                        px-4
                        py-3
                        text-white
                        hover:bg-blue-700
                        transition
                    "
                >

                    <FaPlus />

                    <span>New Chat</span>

                </button>

            </div>

            <div className="flex-1 overflow-y-auto">

                {loading && (

                    <div className="p-4 text-gray-500">

                        Loading...

                    </div>

                )}

                {!loading &&
                    conversations.map((conversation) => (

                        <div
                            key={conversation.id}
                            className={`
                                group
                                flex
                                items-center
                                justify-between
                                px-4
                                py-3
                                transition
                                hover:bg-gray-100

                                ${
                                    selectedConversation ===
                                    conversation.id
                                        ? "bg-blue-50 border-r-4 border-blue-600"
                                        : ""
                                }
                            `}
                        >

                            <button
                                onClick={() =>
                                    onSelect(
                                        conversation.id
                                    )
                                }
                                className="
                                    flex
                                    flex-1
                                    items-center
                                    gap-3
                                    text-left
                                "
                            >

                                <FaComments
                                    className="text-gray-600"
                                />

                                <span className="truncate">

                                    {
                                        conversation.title
                                    }

                                </span>

                            </button>

                            <button
                                onClick={(e) => {

                                    e.stopPropagation();

                                    if (
                                        window.confirm(
                                            "Delete this conversation?"
                                        )
                                    ) {

                                        onDelete(
                                            conversation.id
                                        );

                                    }

                                }}
                                className="
                                    opacity-0
                                    group-hover:opacity-100
                                    transition
                                    p-2
                                    text-gray-500
                                    hover:text-red-600
                                "
                            >

                                <FaTrash />

                            </button>

                        </div>

                    ))}

            </div>

        </aside>

    );

};

export default Sidebar;