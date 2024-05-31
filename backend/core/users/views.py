from django.shortcuts import render
from rest_framework.authtoken.models import Token
from dj_rest_auth.registration.views import RegisterView, ConfirmEmailView
from users.serializers import CustomRegisterSerializer, CustomLoginSerializer
from dj_rest_auth.views import LoginView, PasswordChangeView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PasswordResetCode
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer, PasswordResetCompleteSerializer
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_decode




User = get_user_model()


class IsEmailConfirmed(APIView):
    def post(self, request):
        try:
            email = EmailAddress.objects.get(email=request.data.get('email'))
            if email.verified:
                return Response({'status':'Почта подтверждена'}, status.HTTP_200_OK)
        except:
            return Response({'status':'error'}, status.HTTP_500_INTERNAL_SERVER_ERROR )
        return Response({'status':'Почта не подтверждена'}, status.HTTP_400_BAD_REQUEST)




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


class PasswordChangeViewAPI(PasswordChangeView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                code = PasswordResetCode.objects.create(user=user)
                send_mail(
                    'Password Reset Code',
                    f'Your password reset code is {code.code}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
            return Response({'detail': 'Password reset code sent if the email exists'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                reset_code = PasswordResetCode.objects.get(code=code)
                if (timezone.now() - reset_code.created_at).total_seconds() > 3600:  # 1 hour validity
                    reset_code.delete()
                    return Response({'detail': 'Срок кода истек'}, status=status.HTTP_400_BAD_REQUEST)
                # Code is valid, proceed to reset password
                return Response({'uid': reset_code.user.id, 'code': str(reset_code.code)}, status=status.HTTP_200_OK)
            except PasswordResetCode.DoesNotExist:
                return Response({'detail': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)
        return Response({'detail':'Неверный формат кода'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetCompleteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetCompleteSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(pk=uid)
                reset_code = PasswordResetCode.objects.get(user=user, code=code)
                
                if reset_code:
                    user.set_password(new_password)
                    user.save()
                    reset_code.delete()
                    return Response({'detail': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Invalid reset code'}, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist, PasswordResetCode.DoesNotExist)as e:
                return Response({'detail': 'Invalid uid or code'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)