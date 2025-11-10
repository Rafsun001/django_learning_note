from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import ChatMessage, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Receive message from frontend and broadcast it"""
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']

        # Save to DB
        msg_obj = await self.save_message(message, sender)

        # Broadcast to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': str(msg_obj.created_at),
            }
        )

    async def chat_message(self, event):
        """Send message to WebSocket frontend"""
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, message, sender):
        """Save message to DB (async safe)"""
        return ChatMessage.objects.create(
            chat_room_id=self.room_id,
            sender=sender,
            content=message
        )
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################




























from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep

# Normal 
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocekt Connected ...", event)
        self.send({
            'type': 'websocket.accept'
        }) 

    def websocket_revcieve(self, event):
        print("Message revieved from client", event)
        print(event["text"])
        for i in range(50):
            self.send({
                'type' : "websocket.send",
                'text' : str(i)
            })
            sleep(1)

    def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()

# Normal
import asyncio
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocekt Connected ...", event)
        await self.send({
            'type': 'websocket.accept'
        }) 

    async def websocket_revcieve(self, event):
        print("Message revieved from client", event)
        print(event["text"])
        for i in range(50):
            await self.send({
                'type' : "websocket.send",
                'text' : str(i)
            })
            asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        raise StopConsumer()
    

# With Radis Channel Layers 
from asgiref.sync import async_to_sync
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocekt Connected ...", event)
        print("Channel Layer ...", self.channel_layer) # Channel Layer id  and info 
        print("Channel Name ...", self.channel_name) # Get channel layer name
        
        # Add channel to existing group or a new group
        async_to_sync(self.channel_layer.group_add)(
            'group_Name', # group name
            self.channel_name
            )

        self.send({
            'type': 'websocket.accept'
        }) 

    def websocket_revcieve(self, event):
        print("Message revieved from client", event["text"])
        
        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            'group_Name',{
                "type" : "chat.message",
                "message": event['text']
            }
        )
    
    def chat_message(self, event):
        print("Event ... ", event)
        self.send({
            'type': 'websocket.send',
            'text': event['message']  # ✅ fixed
        })

    def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        print("Channel Layer ...", self.channel_layer) 
        print("Channel Name ...", self.channel_name) 
   
        # Discard a channel from group if disconnected
        async_to_sync(self.channel_layer.group_discard)(
            'group_Name',
            self.channel_name
        ) 

        raise StopConsumer()

# With Radis Channel Layers 
import asyncio
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocekt Connected ...", event)
        print("Channel Layer ...", self.channel_layer) # Channel Layer id  and info 
        print("Channel Name ...", self.channel_name) # Get channel layer name

        # Add channel to existing group or a new group
        await self.channel_layer.group_add(
            'group_Name', # group name
            self.channel_name
            )

        await self.send({
            'type': 'websocket.accept'
        }) 

    async def websocket_revcieve(self, event):
        print("Message revieved from client", event["text"])
        
        # Send message to group
        await self.channel_layer.group_send(
            'group_Name',{
                "type" : "chat.message",
                "message": event['text']
            }
        )

    async def chat_message(self, event):
        print("Event ... ", event)
        await self.send({
            'type': 'websocket.send',
            'text': event['message']  # ✅ fixed
        })

    async def websocket_disconnect(self, event):
        print("Websocket Disconnected...", event)
        print("Channel Layer ...", self.channel_layer) 
        print("Channel Name ...", self.channel_name) 
   
        # Discard a channel from group if disconnected
        await self.channel_layer.group_discard(
            'group_Name',
            self.channel_name
        ) 
        raise StopConsumer()
    


# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from chating.models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]  
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        self.room_group_name = f"chat_{self.room_id}"
 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']
 
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',   
                'message': message,
                'sender': sender.username,
                "sender_image": sender.profile.image.url if sender.profile.image else None,
            }
        )
        message_instance = await self.create_message(message, sender)

    async def chat_message(self, event):
 
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async
    def create_message(self, message, sender):
        message = ChatMessage.objects.create(
            chat_room_id=self.room_id,
            sender=sender,
            content=message
        )