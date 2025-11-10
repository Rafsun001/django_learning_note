from rest_framework import serializers
from .models import ChatRoom, ChatMessage


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for ChatRoom model"""

    class Meta:
        model = ChatRoom
        fields = ['id', 'name']  # only include what we need


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for ChatMessage model"""
    
    # This will show the sender’s username instead of just their ID
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat_room', 'sender', 'content', 'created_at']
        read_only_fields = ['created_at']
