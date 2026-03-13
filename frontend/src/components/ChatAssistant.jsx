import { useState } from "react";
import axios from "axios";
import { useDispatch } from "react-redux";
import { updateForm } from "../redux/formSlice";

export default function ChatAssistant() {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState("");

  const dispatch = useDispatch();

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userMsg = { role: "user", text: message };

    setMessages((prev) => [...prev, userMsg]);

    try {

      const res = await axios.post("http://localhost:8000/chat", {
        message
      });

      dispatch(updateForm(res.data.data));

      const aiMsg = {
        role: "assistant",
        text: res.data.message || "Interaction updated"
      };

      setMessages((prev) => [...prev, aiMsg]);

      setMessage("");

    } catch (error) {

      console.error(error);

    }

  };

  return (
    <div className="bg-white rounded-xl shadow border p-6 flex flex-col h-[700px]">

      <div className="flex items-center gap-2 mb-4">
        <span className="text-blue-500">👁</span>

        <div>
          <h2 className="font-semibold">AI Assistant</h2>
          <p className="text-sm text-gray-500">
            Log Interaction via chat
          </p>
        </div>
      </div>

      <div className="border rounded-lg p-4 flex-1 overflow-y-auto text-sm space-y-2">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`flex ${
              msg.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            <div
              className={`max-w-[75%] px-4 py-2 rounded-lg whitespace-pre-line ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-100 text-gray-800 border"
              }`}
            >
              {msg.text}
            </div>

          </div>

        ))}

      </div>

      <div className="flex mt-4 gap-2">

        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Describe interaction..."
          className="flex-1 border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <button
          onClick={sendMessage}
          className="bg-gray-700 text-white px-4 rounded-lg hover:bg-gray-800 transition"
        >
          Log
        </button>

      </div>

    </div>
  );
}