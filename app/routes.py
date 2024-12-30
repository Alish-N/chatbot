from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.chat import Chat, Message

main = Blueprint('main', __name__)

@main.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    try:
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        user.save()
        return jsonify(user.to_dict()), 201
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
        
        return jsonify(chat.to_dict()), 201
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
        
        return jsonify(message.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400 