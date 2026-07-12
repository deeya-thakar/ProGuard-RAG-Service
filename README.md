# SOP RAG Backend API

A lightweight **Retrieval-Augmented Generation (RAG)** backend built with **FastAPI**, **SQLite**, **TinyDB**, and **Google Gemini**. The API ingests Standard Operating Procedure (SOP) documents, creates searchable text chunks, and provides context-aware answers based only on the selected document content.

## Tech Stack

- **API Framework:** FastAPI
- **Database:** SQLite (SQLAlchemy)
- **Audit & History:** TinyDB
- **LLM:** Google Gemini API (`gemini-flash-latest`)

## Local Setup

### 1. Clone the Repository

`git clone deeya-thakar/ProGuard-RAG-Service`
`cd ProGuard-RAG-Service`

### 2. Create & Activate a Virtual Environment

`python -m venv venv`

**Windows**

`.\venv\Scripts\activate`

**macOS/Linux**

`surce venv/bin/activate`

### 3. Install Dependencies

`pip install -r requirements.txt`

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your Gemini API key:
`GEMINI_API_KEY=AQ.Ab8RN6INBVwTEKmoarOePjN0VweYnY7QX3pKV1LFX-nMtn3t_w_dummy`

## Running the Application

### 1. Ingest Documents

`python ingest.py`

### 2. Start the Server

`python -m uvicorn main:app --reload`

### 3. Access the API

Open Swagger UI:

`http://127.0.0.1:8000/docs`

## API Endpoints

- `GET /documents` – List all ingested SOP documents.
- `GET /documents/{doc_id}/chunks` – Retrieve document chunks.
- `POST /selections` – Create a context from selected chunk IDs.
- `POST /grounded-qa` – Generate answers using the selected context.
- `GET /history` – View the Q&A audit history stored in TinyDB.