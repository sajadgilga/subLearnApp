from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from EnglishLearning import settings

fs = FileSystemStorage(location='media/subs')
imgFs = FileSystemStorage(location='media/profile_pics')


class User(AbstractUser):
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    email = models.EmailField()
    image = models.ImageField(default='default.jpeg', storage=imgFs)  # todo upload_to
    enabled = models.BooleanField(default=True)
    end_time = models.DateTimeField(null=True)

    #
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class Profile(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE,
                                related_name='profile')
    score = models.FloatField(default=0)


class Payment(models.Model):
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    learner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, )


class Subtitle(models.Model):
    name = models.CharField(max_length=256, default='')
    upload_time = models.DateTimeField(auto_now_add=True)
    learner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, )
    file = models.FileField(storage=fs, null=True)


class Exam(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()
    learner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, )
    words = models.ManyToManyField("Word")


class Word(models.Model):
    english_word = models.CharField(max_length=64)
    translation = models.CharField(max_length=64)
    difficulty = models.FloatField(default=7.7)


class Flashcard(models.Model):
    learnt = models.FloatField(default=0.2)
    learner = models.ForeignKey(Profile, null=False, blank=False, on_delete=models.CASCADE, )
    word = models.ForeignKey(Word, null=False, blank=False, on_delete=models.CASCADE, )
    subtitles = models.ManyToManyField(Subtitle, related_name='flashcards')
