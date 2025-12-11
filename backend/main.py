from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime
import shutil
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app.database import get_db, Document
from app.vector_store import VectorStore
from app.agent import KnowledgeAgent
from app.document_processor import DocumentProcessor

# Disable ChromaDB telemetry
os.environ["ANONYMIZED_TELEMENTRY"] = "false"

app = FastAPI(title="Personal Knowledge Copilot")

# CORS middleware - configure for production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
vector_store = VectorStore()
document_processor = DocumentProcessor()
knowledge_agent = KnowledgeAgent(vector_store)

# Pydantic models
class QueryRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, str]]
    conversation_id: str

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    upload_date: datetime
    processed: bool

# Document endpoints
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Save uploaded file temporarily
        file_extension = os.path.splitext(file.filename)[1].lower()
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md', '.eml', '.html', '.htm']
        
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"File type {file_extension} not supported")
        
        temp_path = f"temp_{uuid.uuid4()}{file_extension}"
        
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Empty file")
            buffer.write(content)
        
        # Process document
        document_id = str(uuid.uuid4())
        chunks = await document_processor.process_document(temp_path, file.filename)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No content could be extracted from the document")
        
        # Store in vector database (using "default" as user_id since no auth)
        vector_store.add_documents(chunks, document_id, "default", file.filename)
        
        # Save document metadata
        db = next(get_db())
        db_document = Document(
            id=document_id,
            user_id="default",
            filename=file.filename,
            file_type=file.content_type,
            upload_date=datetime.utcnow(),
            processed=True
        )
        db.add(db_document)
        db.commit()
        
        # Clean up
        os.remove(temp_path)
        
        return {"message": "Document uploaded successfully", "document_id": document_id, "chunks_processed": len(chunks)}
    
    except HTTPException:
        raise
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        logging.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Document upload failed: {str(e)}")

@app.get("/documents")
async def get_documents():
    db = next(get_db())
    documents = db.query(Document).all()
    return [
        DocumentResponse(
            id=doc.id,
            filename=doc.filename,
            file_type=doc.file_type,
            upload_date=doc.upload_date,
            processed=doc.processed
        ) for doc in documents
    ]

# Query endpoint
@app.post("/query")
async def query_knowledge(request: QueryRequest):
    try:
        print(f"Processing query: {request.question}")  # Debug log
        response = knowledge_agent.query(
            question=request.question,
            user_id="default",
            context=request.context
        )
        
        return QueryResponse(
            answer=response["answer"],
            sources=response["sources"],
            conversation_id=response["conversation_id"]
        )
    
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        import traceback
        traceback.print_exc()  # This will print the full traceback
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    try:
        db = next(get_db())
        
        # Check if document exists
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from vector store
        vector_store.delete_document(document_id, "default")
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=f"Document deletion failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Personal Knowledge Copilot API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)