import store from "./redux/store";
import { Provider } from "react-redux";
import InteractionForm from "./components/InteractionForm";
import ChatAssistant from "./components/ChatAssistant";

import "./App.css";

function App() {
  return (
    <Provider store={store}>
   <div className="min-h-screen bg-gray-100 p-8">

      <h1 className="text-2xl font-semibold mb-6">
        Log HCP Interaction
      </h1>

      <div className="flex gap-6">

        {/* LEFT PANEL */}
        <div className="w-2/3">
          <InteractionForm />
        </div>

        {/* RIGHT PANEL */}
        <div className="w-1/3">
          <ChatAssistant />
        </div>

      </div>

    </div>
    </Provider>
  );
}

export default App;