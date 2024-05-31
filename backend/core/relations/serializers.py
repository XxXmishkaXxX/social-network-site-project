from rest_framework import serializers
from .models import Friend, Follower, FriendRequest
from profiles.serializers import UserProfileShortData
from profiles.models import UserProfile



class FriendSerializer(serializers.ModelSerializer):
    
    user_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = Friend
        fields = '__all__'

    def get_user_profile(self, obj):
        user_profile = UserProfile.objects.get(user=obj.friend)
        return UserProfileShortData(user_profile).data

class FriendRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FriendRequest
        fields = '__all__'
    
    def create(self, validated_data):

        return FriendRequest.objects.create(**validated_data)


class SentFriendRequestSerializer(serializers.ModelSerializer):
    to_user_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = FriendRequest
        exclude = ('from_user',)
    
    def get_to_user_profile(self, obj):
        user_profile = UserProfile.objects.get(user=obj.to_user)
        return UserProfileShortData(user_profile).data

    
    

class ReceivedFriendRequestSerializer(serializers.ModelSerializer):
    from_user_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = FriendRequest
        exclude = ('to_user',)

    def get_from_user_profile(self, obj):
        user_profile = UserProfile.objects.get(user=obj.from_user)
        return UserProfileShortData(user_profile).data


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'