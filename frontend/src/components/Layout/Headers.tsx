import { useEffect } from "react";
import { FaRobot } from "react-icons/fa";
import {
    useIsAuthenticated,
    useMsal,
} from "@azure/msal-react";

import LoginButton from "../Auth/LoginButton";
import LogoutButton from "../Auth/LogoutButton";

const Header = () => {
    const { instance, accounts } = useMsal();
    const isAuthenticated = useIsAuthenticated();

    useEffect(() => {
        if (!instance.getActiveAccount() && accounts.length > 0) {
            instance.setActiveAccount(accounts[0]);
        }
    }, [accounts, instance]);

    const activeAccount =
        instance.getActiveAccount() ?? accounts[0];

    return (
        <header className="bg-blue-600 text-white shadow">
            <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">

                <div className="flex items-center gap-3">
                    <FaRobot size={28} />

                    <div>
                        <h1 className="text-xl font-bold">
                            Azure AI Interview Assistant
                        </h1>

                        <p className="text-sm text-blue-100">
                            Agentic RAG Demo
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-4">

                    {isAuthenticated && (
                        <div className="text-right">
                            <p className="text-sm font-medium">
                                {activeAccount?.name}
                            </p>

                            <p className="text-xs text-blue-100">
                                {activeAccount?.username}
                            </p>
                        </div>
                    )}

                    {isAuthenticated ? (
                        <LogoutButton />
                    ) : (
                        <LoginButton />
                    )}

                </div>

            </div>
        </header>
    );
};

export default Header;