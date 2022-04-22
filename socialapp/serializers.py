from attr import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import PostManager

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=User.objects.all())],required = True)
    class Meta:
        model = User
        fields = "__all__"
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
        

class PostManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostManager
        fields = "__all__"
    
    def create(self,validated_data):
        
        posts = PostManager.objects.create(
            hashtag = validated_data['hashtag'],
            image = validated_data["image"],
            user_id = validated_data["user_id"]
        )
        posts.save()
        return posts
    
    def update(self, instance, validated_data):
        pass

class SerachSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostManager
        fields ="__all__"