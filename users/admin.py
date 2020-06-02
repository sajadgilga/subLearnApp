from django.contrib import admin

from users.models import User, Profile, Flashcard, Word


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'image', 'enabled',)


@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('score',)


@admin.register(Flashcard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('learnt',)


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('english_word', 'difficulty')
