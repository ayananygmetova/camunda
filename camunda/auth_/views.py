from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.messages import (PASSWORD_CHANGED,
                            USER_DETAILS_CHANGED)
from utils.exceptions import CommonException
from django.utils.translation import gettext
from datetime import datetime
import requests
from rest_framework.permissions import IsAuthenticated
from utils import messages, codes
from auth_.token import get_token
from auth_.models import MainUser
from auth_.serializers import MainUserSerializer, ChangePasswordSerializer, ChangeDetailsSerializer, \
    RegistrationSerializer, LoginSerializer

USER = 'USER'


class SignUpView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return MainUser.objects.get(email=self.request.data.get('email'))

    def post(self, request):
        serializer_class = RegistrationSerializer(data={"email": self.request.data.get('email'),
                                                        "password": self.request.data.get('password'),
                                                        "fio": self.request.data.get('fio')})
        serializer_class.is_valid()
        serializer_class.save()
        url = 'http://dev.cheesenology.kz:8080/engine-rest/user/create'
        surname, name = (str(self.request.data.get('fio'))+" ").split(" ", 1)
        json = {
            "profile": {
                "id": str(self.request.data.get('email')).partition("@")[0],
                "firstName": name,
                "lastName": surname,
                "email": self.request.data.get('email'),
                "credentials": {
                    "password": self.request.data.get('password')
                }
            }
        }
        requests.post(url, json=json)
        return Response(serializer_class.data,
                        status=status.HTTP_200_OK)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            raise CommonException(detail=gettext(messages.NO_CREDENTIALS),
                                  code=codes.NO_CREDENTIALS)
        try:
            user = MainUser.objects.get(email=email)
            if not user.check_password(password):
                raise CommonException(detail=gettext(messages.WRONG_EMAIL_OR_PASSWORD),
                                      code=codes.WRONG_EMAIL_OR_PASSWORD)
        except MainUser.DoesNotExist:
            raise CommonException(detail={gettext(messages.EMAIL_DOESNT_EXIST)},
                                  code=codes.EMAIL_DOESNT_EXIST)
        token = get_token(user)
        user.last_login = datetime.now()
        user.save()
        url = "http://dev.cheesenology.kz:8080/camunda/app/admin/default/#/login"
        serializer = MainUserSerializer(user)
        return Response({'token': token, 'user': serializer.data},
                        status=status.HTTP_200_OK)


class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = self.request.user
        serializer = MainUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = ChangePasswordSerializer(data=self.request.data,
                                              context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.change_password()
        return Response({gettext(PASSWORD_CHANGED)},
                        status=status.HTTP_200_OK)


class ChangeDetails(generics.UpdateAPIView):
    serializer_class = ChangeDetailsSerializer
    queryset = MainUser.objects.all()

    def put(self, request):
        serializer = ChangeDetailsSerializer(data=request.data,
                                             context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.change_details()
        user = MainUserSerializer(self.request.user)
        return Response((gettext(USER_DETAILS_CHANGED),
                            user.data),
                            status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = ChangeDetailsSerializer(data=request.data,
                                             context={'request': self.request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.change_details()
        user = MainUserSerializer(self.request.user)
        return Response((gettext(USER_DETAILS_CHANGED),
                         user.data),
                        status=status.HTTP_200_OK)
