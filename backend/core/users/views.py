from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.views import RegisterView, ConfirmEmailView
from users.serializers import CustomRegisterSerializer, CustomLoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from rest_framework.response import Response


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

    def post(self, request, *args, **kwargs):
        
        response = super().post(request, *args, **kwargs)
        if 'key' in response.data:
            token_key = response.data['key']

            user = Token.objects.get(key=token_key).user

            user_id = user.id

            response.data['id'] = user_id

        return response



class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'EmailConfirmation.html'
