from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer

@api_view(['GET'])
def chat_rooms(request):
    """Get list of rooms"""
    rooms = ChatRoom.objects.all()
    serializer = ChatRoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def room_messages(request, room_id):
    """Get all messages in a room"""
    messages = ChatMessage.objects.filter(chat_room_id=room_id).order_by('created_at')
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)
