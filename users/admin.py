from django.contrib import admin

from users.models import User, Profile, Flashcard, Word, Subtitle, Exam


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'image', 'enabled',)


@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('score',)


@admin.register(Flashcard)
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('learnt', 'word')


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('english_word', 'difficulty')


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'upload_time', 'learner')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('learner', 'score')
