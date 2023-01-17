from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer
from .utils import Utils
from django.conf import settings


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data["email"])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")

        abs_url = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
            "Hi " + user.username + " Use link below to verify ur email \n" + abs_url
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify ur email",
        }
        Utils.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token=request.GET.get('token')
        print(token)
        try:
            print(jwt.decode(token, settings.SECRET_KEY))
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = CustomUser.objects.get(id = payload("user_id"))
            if not user.is_varified:           
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
