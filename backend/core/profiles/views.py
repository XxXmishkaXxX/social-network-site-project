from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserProfileSerializer, UserProfileShortData, UserProfileWithPostsSerializer
from cities_light.models import Country, City
from .serializers import CountrySerializer, CitySerializer
from .models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ObjectDoesNotExist



class UserProfileCreate(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, )
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        print(request.data, request.user)
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():

            serializer.validated_data['user'] = request.user
            
            country_id = request.data.get('country')
            country = Country.objects.get(id=country_id)
            
            city_id = request.data.get('city')
            city = City.objects.get(id=city_id)
            print(city, country)
            serializer.save(country=country, city=city)

            return Response({'status': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    

class UserProfileView(APIView):

    def get(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(user=pk)
            serializer = UserProfileWithPostsSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Профиль пользователя не найден"}, status=status.HTTP_404_NOT_FOUND)


class UserProfileShortDataView(APIView):
    
    def get(self, request, pk):
        try:
            data = UserProfile.objects.get(user=pk)
            serializer = UserProfileShortData(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Профиль пользователя не найден"}, status=status.HTTP_404_NOT_FOUND)


class UserProfileEditAPIView(APIView):

    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, )
    authentication_classes = [TokenAuthentication]

    def put(self, request, pk):
        user_profile = get_object_or_404(UserProfile, user__id=pk)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCountriesView(APIView):

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetCitiesByCountry(APIView):

    def get(self, request, id):
        cities = City.objects.filter(country_id=id)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)