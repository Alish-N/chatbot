from flask import Blueprint, request, jsonify
from .models.chat import Chat, Message
from .models.user import User
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

api = Blueprint('api', __name__)

PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

def get_ai_response(message_content):
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Be precise and concise."
            },
            {
                "role": "user",
                "content": message_content
            }
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "max_tokens": 150,
        "stream": False
    }
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return str(e)

@api.route('/chat/start', methods=['POST'])
def start_chat():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        user = User.objects.get(id=user_id)
        chat = Chat(participants=[user])
        chat.save()
        
        return jsonify({
            'status': 'success',
            'chat_id': str(chat.id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/chat/<chat_id>/message', methods=['POST'])
def send_message(chat_id):
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')
        
        # Get chat and user
        chat = Chat.objects.get(id=chat_id)
        user = User.objects.get(id=user_id)
        
        # Save user message
        user_message = Message(
            sender=user,
            content=content
        )
        user_message.save()
        chat.messages.append(user_message)
        
        # Get AI response
        ai_response_content = get_ai_response(content)
        
        # Create and save AI message
        ai_message = Message(
            sender=user,  # You might want to create a special AI user
            content=ai_response_content,
            is_ai=True
        )
        ai_message.save()
        chat.messages.append(ai_message)
        
        # Update chat
        chat.updated_at = datetime.utcnow()
        chat.save()
        
        return jsonify({
            'status': 'success',
            'user_message': user_message.to_dict(),
            'ai_message': ai_message.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/chat/<chat_id>/history', methods=['GET'])
def get_chat_history(chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
        return jsonify({
            'status': 'success',
            'chat': chat.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400