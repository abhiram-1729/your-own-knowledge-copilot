import pypdf
from docx import Document as DocxDocument
import email
from email import policy
from bs4 import BeautifulSoup
import os
from typing import List, Dict
import chardet
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    async def process_document(self, file_path: str, filename: str) -> List[Dict]:
        """Process different document types and return chunks"""
        file_extension = os.path.splitext(filename)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._process_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                return self._process_docx(file_path)
            elif file_extension in ['.txt', '.md']:
                return self._process_text(file_path)
            elif file_extension == '.eml':
                return self._process_email(file_path)
            elif file_extension in ['.html', '.htm']:
                return self._process_html(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            logger.error(f"Error processing document {filename}: {e}")
            raise
    
    def _process_pdf(self, file_path: str) -> List[Dict]:
        """Extract text from PDF and chunk it"""
        chunks = []
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        text = page.extract_text()
                        if text and text.strip():
                            page_chunks = self._chunk_text(text, page_num + 1)
                            chunks.extend(page_chunks)
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                        continue
            
            if not chunks:
                logger.warning(f"No text extracted from PDF: {file_path}")
            
            logger.info(f"Processed PDF with {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {e}")
            raise
    
    def _process_docx(self, file_path: str) -> List[Dict]:
        """Extract text from DOCX and chunk it"""
        try:
            doc = DocxDocument(file_path)
            full_text = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text and paragraph.text.strip():
                    full_text.append(paragraph.text)
            
            text = '\n'.join(full_text)
            if not text.strip():
                logger.warning(f"No text extracted from DOCX: {file_path}")
                return []
            
            chunks = self._chunk_text(text)
            logger.info(f"Processed DOCX with {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing DOCX {file_path}: {e}")
            raise
    
    def _process_text(self, file_path: str) -> List[Dict]:
        """Process plain text files"""
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
                text = raw_data.decode(encoding)
            
            if not text.strip():
                logger.warning(f"No text content in file: {file_path}")
                return []
            
            chunks = self._chunk_text(text)
            logger.info(f"Processed text file with {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            raise
    
    def _process_email(self, file_path: str) -> List[Dict]:
        """Extract content from email files"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                msg = email.message_from_file(file, policy=policy.default)
            
            email_content = {
                'subject': msg['subject'] or '',
                'from': msg['from'] or '',
                'to': msg['to'] or '',
                'date': msg['date'] or '',
                'body': ''
            }
            
            # Extract body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        email_content['body'] = part.get_content()
                        break
            else:
                email_content['body'] = msg.get_content()
            
            # Format email as text
            email_text = f"Subject: {email_content['subject']}\nFrom: {email_content['from']}\nTo: {email_content['to']}\nDate: {email_content['date']}\n\n{email_content['body']}"
            
            chunks = self._chunk_text(email_text, chunk_type="email")
            logger.info(f"Processed email with {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing email {file_path}: {e}")
            raise
    
    def _process_html(self, file_path: str) -> List[Dict]:
        """Extract text from HTML files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                text = soup.get_text()
            
            chunks = self._chunk_text(text, chunk_type="html")
            logger.info(f"Processed HTML with {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing HTML {file_path}: {e}")
            raise
    
    def _chunk_text(self, text: str, page_number: int = 0, chunk_type: str = "text") -> List[Dict]:
        """Split text into overlapping chunks"""
        chunks = []
        
        if not text or not text.strip():
            return chunks
            
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append({
                "content": chunk_text,
                "type": chunk_type,
                "page_number": page_number,
                "word_count": len(chunk_words)
            })
        
        return chunks