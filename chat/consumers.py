import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Thread, Message
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.thread_id}'
        

        #join thread group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        #leave group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    #recieve message from wesocket
    async def receive(self, text_data = None, bytes_data = None):
        data = json.loads(text_data)
        message_text = data.get('message')
        user = self.scope['user']

        #save message
        thread = await database_sync_to_async(Thread.objects.get)(id=self.thread_id)
        message = await database_sync_to_async(Message.objects.create)(
            thread = thread,
            sender = user,
            text= message_text
        )

        #broadcast to group

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.text,
                'sender': user.email,
                'created_at': str(message.created_at)
            }
        )
    
    #receive message from group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))