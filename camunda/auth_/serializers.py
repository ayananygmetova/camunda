from rest_framework import serializers

from auth_.models import MainUser
from auth_.token import get_token
from utils.exceptions import CommonException
from django.utils.translation import gettext
from django.contrib.auth.hashers import make_password
from utils import messages, codes

from datetime import datetime
from rest_framework_jwt.settings import api_settings


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ('email', 'fio', 'phone', 'image_url', 'image_url_orig')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    fio = serializers.CharField()

    def save(self):
        camunda_id=self.validated_data['email'].partition('@')[0]
        MainUser.objects.create_user(self.validated_data['email'],
                                     self.validated_data['password'],
                                     self.validated_data['fio'],
                                     camunda_id)


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
    fio = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()

    def validate(self, attrs):
        if self.context['request'].user.email != attrs['email']:
            if MainUser.objects.filter(email=attrs['email']).exists():
                raise CommonException(detail=messages.ALREADY_EXIST,
                                      code=codes.ALREADY_EXIST)
        return attrs

    def change_details(self):
        user = self.context['request'].user
        user.fio = self.validated_data['fio']
        user.email = self.validated_data['email']
        user.phone = self.validated_data['phone']
        user.rowversion = datetime.now()
        user.save()
