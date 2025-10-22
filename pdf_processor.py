import PyPDF2
import re
from typing import List
import os

class PDFProcessor:
    def __init__(self, pdf_path: str, max_chunks: int = 200):
        self.pdf_path = pdf_path
        self.max_chunks = max_chunks
        self.chunks = []
    
    def extract_text_from_pdf(self) -> str:
        """Extract text from PDF file"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        # Remove multiple consecutive punctuation
        text = re.sub(r'([.,!?;:])\1+', r'\1', text)
        return text.strip()
    
    def create_chunks(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.strip()) > 0:
                chunks.append(chunk.strip())
            
            # Limit to max_chunks
            if len(chunks) >= self.max_chunks:
                break
        
        return chunks
    
    def process_pdf(self) -> List[str]:
        """Main method to process PDF and return chunks"""
        print(f"Processing PDF: {self.pdf_path}")
        
        # Extract text
        raw_text = self.extract_text_from_pdf()
        if not raw_text:
            return []
        
        # Clean text
        cleaned_text = self.clean_text(raw_text)
        
        # Create chunks
        self.chunks = self.create_chunks(cleaned_text)
        
        print(f"Created {len(self.chunks)} chunks from PDF")
        return self.chunks
    
    def get_chunks(self) -> List[str]:
        """Get processed chunks"""
        return self.chunks
    
    def save_chunks_to_file(self, output_path: str = "processed_chunks.txt"):
        """Save chunks to a text file for debugging"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, chunk in enumerate(self.chunks):
                    f.write(f"--- Chunk {i+1} ---\n")
                    f.write(chunk)
                    f.write("\n\n")
            print(f"Chunks saved to {output_path}")
        except Exception as e:
            print(f"Error saving chunks: {e}")

if __name__ == "__main__":
    # Test the processor
    processor = PDFProcessor("ICICI_Insurance.pdf")
    chunks = processor.process_pdf()
    processor.save_chunks_to_file()
    print(f"Total chunks created: {len(chunks)}")
