from rest_framework import serializers

from auth_.models import MainUser
from auth_.token import get_token
from utils.exceptions import CommonException
from django.utils.translation import gettext
from django.contrib.auth.hashers import make_password
from utils import messages, codes
from rest_framework_jwt.settings import api_settings


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def save(self):
        MainUser.objects.create_user(self.validated_data['username'],
                                     self.validated_data['password'],
                                     self.validated_data['first_name'],
                                     self.validated_data['last_name'])


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if not self.context['request'].user.check_password(attrs['password']):
            raise CommonException(detail=messages.WRONG_PASSWORD, code=codes.WRONG_PASSWORD)
        if attrs['password1'] != attrs['password2']:
            raise CommonException(detail=messages.PASSWORDS_NOT_SAME,
                                  code=codes.PASSWORDS_NOT_SAME)
        return attrs

    def change_password(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['password1'])
        user.save()


class ChangeDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

    def validate(self, attrs):
        if self.context['request'].user.email != attrs['email']:
            if MainUser.objects.filter(email=attrs['email']).exists():
                raise CommonException(detail=messages.ALREADY_EXIST,
                                      code=codes.ALREADY_EXIST)
        return attrs

    def change_details(self):
        user = self.context['request'].user
        if self.validated_data['first_name'] is not '':
            user.fist_name = self.validated_data['first_name']
        if self.validated_data['last_name'] is not '':
            user.last_name = self.validated_data['last_name']
        if self.validated_data['email'] is not '':
            user.email = self.validated_data['email']
        user.save()
