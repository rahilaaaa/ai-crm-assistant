import { useSelector } from "react-redux";

export default function InteractionForm() {

  const form = useSelector((state) => state.form);

  return (
    <div className="bg-white rounded-xl shadow border p-6">

      <h2 className="text-lg font-semibold mb-6">
        Interaction Details
      </h2>

      {/* HCP + TYPE */}
      <div className="grid grid-cols-2 gap-4 mb-4">

        <div>
          <label className="text-sm text-gray-600">HCP Name</label>
          <input
            value={form.hcp_name || ""}
            className="w-full border rounded-lg p-2 mt-1"
            placeholder="Search or select HCP..."
            readOnly
          />
        </div>

        <div>
          <label className="text-sm text-gray-600">Interaction Type</label>
          <select
            value={form.interaction_type || ""}
            className="w-full border rounded-lg p-2 mt-1"
          >
            <option value="">Select</option>
            <option value="meeting">Meeting</option>
            <option value="call">Call</option>
          </select>
        </div>

      </div>

      {/* DATE + TIME */}
      <div className="grid grid-cols-2 gap-4 mb-4">

        <div>
          <label className="text-sm text-gray-600">Date</label>
          <input
            value={form.meeting_date || ""}
            className="w-full border rounded-lg p-2 mt-1"
            readOnly
          />
        </div>

        <div>
          <label className="text-sm text-gray-600">Time</label>
          <input
            value={form.meeting_time || ""}
            className="w-full border rounded-lg p-2 mt-1"
            readOnly
          />
        </div>

      </div>

      {/* ATTENDEES */}
      <div className="mb-4">
        <label className="text-sm text-gray-600">Attendees</label>
        <input
          value={form.attendees || ""}
          className="w-full border rounded-lg p-2 mt-1"
          readOnly
        />
      </div>

      {/* TOPICS */}
      <div className="mb-4">
        <label className="text-sm text-gray-600">Topics Discussed</label>
        <textarea
          rows="3"
          value={form.topics || ""}
          className="w-full border rounded-lg p-2 mt-1"
          readOnly
        />
      </div>

      {/* MATERIALS */}
      <div className="border rounded-lg p-4 mb-4">

        <h3 className="font-medium text-gray-700 mb-2">
          Materials Shared
        </h3>

        <p className="text-gray-600 text-sm">
          {form.materials_shared || "No materials added"}
        </p>

      </div>

      {/* SENTIMENT */}
      <div className="mb-4">

        <label className="text-sm text-gray-600">
          Observed HCP Sentiment
        </label>

        <div className="flex gap-6 mt-2">

          <label>
            <input
              type="radio"
              checked={form.sentiment === "positive"}
              readOnly
            /> Positive
          </label>

          <label>
            <input
              type="radio"
              checked={form.sentiment === "neutral"}
              readOnly
            /> Neutral
          </label>

          <label>
            <input
              type="radio"
              checked={form.sentiment === "negative"}
              readOnly
            /> Negative
          </label>

        </div>

      </div>

      {/* OUTCOMES */}
      <div className="mb-4">
        <label className="text-sm text-gray-600">Outcomes</label>
        <textarea
          rows="2"
          value={form.outcomes || ""}
          className="w-full border rounded-lg p-2 mt-1"
          readOnly
        />
      </div>

      {/* FOLLOWUPS */}
      <div>
        <label className="text-sm text-gray-600">
          Follow-up Actions
        </label>

        <textarea
          rows="2"
          value={form.followups || ""}
          className="w-full border rounded-lg p-2 mt-1"
          readOnly
        />
      </div>

    </div>
  );
}