from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from EnglishLearning import settings


class User(AbstractUser):
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    email = models.EmailField()
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')  # todo upload_to
    enabled = models.BooleanField(default=True)


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
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE, related_name='profile')
    score = models.FloatField(default=0)


class Payment(models.Model):
    amount = models.IntegerField()
    time = models.DateTimeField()
    end_time = models.DateTimeField()
    learner = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Subtitle(models.Model):
    text = models.CharField(max_length=10000)
    upload_time = models.DateTimeField()
    learner = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Exam(models.Model):
    time = models.DateTimeField()
    score = models.FloatField()
    learner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    words = models.ManyToManyField("Word")


class Word(models.Model):
    english_word = models.CharField(max_length=64)
    translation = models.CharField(max_length=64)
    difficulty = models.CharField(max_length=64)


class Flashcard(models.Model):
    learnt = models.BooleanField()
    learner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
