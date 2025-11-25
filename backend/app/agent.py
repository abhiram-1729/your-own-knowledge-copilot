from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class KnowledgeAgent:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.conversation_memory = {}
        
        # Try to initialize Gemini, but don't fail if not available
        self.gemini_available = False
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.gemini_available = True
                logger.info("Gemini AI initialized successfully")
            else:
                logger.warning("GEMINI_API_KEY not set. Using fallback responses.")
        except ImportError:
            logger.warning("google-generativeai not installed. Using fallback responses.")
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini: {e}. Using fallback responses.")
    
    def query(self, question: str, user_id: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        # Get conversation history
        conversation_id = self._get_conversation_id(context)
        history = self._get_conversation_history(conversation_id)
        
        # Search for relevant documents
        relevant_docs = self.vector_store.search(question, user_id, n_results=5)
        
        if not relevant_docs:
            return {
                "answer": "I couldn't find any relevant information in your documents to answer this question. Please upload relevant documents first.",
                "sources": [],
                "conversation_id": conversation_id
            }
        
        # Build context from documents
        context_text = self._build_context(relevant_docs, history)
        
        # Generate answer
        if self.gemini_available:
            answer = self._generate_gemini_answer(question, context_text, history)
        else:
            answer = self._generate_smart_fallback_answer(question, context_text, relevant_docs)
        
        # Update conversation history
        self._update_conversation_history(conversation_id, question, answer)
        
        # Only include sources if the answer contains actual information
        no_info_phrases = [
            "couldn't find this information",
            "couldn't find any relevant information",
            "please upload relevant documents",
            "not found in your uploaded documents"
        ]
        
        answer_lower = answer.lower()
        has_information = not any(phrase in answer_lower for phrase in no_info_phrases)
        
        # Get unique sources only if information was found
        unique_sources = self._get_unique_sources(relevant_docs) if has_information else []
        
        return {
            "answer": answer,
            "sources": unique_sources,
            "conversation_id": conversation_id
        }
    
    def _generate_gemini_answer(self, question: str, context: str, history: List[Dict]) -> str:
        try:
            import google.generativeai as genai
            
            # Build the prompt for Gemini
            prompt = self._build_gemini_prompt(question, context, history)
            logger.info(f"Sending prompt to Gemini, context length: {len(context)}")
            
            # Generate response with safety settings
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=1000,
                )
            )
            
            if response.text:
                logger.info(f"Gemini response: {response.text[:200]}...")
                return response.text
            else:
                logger.warning("Gemini returned empty response")
                return self._generate_smart_fallback_answer(question, context, [])
                
        except Exception as e:
            error_msg = str(e)
            if "leaked" in error_msg.lower() or "permission denied" in error_msg.lower():
                logger.error(f"API key issue: {e}")
                return "Your Gemini API key has been revoked. Please get a new API key from Google AI Studio and update your .env file."
            logger.error(f"Error calling Gemini API: {e}")
            return self._generate_smart_fallback_answer(question, context, [])
    
    def _build_gemini_prompt(self, question: str, context: str, history: List[Dict]) -> str:
        prompt = f"""You are a helpful AI assistant that answers questions based STRICTLY on the user's uploaded documents.

CONTEXT FROM USER'S DOCUMENTS:
{context}

CONVERSATION HISTORY:
{self._format_history(history)}

CURRENT QUESTION: {question}

CRITICAL INSTRUCTIONS:
1. You MUST answer using ONLY the information from the context provided above
2. Look for relevant information in the context that relates to the question, even if not an exact match
3. If the context contains information related to the question, extract and present it clearly
4. If the context truly doesn't contain any relevant information, respond with: "I couldn't find this information in your uploaded documents."
5. Do NOT use any external knowledge or make up information
6. Be concise and reference specific details from the context when available

FORMATTING GUIDELINES:
- Use clear headings with **bold text** for main concepts
- Use bullet points (•) for lists of items or strategies
- Use numbered lists (1., 2., etc.) for sequential steps
- Organize information with proper spacing and structure
- Keep paragraphs short and focused on single ideas

ANSWER:"""
        return prompt
    
    def _generate_smart_fallback_answer(self, question: str, context: str, relevant_docs: List[Dict]) -> str:
        """Generate a smart response using the document content when Gemini is not available"""
        if not context or not relevant_docs:
            return "I couldn't find this information in your uploaded documents. Please upload relevant documents first."
        
        # Check if any documents actually contain relevant keywords
        question_lower = question.lower()
        relevant_keywords = []
        
        for doc in relevant_docs[:3]:
            content_lower = doc['content'].lower()
            # Check for any word overlap between question and document
            question_words = set(question_lower.split())
            content_words = set(content_lower.split())
            overlap = question_words.intersection(content_words)
            
            if len(overlap) > 0:
                relevant_keywords.extend(list(overlap)[:3])  # Take first 3 overlapping words
        
        if not relevant_keywords:
            return "I couldn't find this information in your uploaded documents."
        
        # If some relevance found, provide limited information from documents
        key_content = []
        for doc in relevant_docs[:2]:  # Use top 2 most relevant documents
            content = doc['content']
            preview = content[:200] + "..." if len(content) > 200 else content
            key_content.append(preview)
        
        combined_content = " ".join(key_content)
        return f"Based on your documents, I found some information related to '{' '.join(relevant_keywords)}'. The documents mention: {combined_content}. However, I couldn't find a specific answer to your question in the uploaded materials."
    
    def _format_history(self, history: List[Dict]) -> str:
        if not history:
            return "No previous conversation."
        
        formatted = []
        for msg in history[-3:]:
            formatted.append(f"User: {msg['question']}")
            formatted.append(f"Assistant: {msg['answer']}")
        
        return "\n".join(formatted)
    
    def _build_context(self, documents: List[Dict], history: List[Dict]) -> str:
        context_parts = []
        
        for i, doc in enumerate(documents):
            source_info = f"From {doc['metadata']['filename']}:"
            context_parts.append(f"{source_info}\n{doc['content']}")
        
        context = "\n\n".join(context_parts)
        logger.info(f"Built context with {len(documents)} documents, total length: {len(context)}")
        return context
    
    def _get_unique_sources(self, documents: List[Dict]) -> List[Dict]:
        seen_files = set()
        unique_sources = []
        
        for doc in documents:
            filename = doc['metadata']['filename']
            if filename not in seen_files:
                seen_files.add(filename)
                unique_sources.append({
                    "filename": filename,
                    "content_preview": doc['content'][:150] + "..." if len(doc['content']) > 150 else doc['content']
                })
        
        return unique_sources
    
    def _get_conversation_id(self, context: Optional[Dict]) -> str:
        if context and "conversation_id" in context:
            return context["conversation_id"]
        return str(uuid.uuid4())
    
    def _get_conversation_history(self, conversation_id: str) -> List[Dict]:
        return self.conversation_memory.get(conversation_id, [])
    
    def _update_conversation_history(self, conversation_id: str, question: str, answer: str):
        if conversation_id not in self.conversation_memory:
            self.conversation_memory[conversation_id] = []
        
        self.conversation_memory[conversation_id].append({
            "question": question,
            "answer": answer,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        if len(self.conversation_memory[conversation_id]) > 10:
            self.conversation_memory[conversation_id] = self.conversation_memory[conversation_id][-10:]