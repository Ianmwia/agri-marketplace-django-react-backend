from django.core import exceptions
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
import re

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password','role', 'location']

    def validate_password(self, data):
        if len(data) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', data):
            raise serializers.ValidationError('Password must have at least one Capital Letter')
        
        if not re.search(r'[!@#$%^&*()<>?/]', data):
            raise serializers.ValidationError('Password must have at least one symbol')
        
        user = CustomUser(data)
        #password = data.get('password')
        try:
            validate_password(password=data, user=user)
        except exceptions.ValidationError as error:
            raise serializers.ValidationError({"password":list(error.messages)})
        return data
    

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    '''
    LoginSerializer to validate credentials, no meta needed since we are checking not creating
    '''
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ProfileUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    # install pillow for drf to render
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','image', 'location', 'phone', 'role']
        read_only_fields = ['email', 'role']
