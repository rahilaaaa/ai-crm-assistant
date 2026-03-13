import { createSlice } from "@reduxjs/toolkit";

const formSlice = createSlice({
  name: "form",
  initialState: {
    hcp_name: "",
    interaction_type: "",
    meeting_date: "",
    meeting_time: "",
    attendees: "",
    topics: "",
    materials_shared: "",
    sentiment: "",
    outcomes: "",
    followups: ""
  },
  reducers: {
    updateForm: (state, action) => {
      Object.assign(state, action.payload);
    }
  }
});

export const { updateForm } = formSlice.actions;
export default formSlice.reducer;