import os
import re
from database import SessionLocal, Document, Chunk

def ingest_data():
    db = SessionLocal()
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        print(f"Error: Could not find the '{data_dir}' folder. Please create it and add your SOP files.")
        return

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            doc = Document(name=filename)
            db.add(doc)
            db.commit()
            db.refresh(doc)
            
            # Split document by numbered sections logically
            parts = re.split(r'\n(?=\d+\.\s)', text)
            for i, part in enumerate(parts):
                if part.strip():
                    chunk = Chunk(document_id=doc.id, chunk_number=i+1, content=part.strip())
                    db.add(chunk)
            db.commit()
    print("Ingestion complete! Database is populated.")

if __name__ == "__main__":
    ingest_data()