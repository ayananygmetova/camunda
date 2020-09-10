from rest_framework import serializers
from datetime import datetime

from auth_.models import MainUser
from utils.exceptions import CommonException
from utils import messages, codes


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
        try:
            attrs['email']
        except:
            return attrs
        if attrs['email'] is not None:
            if self.context['request'].user.email != attrs['email']:
                if MainUser.objects.filter(email=attrs['email']).exists():
                    raise CommonException(detail=messages.ALREADY_EXIST,
                                          code=codes.ALREADY_EXIST)
        return attrs

    def change_details(self):
        user = self.context['request'].user
        try:
            user.fio = self.validated_data['fio']
        except:
            pass
        try:
            user.email = self.validated_data['email']
        except:
            pass
        try:
            user.phone = self.validated_data['phone']
        except:
            pass
        user.rowversion = datetime.now()
        user.save()
