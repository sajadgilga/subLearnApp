from django.contrib import admin

from users.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'image', 'enabled',)


@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('score',)
