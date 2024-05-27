from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserProfileSerializer, UserProfileShortData
from cities_light.models import Country, City
from .serializers import CountrySerializer, CitySerializer
from .models import UserProfile
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import RetrieveUpdateAPIView



class UserProfileCreate(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, )
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():

            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'status': True}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)
    

class UserProfileWallView(APIView):

    def get(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(user=pk)
            serializer = UserProfileSerializer(user_profile)
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

    def get(self, request):

        data = UserProfile.objects.get(user=request.user.pk)
        serializer = UserProfileSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        user_profile = get_object_or_404(UserProfile, user__id=request.user.pk)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCountriesView(APIView):

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetCitiesByCountry(APIView):

    def get(self, request, id):
        cities = City.objects.filter(country_id=id)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)