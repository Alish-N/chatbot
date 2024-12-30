from flask import Blueprint, request, jsonify, render_template
from app.models.user import User
from app.models.chat import Chat, Message
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    try:
        # Create user instance without password_hash first
        user = User(
            username=data['username'],
            email=data['email']
        )
        # Set password separately using the method that handles hashing
        user.set_password(data['password'])
        user.save()
        
        return jsonify({
            'status': 'success',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    
    try:
        user = User.objects.get(email=data['email'])
        if user.check_password(data['password']):
            return jsonify({
                'status': 'success',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401
    except User.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/api/chats', methods=['POST'])
def create_chat():
    data = request.get_json()
    
    try:
        participants = [User.objects.get(id=user_id) 
                       for user_id in data['participant_ids']]
        
        chat = Chat(participants=participants)
        chat.save()
        
        return jsonify({
            'status': 'success',
            'chat': chat.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/api/chats/<chat_id>/messages', methods=['POST'])
def send_message(chat_id):
    data = request.get_json()
    
    try:
        chat = Chat.objects.get(id=chat_id)
        sender = User.objects.get(id=data['sender_id'])
        
        message = Message(
            sender=sender,
            content=data['content']
        )
        message.save()
        
        chat.messages.append(message)
        chat.updated_at = datetime.utcnow()
        chat.save()
        
        return jsonify({
            'status': 'success',
            'message': message.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400 