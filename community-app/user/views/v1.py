from datetime import datetime
from user.models import User
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.db import IntegrityError, transaction
from user.serializers.v1 import (
    UserEmailValidateSerializer,
    PasswordValidateSerializer,
    UserPhoneValidateSerializer,
    UserRegisterSerializer,
    UserReturnV1Serializer,
    UserPhoneLoginsSerializer,
)
from rest_framework.authtoken.models import Token


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    """
        POST /v1/user/register/
        회원가입 (v1)
    """

    @transaction.atomic()
    def create(self, request):
        email = request.data.get("email", None)
        req_data = request.data.copy()

        if email is None:
            count = 0
            while True:
                count += 1
                email = f"communityuser{User.objects.count()+count}@community.com"
                email_validate = UserEmailValidateSerializer(data={"email": email})
                if email_validate.is_valid() is True:
                    req_data.update({"email": email})
                    break

        password_validate = PasswordValidateSerializer(data=req_data)
        if password_validate.is_valid() is False:
            return Response(
                {"message": "비밀번호가 조건에 충족하지 않아요. 다시 설정해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 전화번호 인증 후 가입
        phone_validate = UserPhoneValidateSerializer(data=req_data)
        if phone_validate.is_valid() is False:
            return Response(
                {"message": "사용 할 수 없는 전화번호에요!"}, status=status.HTTP_409_CONFLICT
            )

        serializer = UserRegisterSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        user.save()

        return Response(
            {
                "token": token.key,
                "message": "회원가입에 성공했어요.",
                "user": UserReturnV1Serializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class UserLoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    """
        POST /v1/user/login/
        로그인 (v1)
    """

    def create(self, request):
        serializer = UserPhoneLoginsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(phone=serializer.validated_data["phone"])

        if user.is_active is False:
            return Response(
                {"message": "탈퇴 또는 관리자에 의해 중지된 계정입니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        is_check_password = user.check_password(serializer.validated_data["password"])
        if is_check_password is False:
            return Response(
                {
                    "message": "비밀번호가 일치하지 않아요.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.last_login = datetime.now()
        user.save(update_fields=["last_login"])
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": UserReturnV1Serializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


