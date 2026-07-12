import UploadCard from "../components/Upload/UploadCard";
import ChatWindow from "../components/Chat/ChatWindow";

const Home = () => {
    return (
        <main className="max-w-5xl mx-auto p-6 space-y-6">

            <UploadCard />
            <ChatWindow />

            <div className="rounded-lg border bg-white p-6 shadow-sm">
                Chat Component
            </div>

        </main>
    );
};

export default Home;