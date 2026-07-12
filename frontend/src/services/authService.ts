import { msalInstance } from "../auth/msalInstance";
import { loginRequest } from "../auth/authConfig";

export async function getAccessToken(): Promise<string | null> {

    const account = msalInstance.getActiveAccount();

    if (!account) {
        return null;
    }

    try {

        const response =
            await msalInstance.acquireTokenSilent({

                ...loginRequest,

                account,

            });

        return response.accessToken;

    } catch (error) {

        console.error(error);

        return null;

    }
}