import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../../auth/authConfig";

const LoginButton = () => {
    const { instance } = useMsal();

    const handleLogin = async () => {
    try {
        await instance.loginRedirect(loginRequest);
    } catch (error) {
        console.error(error);
    }
};

    return (
        <button
            onClick={handleLogin}
            className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
            Sign in with Microsoft
        </button>
    );
};

export default LoginButton;