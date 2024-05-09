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
    def post(self, request):
        try:
            email = EmailAddress.objects.get(email=request.data.get('email'))
            if email.verified:
                return Response({'status': True}, status=200)
        except:
            return Response({'status': 'error'})
        return Response({'status': False})



class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'EmailConfirmation.html'
