import { useMsal } from "@azure/msal-react";

const LogoutButton = () => {
    const { instance } = useMsal();

    const handleLogout = async () => {
        await instance.logoutPopup();
    };

    return (
        <button
            onClick={handleLogout}
            className="rounded-lg bg-red-600 px-4 py-2 text-white hover:bg-red-700"
        >
            Logout
        </button>
    );
};

export default LogoutButton;