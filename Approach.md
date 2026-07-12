# Approach

## 1. Chunking Strategy

The provided SOP documents follow a structured numbered format, making rule-based chunking a practical and reliable approach. During ingestion, each document is parsed using a regular expression that identifies numbered sections (e.g., `1.`, `2.`, `3.`). Each section is stored as an individual chunk along with its document metadata and sequence number.

This strategy preserves the logical meaning of each procedure and prevents instructions from being split across multiple chunks. Since the assignment documents already have a well-defined structure, regex-based chunking is simpler, more deterministic, and computationally efficient than semantic or token-based chunking.

## 2. Data Model

The application uses two storage systems based on the characteristics of the data.

### SQLite (SQLAlchemy)

Structured application data is stored in SQLite using SQLAlchemy ORM.

The database maintains:
- **Documents** – stores metadata for each SOP.
- **Chunks** – stores individual text sections linked to their parent document.
- **Selections** – stores user-selected chunk IDs that define the context for question answering.

A relational database was chosen because these entities have clear relationships and benefit from schema validation and referential integrity.

### TinyDB

Question-answer history is stored separately in TinyDB.

Each record contains:
- User question
- Generated answer
- Selection ID
- Referenced chunk IDs
- Timestamp

TinyDB is suitable because session history is append-only and does not require complex joins or relational queries. Separating logs from operational data also keeps the primary database focused on document retrieval.

## 3. Prompt Design for Grounding

To reduce hallucinations, every question sent to the language model includes only the text contained within the selected chunks.

The prompt explicitly instructs the model to:

- Answer only from the supplied context.
- Avoid using external knowledge.
- Return a fallback response when the answer cannot be found in the provided chunks.

This constrained prompting ensures that generated responses remain traceable to the selected SOP content, making the system more reliable for document-based question answering.

## 4. Trade-offs & Future Improvements

The current implementation was designed to satisfy the assignment requirements while remaining simple and maintainable.

### Current Trade-offs

- Context is created manually by selecting chunk IDs instead of performing automatic retrieval.
- SQLite is sufficient for development but is not intended for high-concurrency production workloads.
- Rule-based chunking assumes documents follow a numbered structure and may not generalize to unstructured files.

### Future Improvements

Given additional development time, the following enhancements would improve scalability and usability:

- Integrate a vector database such as FAISS, Pinecone, or ChromaDB to support embedding-based semantic retrieval.
- Replace manual chunk selection with automatic similarity search.
- Migrate to PostgreSQL for improved scalability and concurrent access.
- Normalize the selection model using a many-to-many relationship instead of storing chunk identifiers directly.
- Add authentication, rate limiting, comprehensive logging, and containerized deployment for production readiness.