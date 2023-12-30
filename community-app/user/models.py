import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        user = self.model(
            email=kwargs["email"],
            phone=kwargs["phone"],
        )

        user.set_password(kwargs["password"])
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(
            email=kwargs["email"],
            phone=kwargs["phone"],
            password=kwargs["password"],
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


"""
    유저 모델
    회원 유저 모델입니다.
"""


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "유저"
        verbose_name_plural = "유저"

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="전화번호",
        unique=True,
    )
    email = models.EmailField(
        verbose_name="이메일",
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="유저 활성화",
    )
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="가입날짜",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["phone"]

    def __str__(self) -> str:
        return f"{self.email}"
