from mongoengine import Document, StringField, ReferenceField, DateTimeField, ListField, BooleanField
from datetime import datetime
from .user import User

class Message(Document):
    sender = ReferenceField(User, required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    is_ai = BooleanField(default=False)
    
    meta = {
        'collection': 'messages',
        'ordering': ['-created_at']
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'sender': self.sender.to_dict(),
            'content': self.content,
            'created_at': self.created_at,
            'is_ai': self.is_ai
        }

class Chat(Document):
    participants = ListField(ReferenceField(User), required=True)
    messages = ListField(ReferenceField(Message))
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'chats',
        'ordering': ['-updated_at']
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'participants': [user.to_dict() for user in self.participants],
            'messages': [message.to_dict() for message in self.messages],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 