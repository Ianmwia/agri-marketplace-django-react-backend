from rest_framework import serializers
from .models import Thread, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_role = serializers.CharField(source='sender.get_role_display', read_only=True)
    sender = serializers.ReadOnlyField(source='sender.email')

    class Meta:
        model = Message
        fields = ['id', 'thread', 'sender', 'sender_name', 'sender_role', 'text', 'created_at', 'is_read']
        read_only_fields = ['sender', 'created_at']

    def get_sender_name(self, obj):
        return f'{obj.sender.first_name} {obj.sender.last_name}'.strip() or obj.sender.email

class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    #user1 details
    user1_name = serializers.SerializerMethodField()
    user1_role = serializers.CharField(source='user1.get_role_display', read_only=True) 

    #user2 details
    user2_name = serializers.SerializerMethodField()
    user2_role = serializers.CharField(source='user2.get_role_display', read_only=True) 

    class Meta:
        model = Thread
        fields = ['id', 'user1', 'user2', 'user1_name', 'user2_name','user1_role','user2_role', 'updated_at', 'messages']

    def get_user1_name(self, obj):
        return f'{obj.user1.first_name} {obj.user1.last_name}'.strip() or obj.user1.email
    
    def get_user2_name(self, obj):
        return f'{obj.user2.first_name} {obj.user2.last_name}'.strip() or obj.user2.email