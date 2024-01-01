from django.urls import path
from user.views import v1

register = v1.UserRegisterViewSet.as_view({"post": "create"})
login = v1.UserLoginViewSet.as_view({"post": "create"})

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
]
