from rest_framework import serializers
from .models import UserProfile
from relations.models import  Friend, FriendRequest
from string import punctuation
from cities_light.models import Country, City
import re



class UserProfileSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    full_name = serializers.CharField()
    birth_date = serializers.DateField(format="%Y-%m-%d")
    bio = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    country = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        
    def validate_country(self, country):
        
        if country == 'null':
            country= None
        
        if country:
            country = Country.objects.get(pk=int(country))
        
        return country

    def validate_city(self, city):

        if city == 'null':
            city = None

        if city:
            city = City.objects.get(pk=int(city))

        return city
    

    
    def validate_full_name(self, full_name):
        try:
            if not re.match(r'^[a-zA-Zа-яА-Я\s|-]+$', full_name):
                raise serializers.ValidationError('Имя или фамилия содержат недопустимые символы')
            
            first_name, second_name = full_name.split('|')

            if not (first_name and second_name):
                raise serializers.ValidationError('Полное имя должно содержать Имя и Фамилию')

            if len(first_name) > 150 or len(first_name) < 3:
                raise serializers.ValidationError('Имя должно быть длиной от 2 до 150 символов')

            if len(second_name) > 150 or len(second_name) < 3:
                raise serializers.ValidationError('Фамилия должна быть длиной от 2 до 150 символов')

            for sym in punctuation:
                if sym in first_name or sym in second_name:
                    raise serializers.ValidationError('Имя или фамилия содержит недопустимые символы')

            return ' '.join(full_name.split('|'))
        except Exception as ex:
            raise ex
    
    def create(self, validated_data):
        
        try:
            profile = UserProfile.objects.create(**validated_data)
            return profile

        except Exception as e:
            print(e)
            raise serializers.ValidationError("Пользователь уже имеет профиль")
        
    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        instance.sex = validated_data.get('sex', instance.sex)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.country = validated_data.get('country')
        instance.city = validated_data.get('city')
        

        instance.save()
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['country'] = {
            'id': instance.country.id,
            'name': instance.country.name
        } if instance.country else None
        data['city'] = {
            'id': instance.city.id,
            'name': instance.city.name
        } if instance.city else None
        return data


class UserProfileShortData(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk', 'full_name', 'avatar', ]


class UserProfileWithFriendStatusSerializer(serializers.ModelSerializer):
    
    is_friend = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_is_friend(self, obj):
        profile_owner = obj.user
        request_user = self.context['request'].user
        if request_user.is_anonymous:
            return {"is_friend": False, "is_request_sent": False}
            
        # Check if the users are friends
        is_friend = Friend.objects.filter(user=request_user, friend=profile_owner).exists()
            
        # Check if there is a friend request
        is_request_sent_to_user = FriendRequest.objects.filter(from_user=request_user, to_user=profile_owner, is_accepted=False).exists()
        
        is_request_sent_from_user = FriendRequest.objects.filter(from_user=profile_owner, to_user=request_user, is_accepted=False).exists()
            
        return {"is_friend": is_friend, "is_request_sent_to_user": is_request_sent_to_user, 'is_request_sent_from_user': is_request_sent_from_user}
    
    def get_is_following(self, obj):
        profile_owner = obj.user
        request_user = self.context['request'].user
        if request_user.is_anonymous:
            return False
        
        # Check if the request user is following the profile owner
        is_following = profile_owner.followers.filter(follower=request_user).exists()
        
        return is_following



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']
