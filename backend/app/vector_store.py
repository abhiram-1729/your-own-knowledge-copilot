import chromadb
from chromadb.config import Settings
import uuid
import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.persist_directory = "./chroma_db"
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Use ChromaDB's default embedding function with error handling
        try:
            self.collection = self.client.get_or_create_collection(
                name="knowledge_documents",
                metadata={"description": "Personal knowledge documents"}
            )
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, chunks: List[Dict], document_id: str, user_id: str, filename: str):
        """Add document chunks to vector store"""
        if not chunks:
            logger.warning("No chunks to add to vector store")
            return
            
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_{i}"
            ids.append(chunk_id)
            documents.append(chunk["content"])
            
            metadata = {
                "document_id": document_id,
                "user_id": user_id,
                "filename": filename,
                "chunk_index": i,
                "chunk_type": chunk.get("type", "text"),
                "page_number": chunk.get("page_number", 0)
            }
            metadatas.append(metadata)
        
        try:
            # Add to collection - ChromaDB will handle embeddings automatically
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Successfully added {len(chunks)} chunks to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def search(self, query: str, user_id: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant documents"""
        try:
            # Search in vector store - ChromaDB handles embedding internally
            # Removed user filtering since no authentication
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            formatted_results = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if results['distances'] else 0
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    def delete_document(self, document_id: str, user_id: str):
        """Delete all chunks of a document"""
        try:
            # Get all chunks for this document
            results = self.collection.get(where={"document_id": document_id})
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted document {document_id} from vector store")
        except Exception as e:
            logger.error(f"Error deleting document from vector store: {e}")