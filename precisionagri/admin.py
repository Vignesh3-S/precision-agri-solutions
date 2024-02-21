from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Agriculture,NPK,User,Search,ApiUser,Contact
from django.contrib.auth.admin import UserAdmin

admin.site.register(Agriculture)
admin.site.register(NPK)
admin.site.register(Session)
admin.site.register(Search)
admin.site.register(ApiUser)
admin.site.register(Contact)

class CustomUserAdmin(UserAdmin):
    admin.site.site_header = "PAS Administration"
    model = User
    list_display = ("username","email","date_joined","last_login","is_active")
    list_filter = ("is_staff", "is_active","is_superuser")
    fieldsets = (
        ("User Details", {"fields": ("username","state","district","native","mobile","userimg")}),
        ("Authentiction Details", {"fields": ("email","password")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_superuser","is_account_verified","is_PAS_account","is_api_token_obtained", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("date_joined","date_updated","last_login")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1","password2","is_staff","is_active")}
        ),
    )
    readonly_fields = ("date_updated","date_joined","last_login",)
    search_fields = ("email","mobile",)
    ordering = ("date_joined",)

admin.site.register(User, CustomUserAdmin)


# Register your models here.
