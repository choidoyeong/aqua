from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model = Profile
       fields = ('weight',)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'password', 'profile')
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password_data = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password_data)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

class WaterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Water
        fields = ('user' , 'date', 'liters', 'titration_liters','success',)

class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = ('id','user', 'content', 'date')

class ScrapSerializer(serializers.ModelSerializer):
    tip = serializers.StringRelatedField()
    class Meta:
        model = Scrap
        fields = ('id','user', 'tip', 'date')
    