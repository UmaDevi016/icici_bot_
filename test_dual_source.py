#!/usr/bin/env python3
"""
Test script to verify dual source (PDF + Web) functionality
"""

from chatbot import ICICIInsuranceChatbot

def test_dual_source():
    """Test the chatbot with PDF and web content"""
    print("=" * 60)
    print("Testing ICICI Insurance Chatbot - Dual Source Mode")
    print("=" * 60)
    
    # Initialize chatbot
    print("\n🔄 Initializing chatbot...")
    bot = ICICIInsuranceChatbot()
    
    # Check chunk distribution
    total_chunks = len(bot.chunks)
    pdf_chunks = len([c for c in bot.chunks if '[PDF]' in c])
    web_chunks = len([c for c in bot.chunks if '[WEB]' in c])
    
    print(f"\n✅ Chatbot initialized successfully!")
    print(f"\n📊 Content Distribution:")
    print(f"   Total chunks: {total_chunks}")
    print(f"   PDF chunks:   {pdf_chunks} ({pdf_chunks/total_chunks*100:.1f}%)")
    print(f"   Web chunks:   {web_chunks} ({web_chunks/total_chunks*100:.1f}%)")
    
    # Test queries
    print(f"\n🧪 Testing queries...")
    test_queries = [
        "What is ICICI Insurance?",
        "What types of insurance plans are available?",
        "How do I file a claim?"
    ]
    
    session_id = "test_dual_source_123"
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        result = bot.chat(query, session_id)
        
        if result['status'] == 'success':
            print(f"✅ Status: {result['status']}")
            print(f"📚 Response: {result['response'][:150]}...")
        else:
            print(f"❌ Error: {result['response']}")
    
    print(f"\n{'=' * 60}")
    print("🎉 Dual source testing completed!")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    test_dual_source()
