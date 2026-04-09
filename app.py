import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# Store conversations
conversations = {}

SYSTEM_PROMPT = """You are a helpful E-Commerce Customer Support Agent for a Bangladeshi online store.

🎯 YOUR RESPONSIBILITIES:
1. Answer questions about products, prices, and availability
2. Help with orders, returns, and refunds
3. Provide shipping information
4. Handle complaints professionally
5. Speak in clear Bengali and English

📋 STORE INFORMATION:
- We sell electronics, clothing, and groceries
- Shipping to all Bangladesh divisions
- Free shipping on orders over 500 BDT
- 7-day return policy
- Payment methods: bKash, Nagad, Card, Bank Transfer

🌐 LANGUAGE RULES:
- If customer writes in Bengali, respond in Bengali
- If customer writes in English, respond in English
- If mixed, use both languages
- Always be polite and professional

💬 RESPONSE STYLE:
- Keep responses short and clear (2-3 sentences max)
- Be friendly but professional
- Always ask if they need more help
"""

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message is empty'}), 400
        
        if session_id not in conversations:
            conversations[session_id] = []
        
        conversation_history = conversations[session_id]
        
        conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": SYSTEM_PROMPT
                }
            ] + conversation_history,
            max_tokens=512,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content
        
        conversation_history.append({
            "role": "assistant",
            "content": bot_response
        })
        
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
            conversations[session_id] = conversation_history
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Check if server is running"""
    return jsonify({'status': 'running', 'message': 'Chatbot server is online! 🤖'}), 200

@app.route('/', methods=['GET'])
def home():
    """Home route"""
    return jsonify({
        'status': 'success',
        'message': 'E-Commerce Chatbot API is running',
        'endpoints': {
            '/chat': 'POST - Send message to chatbot',
            '/health': 'GET - Check server status'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')