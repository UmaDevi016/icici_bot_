from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import pickle
import os
from pdf_processor import PDFProcessor
from database import ConversationDB
from web_scraper import ICICIWebScraper
from faq import find_faq_answer

class ICICIInsuranceChatbot:
    def __init__(self, pdf_path: str = "ICICI_Insurance.pdf", model_name: str = "all-MiniLM-L6-v2", 
                 use_web_content: bool = True, max_pdf_chunks: int = 150, max_web_pages: int = 10):
        self.pdf_path = pdf_path
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None
        self.db = ConversationDB()
        self.embeddings_file = "embeddings.pkl"
        self.chunks_file = "chunks.pkl"
        self.use_web_content = use_web_content
        self.max_pdf_chunks = max_pdf_chunks
        self.max_web_pages = max_web_pages
        
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
        """Process PDF and web content, then create embeddings"""
        all_chunks = []
        
        # Process PDF
        print(f"Processing PDF (max {self.max_pdf_chunks} chunks)...")
        processor = PDFProcessor(self.pdf_path, max_chunks=self.max_pdf_chunks)
        pdf_chunks = processor.process_pdf()
        
        if pdf_chunks:
            # Add source tag to PDF chunks
            pdf_chunks = [f"[PDF] {chunk}" for chunk in pdf_chunks]
            all_chunks.extend(pdf_chunks)
            print(f"Added {len(pdf_chunks)} chunks from PDF")
        
        # Scrape and process web content
        if self.use_web_content:
            print(f"Scraping ICICI website (max {self.max_web_pages} pages)...")
            try:
                scraper = ICICIWebScraper(max_pages=self.max_web_pages)
                scraper.scrape_important_pages()
                web_chunks = scraper.create_chunks_from_web_content()
                
                if web_chunks:
                    # Limit web chunks to maintain total around 200
                    remaining_capacity = 200 - len(all_chunks)
                    web_chunks = web_chunks[:remaining_capacity]
                    
                    # Add source tag to web chunks
                    web_chunks = [f"[WEB] {chunk}" for chunk in web_chunks]
                    all_chunks.extend(web_chunks)
                    print(f"Added {len(web_chunks)} chunks from website")
            except Exception as e:
                print(f"Warning: Could not scrape web content: {e}")
                print("Continuing with PDF content only...")
        
        if not all_chunks:
            raise Exception("No chunks created from any source")
        
        self.chunks = all_chunks
        
        # Create embeddings
        print(f"Creating embeddings for {len(self.chunks)} total chunks...")
        self.embeddings = self.model.encode(self.chunks)
        
        # Save embeddings and chunks
        self.save_embeddings()
        print(f"✅ Successfully created embeddings for {len(self.chunks)} chunks")
        print(f"   - PDF chunks: {len([c for c in self.chunks if c.startswith('[PDF]')])}")
        print(f"   - Web chunks: {len([c for c in self.chunks if c.startswith('[WEB]')])}")
    
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
    
    def find_relevant_chunks(self, query: str, top_k: int = 8) -> List[Tuple[str, float]]:
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
        # Filter chunks with similarity above threshold (lowered for better recall)
        filtered_chunks = [(chunk, score) for chunk, score in relevant_chunks if score > 0.25]
        
        if not filtered_chunks:
            return ("I apologize, but I couldn't find relevant information in the ICICI Insurance "
                   "documentation and website to answer your question. Could you please rephrase your question "
                   "or ask about specific ICICI Insurance products or services?")
        
        # Separate sources
        sources = []
        clean_chunks = []
        
        # Use top 5 chunks instead of 3 for better context
        for chunk, score in filtered_chunks[:5]:
            if chunk.startswith('[PDF]'):
                sources.append('PDF')
                clean_chunks.append(chunk.replace('[PDF] ', ''))
            elif chunk.startswith('[WEB]'):
                sources.append('Website')
                clean_chunks.append(chunk.replace('[WEB] ', ''))
            else:
                clean_chunks.append(chunk)
        
        # Create context from relevant chunks
        context = "\n\n".join(clean_chunks[:5])
        
        # Simple response generation based on context
        response = self.create_contextual_response(query, context, conversation_context)
        
        # Add source information if available
        unique_sources = list(set(sources))
        if unique_sources:
            source_text = " and ".join(unique_sources)
            response += f"\n\n📚 Source: {source_text}"
        
        return response
    
    def create_contextual_response(self, query: str, context: str, conversation_context: str) -> str:
        """Create a contextual response based on the query and retrieved information"""
        query_lower = query.lower()
        
        # Handle greetings
        if any(word in query_lower for word in ["hello", "hi", "hey"]):
            return "Hello! I'm your ICICI Insurance assistant. I can help you with information about insurance products, claims, policies, and more. What would you like to know?"
        
        if "thank" in query_lower:
            return "You're welcome! Feel free to ask if you have any other questions about ICICI Insurance."
        
        # Clean up context - remove source tags and extra whitespace
        context = context.replace('[PDF]', '').replace('[WEB]', '')
        # Remove source prefixes like "From Life Insurance - ICICI Prudential..."
        import re
        context = re.sub(r'From [^:]+:\s*', '', context)
        context = re.sub(r'Source: [^.]+\.', '', context)
        sentences = [s.strip() for s in context.split('.') if s.strip()]
        
        # Extract query keywords (filter out common words)
        stop_words = {'what', 'is', 'are', 'the', 'how', 'can', 'do', 'does', 'tell', 'me', 'about', 'a', 'an', 'and', 'or', 'in', 'on', 'for', 'to', 'of', 'with'}
        query_keywords = [word for word in query_lower.split() if word not in stop_words and len(word) > 2]
        
        # Score sentences based on keyword matches and position
        scored_sentences = []
        for i, sentence in enumerate(sentences[:15]):  # Limit to first 15 sentences
            if len(sentence) < 20:  # Skip very short sentences
                continue
            
            # Skip sentences with technical jargon or UIN codes
            if 'UIN:' in sentence or 'WII' in sentence or len(sentence) > 500:
                continue
            
            sentence_lower = sentence.lower()
            score = 0
            
            # Score based on keyword matches
            for keyword in query_keywords:
                if keyword in sentence_lower:
                    score += 3
            
            # Prefer earlier sentences (they're usually more relevant)
            score += (15 - i) * 0.2
            
            # Prefer sentences with specific terms
            if any(term in sentence_lower for term in ['benefit', 'cover', 'premium', 'claim', 'policy', 'insurance']):
                score += 1.5
            
            # Boost sentences that look like answers
            if any(phrase in sentence_lower for phrase in ['you can', 'offers', 'provides', 'includes', 'available']):
                score += 2
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and take top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in scored_sentences[:4]]
        
        if not top_sentences:
            return "Based on the available information, " + sentences[0] if sentences else "I couldn't find specific information about that."
        
        # Build response based on query type
        response = self._build_structured_response(query_lower, top_sentences, query_keywords)
        
        return response
    
    def _build_structured_response(self, query_lower: str, sentences: List[str], keywords: List[str]) -> str:
        """Build a structured response based on query type"""
        
        # Question type detection
        if "what is" in query_lower:
            # Definition question
            response = sentences[0]
            # Add second sentence only if it adds value
            if len(sentences) > 1 and len(sentences[0]) < 150:
                response += " " + sentences[1]
        
        elif "what are" in query_lower or "what types" in query_lower:
            # List question
            response = "ICICI Insurance offers: " + sentences[0]
            if len(sentences) > 1 and len(response) < 180:
                response += " " + sentences[1]
        
        elif "how to" in query_lower or "how do" in query_lower or "how can" in query_lower:
            # Process/instruction question
            if "file" in query_lower and "claim" in query_lower:
                response = sentences[0]
            else:
                response = sentences[0]
            if len(sentences) > 1 and len(response) < 200:
                response += " " + sentences[1]
        
        elif "types" in query_lower or "kinds" in query_lower or "options" in query_lower:
            # Options question
            response = sentences[0]
            if len(sentences) > 1 and len(response) < 180:
                response += " " + sentences[1]
        
        elif "benefit" in query_lower or "advantage" in query_lower:
            # Benefits question
            response = "Key benefits include: " + sentences[0]
            if len(sentences) > 1 and len(response) < 200:
                response += " " + sentences[1]
        
        elif "claim settlement ratio" in query_lower or "settlement ratio" in query_lower:
            # Specific metric question
            response = "ICICI Prudential has a 99.3% claim settlement ratio for FY 2024-25, demonstrating strong reliability in processing claims."
        
        elif "contact" in query_lower or "customer support" in query_lower or "helpline" in query_lower:
            # Contact information
            response = sentences[0]
            if len(sentences) > 1:
                response += " " + sentences[1]
        
        elif "claim" in query_lower:
            # Claims question
            response = sentences[0]
            if len(sentences) > 1 and "claim" in sentences[1].lower():
                response += " " + sentences[1]
        
        else:
            # General question
            response = sentences[0]
            if len(sentences) > 1 and len(sentences[0]) < 150:
                response += " " + sentences[1]
        
        # Ensure proper ending
        if not response.endswith('.'):
            response += "."
        
        # Limit response length to avoid overwhelming users
        if len(response) > 350:
            # Try to cut at a sentence boundary
            response = response[:350].rsplit('.', 1)[0] + "."
        
        return response
    
    def chat(self, query: str, session_id: str) -> Dict:
        """Main chat method"""
        try:
            # Create session if it doesn't exist
            self.db.create_session(session_id)
            
            # Check FAQ database first for common questions
            faq_answer = find_faq_answer(query)
            if faq_answer:
                # Store FAQ conversation in database
                self.db.add_conversation(session_id, query, faq_answer, ["FAQ"])
                return {
                    "response": faq_answer + "\n\n📚 Source: FAQ",
                    "relevant_chunks": 1,
                    "session_id": session_id,
                    "status": "success"
                }
            
            # Get conversation context
            conversation_context = self.db.get_recent_context(session_id, limit=3)
            
            # Find relevant chunks
            relevant_chunks = self.find_relevant_chunks(query, top_k=8)
            
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
