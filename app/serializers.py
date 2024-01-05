from rest_framework import serializers
from .models import Note
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth import authenticate

User = get_user_model()

# Authentication
        
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email', None)
        if not email:
            raise serializers.ValidationError('Email is required for account creation.')

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email must be unique.')

        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(self.context['request'], username=username, password=password)

        if user and user.is_active:
            return {'user': user}

        raise serializers.ValidationError('Incorrect Credentials')
    
    
# Notes

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        
class ShareNoteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    
class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']