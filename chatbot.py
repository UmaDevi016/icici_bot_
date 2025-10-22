from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import pickle
import os
from pdf_processor import PDFProcessor
from database import ConversationDB

class ICICIInsuranceChatbot:
    def __init__(self, pdf_path: str = "ICICI_Insurance.pdf", model_name: str = "all-MiniLM-L6-v2"):
        self.pdf_path = pdf_path
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None
        self.db = ConversationDB()
        self.embeddings_file = "embeddings.pkl"
        self.chunks_file = "chunks.pkl"
        
        # Load or create embeddings
        self.load_or_create_embeddings()
    
    def load_or_create_embeddings(self):
        """Load existing embeddings or create new ones"""
        if os.path.exists(self.embeddings_file) and os.path.exists(self.chunks_file):
            print("Loading existing embeddings...")
            self.load_embeddings()
        else:
            print("Creating new embeddings...")
            self.create_embeddings()
    
    def create_embeddings(self):
        """Process PDF and create embeddings"""
        # Process PDF
        processor = PDFProcessor(self.pdf_path, max_chunks=200)
        self.chunks = processor.process_pdf()
        
        if not self.chunks:
            raise Exception("No chunks created from PDF")
        
        # Create embeddings
        print("Creating embeddings for chunks...")
        self.embeddings = self.model.encode(self.chunks)
        
        # Save embeddings and chunks
        self.save_embeddings()
        print(f"Created embeddings for {len(self.chunks)} chunks")
    
    def save_embeddings(self):
        """Save embeddings and chunks to files"""
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(self.embeddings, f)
        
        with open(self.chunks_file, 'wb') as f:
            pickle.dump(self.chunks, f)
        
        print("Embeddings saved successfully")
    
    def load_embeddings(self):
        """Load embeddings and chunks from files"""
        try:
            with open(self.embeddings_file, 'rb') as f:
                self.embeddings = pickle.load(f)
            
            with open(self.chunks_file, 'rb') as f:
                self.chunks = pickle.load(f)
            
            print(f"Loaded embeddings for {len(self.chunks)} chunks")
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            self.create_embeddings()
    
    def find_relevant_chunks(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Find most relevant chunks for a query"""
        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top-k most similar chunks
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        relevant_chunks = []
        for idx in top_indices:
            relevant_chunks.append((self.chunks[idx], similarities[idx]))
        
        return relevant_chunks
    
    def generate_response(self, query: str, relevant_chunks: List[Tuple[str, float]], 
                         conversation_context: str = "") -> str:
        """Generate response based on relevant chunks and context"""
        # Filter chunks with similarity above threshold
        filtered_chunks = [chunk for chunk, score in relevant_chunks if score > 0.3]
        
        if not filtered_chunks:
            return ("I apologize, but I couldn't find relevant information in the ICICI Insurance "
                   "documentation to answer your question. Could you please rephrase your question "
                   "or ask about specific ICICI Insurance products or services?")
        
        # Create context from relevant chunks
        context = "\n\n".join(filtered_chunks[:3])  # Use top 3 chunks
        
        # Simple response generation based on context
        response = self.create_contextual_response(query, context, conversation_context)
        
        return response
    
    def create_contextual_response(self, query: str, context: str, conversation_context: str) -> str:
        """Create a contextual response based on the query and retrieved information"""
        query_lower = query.lower()
        
        # Extract key information from context
        response_parts = []
        
        # Add relevant information from context
        sentences = context.split('.')
        relevant_sentences = []
        
        # Find sentences that might be relevant to the query
        query_keywords = set(query_lower.split())
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in query_keywords if len(keyword) > 2):
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            # Take the most relevant sentences
            response = ". ".join(relevant_sentences[:3])
            if not response.endswith('.'):
                response += "."
        else:
            # Fallback to first part of context
            response = ". ".join(sentences[:2])
            if not response.endswith('.'):
                response += "."
        
        # Add conversational elements
        if "thank" in query_lower:
            response = "You're welcome! " + response
        elif "hello" in query_lower or "hi" in query_lower:
            response = "Hello! I'm here to help you with ICICI Insurance queries. " + response
        
        return response
    
    def chat(self, query: str, session_id: str) -> Dict:
        """Main chat method"""
        try:
            # Create session if it doesn't exist
            self.db.create_session(session_id)
            
            # Get conversation context
            conversation_context = self.db.get_recent_context(session_id, limit=3)
            
            # Find relevant chunks
            relevant_chunks = self.find_relevant_chunks(query, top_k=5)
            
            # Generate response
            response = self.generate_response(query, relevant_chunks, conversation_context)
            
            # Store conversation in database
            context_chunks = [chunk for chunk, _ in relevant_chunks[:3]]
            self.db.add_conversation(session_id, query, response, context_chunks)
            
            return {
                "response": response,
                "relevant_chunks": len(relevant_chunks),
                "session_id": session_id,
                "status": "success"
            }
        
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            return {
                "response": error_response,
                "relevant_chunks": 0,
                "session_id": session_id,
                "status": "error"
            }
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        return self.db.get_conversation_history(session_id)
    
    def cleanup_files(self):
        """Clean up temporary files"""
        files_to_remove = ["processed_chunks.txt"]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
                print(f"Removed {file}")

if __name__ == "__main__":
    # Test the chatbot
    chatbot = ICICIInsuranceChatbot()
    
    # Test queries
    test_queries = [
        "What is ICICI Insurance?",
        "What types of insurance do you offer?",
        "How can I file a claim?"
    ]
    
    session_id = "test_session"
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = chatbot.chat(query, session_id)
        print(f"Response: {result['response']}")
        print(f"Status: {result['status']}")
