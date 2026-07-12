import type { Configuration } from "@azure/msal-browser";

export const msalConfig: Configuration = {
    auth: {
        clientId: "ff043519-2326-418a-9e9f-5b3f5b3d2baf",
        authority: "https://login.microsoftonline.com/e72ff303-f8ad-4168-8ff3-f8f1e8b8d311",
        redirectUri: "http://localhost:5173",
        
    },

    cache: {
        cacheLocation: "sessionStorage",
        
    },
};
export const loginRequest = {
    scopes: [
        "openid",
        "profile",
        "email",
        "api://9965846d-3da6-435e-9b87-ea24e61c58e5/chat.access",
    ],
};
