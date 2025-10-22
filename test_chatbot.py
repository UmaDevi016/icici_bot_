#!/usr/bin/env python3
"""
Simple test script to verify the chatbot functionality
"""

import requests
import json
import time

def test_chatbot():
    """Test the chatbot API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing ICICI Insurance Chatbot...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health Check:")
            print(f"   Status: {health_data['status']}")
            print(f"   Chatbot Ready: {health_data['chatbot_ready']}")
            print(f"   Chunks Loaded: {health_data['chunks_loaded']}")
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    # Test chat endpoint
    test_messages = [
        "What is ICICI Insurance?",
        "What types of insurance do you offer?",
        "How can I file a claim?",
        "Thank you for the information"
    ]
    
    session_id = None
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🔄 Test {i}: {message}")
        
        try:
            payload = {"message": message}
            if session_id:
                payload["session_id"] = session_id
            
            response = requests.post(
                f"{base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                session_id = data["session_id"]  # Keep session for context
                
                print(f"✅ Response received:")
                print(f"   Status: {data['status']}")
                print(f"   Relevant Chunks: {data['relevant_chunks']}")
                print(f"   Response: {data['response'][:100]}...")
            else:
                print(f"❌ Chat request failed: {response.status_code}")
                print(f"   Error: {response.text}")
        
        except Exception as e:
            print(f"❌ Error in chat request: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    # Test history endpoint
    if session_id:
        print(f"\n🔄 Testing conversation history...")
        try:
            response = requests.get(f"{base_url}/history/{session_id}")
            if response.status_code == 200:
                history_data = response.json()
                print(f"✅ History retrieved:")
                print(f"   Session ID: {history_data['session_id']}")
                print(f"   Conversation Count: {len(history_data['history'])}")
            else:
                print(f"❌ History request failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error getting history: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Chatbot testing completed!")
    print("\n📝 Next steps:")
    print("1. Open your browser and go to http://localhost:8000")
    print("2. Start chatting with the ICICI Insurance assistant")
    print("3. Try asking about insurance products, claims, or policies")
    
    return True

if __name__ == "__main__":
    test_chatbot()
