import { API_BASE_URL } from "../utils/constants";
import { getAccessToken } from "./authService";

export interface StreamCallbacks {
    onStart?: (data: any) => void;
    onToken?: (token: string) => void;
    onBlocked?: (message: string) => void;
    onDone?: (data: any) => void;
    onError?: (error: Error) => void;
}

export async function streamChat(
    body: {
        question: string;
        conversation_id?: string;
    },
    callbacks: StreamCallbacks
) {

    const token = await getAccessToken();

    const response = await fetch(
        `${API_BASE_URL}/chat/stream`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(body),
        }
    );

    if (!response.ok) {

        let error: Error;

        switch (response.status) {

            case 401:
                error = new Error("Unauthorized");
                break;

            case 403:
                error = new Error("Forbidden");
                break;

            case 500:
                error = new Error("ServerError");
                break;

            default:
                error = new Error("RequestFailed");
        }

        callbacks.onError?.(error);

        throw error;
    }

    if (!response.body) {

        const error = new Error("NoResponseStream");

        callbacks.onError?.(error);

        throw error;
    }

    const reader = response.body.getReader();

    const decoder = new TextDecoder();

    let buffer = "";

    while (true) {

        const { value, done } =
            await reader.read();

        if (done) break;

        buffer += decoder.decode(value, {
            stream: true,
        });

        const events = buffer.split("\n\n");

        buffer = events.pop() ?? "";

        for (const event of events) {

            let eventName = "";
            let data = "";

            for (const line of event.split("\n")) {

                if (line.startsWith("event:")) {
                    eventName = line
                        .replace("event:", "")
                        .trim();
                }

                if (line.startsWith("data:")) {
                    data = line.replace(/^data:\s?/, "");
                }

            }

            switch (eventName) {

                case "start":
                    callbacks.onStart?.(
                        JSON.parse(data)
                    );
                    break;

                case "token":
                    callbacks.onToken?.(data);
                    break;

                case "blocked":
                    callbacks.onBlocked?.(
                        JSON.parse(data).message
                    );
                    break;

                case "done":
                    callbacks.onDone?.(
                        JSON.parse(data)
                    );
                    break;

                case "error":
                    callbacks.onError?.(
                        new Error(data)
                    );
                    break;
            }
        }
    }
}