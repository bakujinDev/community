from django.urls import path
from user.views import v1

register = v1.UserRegisterViewSet.as_view({"post": "create"})
login = v1.UserLoginViewSet.as_view({"post": "create"})
user_info = v1.UserInfoViewSet.as_view({"get": "get"})

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("user_info/", user_info, name="userInfo"),
]
