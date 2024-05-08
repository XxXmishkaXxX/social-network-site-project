from django.shortcuts import render
from dj_rest_auth.registration.views import RegisterView, ConfirmEmailView
from users.serializers import CustomRegisterSerializer, CustomLoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress



User = get_user_model()

class IsEmailConfirmed(APIView):
    def get(self, request, email):
        user = request.user
        print(user)
        if not user.is_authenticated:
            return Response({'detail': 'User is not authenticated.'}, status=403)
        
        primary_email = EmailAddress.objects.get_primary(user)
        if not primary_email:
            return Response({'detail': 'No primary email associated with the user.'}, status=400)
        
        is_confirmed = primary_email.verified
        return Response({'is_confirmed': is_confirmed})



class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'EmailConfirmation.html'
