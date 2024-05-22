from rest_framework import serializers
from .models import UserProfile
from string import punctuation
from cities_light.models import Country, City
from wall.models import Post
from wall.serializers import PostSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    full_name = serializers.CharField()
    birth_date = serializers.DateField(format="%Y-%m-%d")
    bio = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    country = serializers.CharField()
    city = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = '__all__'


    def validate_full_name(self, full_name):
        
        try:
            print(full_name)
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
            raise serializers.ValidationError('Вы забыли заполнить имя или фамилию')

    
    def create(self, validated_data):
        
        try:
            print(validated_data)
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
        
        country_id = validated_data.get('country')
        city_id = validated_data.get('city')
        
        if country_id:
            try:
                country_instance = Country.objects.get(id=country_id)
                instance.country = country_instance
            except Country.DoesNotExist:
                raise serializers.ValidationError("Invalid country ID")

        if city_id:
            try:
                city_instance = City.objects.get(id=city_id)
                instance.city = city_instance
            except Country.DoesNotExist:

                raise serializers.ValidationError("Invalid city ID")

        instance.save()
        return instance
    
    def get_country(self, obj):
        return obj.country.name if obj.country else 'Не указан'

    def get_city(self, obj):
        return obj.city.name if obj.city else 'Не указан'
    
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

class UserProfileWithPostsSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'  # Adjust the fields as per your UserProfile model

    def get_posts(self, obj):
        posts = Post.objects.filter(author=obj)
        return PostSerializer(posts, many=True).data


class UserProfileShortData(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk', 'full_name', 'avatar', ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']
