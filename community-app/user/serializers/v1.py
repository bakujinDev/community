from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import User
from datetime import datetime

"""
    회원 가입 / 로그인 관련 시리얼라이저
"""


# 이메일 체크
class UserEmailValidateSerializer(serializers.Serializer):
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


# 비밀번호 체크
class PasswordValidateSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)


# 전화번호 체크
class UserPhoneValidateSerializer(serializers.Serializer):
    phone = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


# 회원가입 시리얼라이저
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "phone")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if (
            validated_data.get("phone")
            and User.objects.filter(phone=validated_data.get("phone")).exists() is False
        ):  # 전화번호 저장하기
            user.phone = validated_data["phone"]
            user.phone_verification = True
            user.phone_verify_at = datetime.now()

        user.save()

        return user


class UserReturnV1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_active",
            "is_staff",
            "is_admin",
            "is_superuser",
            "user_permissions",
            "groups",
        )
