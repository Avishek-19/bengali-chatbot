import os
from groq import Groq
from dotenv import load_dotenv

# Load your API key
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Store conversation history
conversation_history = []

# System prompt - This tells the AI how to behave
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
- Use Bengali numbers when appropriate (০, ১, ২... or English: 0, 1, 2...)

💬 RESPONSE STYLE:
- Keep responses short and clear (2-3 sentences max)
- Use bullet points for lists
- Be friendly but professional
- Always ask if they need more help
- Suggest related products when appropriate

⚠️ IMPORTANT:
- Never make up product prices
- Don't process actual payments
- Refer complex issues to management
- Always verify customer information before returns
"""

def chat_with_bot(user_message):
    """Send message to Groq and get response"""
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Get response from Groq with system prompt
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": SYSTEM_PROMPT  # Include system prompt
            }
        ] + conversation_history,  # Then add conversation
        max_tokens=1024,
        temperature=0.7
    )
    
    # Extract bot response
    bot_response = response.choices[0].message.content
    
    # Add bot response to history
    conversation_history.append({
        "role": "assistant",
        "content": bot_response
    })
    
    return bot_response

def main():
    """Main function to run chatbot"""
    print("=" * 70)
    print("🤖 E-Commerce Customer Support Chatbot (Bengali-English)")
    print("=" * 70)
    print("📱 Welcome to our customer support!")
    print("💬 Ask about products, orders, returns, or shipping")
    print("🌐 Type in Bengali or English (mixed is okay too!)")
    print("❌ Type 'exit' to quit")
    print("=" * 70)
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == "exit":
            print("\n✅ Thank you for using our service! Goodbye! 👋")
            break
        
        if not user_input:
            print("⚠️  Please type something...")
            continue
        
        print("\n🤖 Bot is thinking...")
        response = chat_with_bot(user_input)
        print(f"\n🤖 Bot: {response}")

if __name__ == "__main__":
    main()