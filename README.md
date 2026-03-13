# AI Pharma CRM Assistant

AI-powered CRM assistant for pharmaceutical field representatives.
The system helps record doctor interactions, fetch HCP history,
suggest follow-ups, and recommend materials using an AI agent.


## Tech Stack

Backend
- FastAPI
- Python
- LangChain
- Groq LLM

Frontend
- React
- Redux
- Axios

 Database
-  PostgreSQL

## Project Structure

CRM_HCP/
│
├── backend
│   ├── langgraph_agent
│   ├── services
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   └── package.json
│
└── README.md


---

## Backend Setup

cd backend

python -m venv env

env\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload

---

## Frontend Setup

cd frontend

npm install

npm run dev

---

## Features

- Log doctor interactions
- Fetch HCP history
- Suggest follow-up actions
- Recommend marketing materials
- AI-powered conversation input

---

## Example Interaction

Input:

Today I had a meeting with Dr. Kenny about diabetes medication.

Output:

- Interaction logged
- Follow-up suggestions generated
- Recommended materials provided

---

## Author

Rahila MK
Python Full Stack Developer