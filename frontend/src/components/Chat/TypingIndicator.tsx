const TypingIndicator = () => {
    return (
        <div className="flex justify-start">

            <div className="rounded-2xl bg-gray-100 px-4 py-3">

                <div className="flex items-center gap-1">

                    <span
                        className="h-2 w-2 rounded-full bg-gray-500 animate-bounce"
                    />

                    <span
                        className="h-2 w-2 rounded-full bg-gray-500 animate-bounce"
                        style={{
                            animationDelay: "0.15s",
                        }}
                    />

                    <span
                        className="h-2 w-2 rounded-full bg-gray-500 animate-bounce"
                        style={{
                            animationDelay: "0.30s",
                        }}
                    />

                </div>

            </div>

        </div>
    );
};

export default TypingIndicator;