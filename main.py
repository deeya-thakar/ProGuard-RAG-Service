import os
import google.generativeai as genai
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from tinydb import TinyDB
# pyrefly: ignore [missing-import]
from database import SessionLocal, Document, Chunk, Selection
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

app = FastAPI(title="ProGuard RAG Service")
history_db = TinyDB('history.json')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SelectionRequest(BaseModel):
    chunk_ids: List[int]

class QARequest(BaseModel):
    selection_id: int
    question: str

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@app.get("/documents/{doc_id}/chunks")
def get_chunks(doc_id: int, db: Session = Depends(get_db)):
    return db.query(Chunk).filter(Chunk.document_id == doc_id).all()

@app.post("/selections")
def create_selection(req: SelectionRequest, db: Session = Depends(get_db)):
    chunk_ids_str = ",".join(map(str, req.chunk_ids))
    selection = Selection(chunk_ids=chunk_ids_str)
    db.add(selection)
    db.commit()
    db.refresh(selection)
    return {"selection_id": selection.id}

@app.post("/grounded-qa")
def grounded_qa(req: QARequest, db: Session = Depends(get_db)):
    selection = db.query(Selection).filter(Selection.id == req.selection_id).first()
    if not selection:
        raise HTTPException(status_code=404, detail="Selection not found")
    
    chunk_ids = [int(id) for id in selection.chunk_ids.split(',')]
    chunks = db.query(Chunk).filter(Chunk.id.in_(chunk_ids)).all()
    
    context = "\n\n".join([f"Chunk {c.id}: {c.content}" for c in chunks])
    
    prompt = f"""
    You are a strict compliance assistant. Answer the user's question using ONLY the provided chunks.
    If the answer is not contained in the chunks, state exactly: 'I do not have enough information.'
    
    Context:
    {context}
    
    Question: {req.question}
    """
    
    response = model.generate_content(prompt)
    answer = response.text
    
    history_db.insert({
        "question": req.question,
        "answer": answer,
        "selection_id": req.selection_id,
        "citations": chunk_ids
    })
    
    return {"answer": answer, "citations": chunk_ids}

@app.get("/history")
def get_history():
    return history_db.all()