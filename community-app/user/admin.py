from .models import User
from django.contrib import admin
from django.contrib.auth import forms
from community.helper.pagination import CachingPaginator


class AdminChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


"""
    유저 어드민
"""


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    show_full_result_count = False
    paginator = CachingPaginator
    form = AdminChangeForm

    list_display = [
        "uuid",
        "email",
        "phone",
        "is_active",
        "created_at",
    ]
    list_display_links = [
        "uuid",
        "email",
        "phone",
        "is_active",
        "created_at",
    ]
    search_fields = [
        "uuid",
        "email",
        "phone",
    ]
    readonly_fields = [
        "last_login",
        "groups",
        "user_permissions",
    ]
    
